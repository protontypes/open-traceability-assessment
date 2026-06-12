#!/usr/bin/env python3
"""
Run an Open Traceability Assessment multiple times against an open project,
open-science project, or report URL, then produce JSON and Markdown reports.

Example:
  export OPENAI_API_KEY="sk-..."
  pip install openai requests beautifulsoup4 pydantic pypdf

  python open_traceability_assessment.py \
    --project-url https://github.com/natcap/invest \
    --runs 5 \
    --include-total \
    --out-prefix invest_open_traceability

  python open_traceability_assessment.py \
    --project-url https://example.org/report.pdf \
    --runs 3 \
    --no-include-total
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import statistics
import textwrap
import time
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional
from urllib.parse import quote, urlparse

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, ConfigDict, Field

# The provider SDKs (openai, anthropic) are imported lazily in build_clients() so
# that running against a single provider does not require the other to be installed.


DEFAULT_DEFINITION_URL = "https://raw.githubusercontent.com/protontypes/open-traceability/refs/heads/main/docs/definition.md"
DEFAULT_PROJECT_URL = "https://github.com/natcap/invest"


# -----------------------------
# Structured output schema
# -----------------------------

class EvidenceReference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str = Field(description="Short human-readable label for the referenced artifact.")
    url: str = Field(description="URL of the artifact, page, repository file, issue tracker, paper, docs page, etc.")
    quote_or_finding: str = Field(description="Brief quote, paraphrase, or concrete observed finding.")
    relevance: str = Field(description="Why this reference supports the score.")


class StageAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stage: int = Field(ge=1, le=6)
    stage_name: str
    score: int = Field(ge=0, le=100)
    score_derivation: str = Field(
        description=(
            "Explain how the score was derived from evidence. Mention positive evidence, "
            "missing evidence, uncertainty, and why the exact score was selected."
        )
    )
    uncertainty: Literal["low", "medium", "high"] = Field(
        description="Overall confidence in this stage's score given the available evidence."
    )
    uncertainty_reason: str = Field(description="One sentence explaining the uncertainty level.")
    references: list[EvidenceReference]


class AssessmentRun(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_number: int
    project_name: str
    project_url: str
    stages: list[StageAssessment]
    total_score: Optional[int] = Field(
        default=None,
        ge=0,
        le=100,
        description="Leave null. Computed locally by the runner as the rounded mean of the stage scores.",
    )
    total_score_derivation: Optional[str] = Field(
        default=None,
        description="Leave null. Filled in locally by the runner.",
    )
    single_paragraph_summary: str
    limitations: list[str]
    model_name: Optional[str] = Field(
        default=None,
        description="Leave null. Set locally by the runner to the model that produced this run.",
    )


# -----------------------------
# Evidence collection
# -----------------------------

@dataclass
class EvidenceItem:
    label: str
    url: str
    text: str


def compact_text(text: str, max_chars: int) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 200].rstrip() + "\n\n...[truncated]..."


def http_get(url: str, timeout: int = 30) -> requests.Response:
    headers = {
        "User-Agent": "open-traceability-assessor/1.0",
        "Accept": "text/html,application/xhtml+xml,application/xml,text/plain,application/pdf,*/*",
    }
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response


def candidate_text_urls(url: str) -> list[str]:
    """Try HackMD's markdown download endpoint first when applicable."""
    urls = []
    parsed = urlparse(url)
    if "hackmd.io" in parsed.netloc and not parsed.path.endswith("/download"):
        urls.append(url.rstrip("/") + "/download")
    urls.append(url)
    return urls


def extract_text_from_response(response: requests.Response, source_url: str) -> str:
    content_type = response.headers.get("content-type", "").lower()
    raw = response.content

    if "application/pdf" in content_type or source_url.lower().endswith(".pdf"):
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("PDF input requires: pip install pypdf") from exc

        reader = PdfReader(io.BytesIO(raw))
        pages = []
        for i, page in enumerate(reader.pages):
            try:
                pages.append(f"\n\n--- PDF page {i + 1} ---\n{page.extract_text() or ''}")
            except Exception:
                pages.append(f"\n\n--- PDF page {i + 1} ---\n[Could not extract text]")
        return "\n".join(pages)

    text = raw.decode(response.encoding or "utf-8", errors="replace")

    if "html" in content_type or "<html" in text[:1000].lower():
        soup = BeautifulSoup(text, "html.parser")
        for tag in soup(["script", "style", "noscript", "svg"]):
            tag.decompose()
        return soup.get_text("\n")

    return text


def fetch_url_text(url: str, max_chars: int = 50_000) -> str:
    last_error: Optional[Exception] = None
    for candidate in candidate_text_urls(url):
        try:
            response = http_get(candidate)
            text = extract_text_from_response(response, candidate)
            if text.strip():
                return compact_text(text, max_chars)
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"Could not fetch text from {url}: {last_error}")


def parse_github_repo(url: str) -> Optional[tuple[str, str]]:
    parsed = urlparse(url)
    if parsed.netloc.lower() not in {"github.com", "www.github.com"}:
        return None
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 2:
        return None
    owner = parts[0]
    repo = parts[1].removesuffix(".git")
    return owner, repo


def github_headers() -> dict[str, str]:
    headers = {
        "User-Agent": "open-traceability-assessor/1.0",
        "Accept": "application/vnd.github+json",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def github_api_get(url: str) -> dict:
    response = requests.get(url, headers=github_headers(), timeout=30)
    response.raise_for_status()
    return response.json()


def github_raw_url(owner: str, repo: str, branch: str, path: str) -> str:
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{quote(branch, safe='')}/{quote(path)}"


IMPORTANT_FILE_PATTERNS = [
    r"(^|/)readme(\..*)?$",
    r"(^|/)license(\..*)?$",
    r"(^|/)citation(\.cff|\.md|\.txt)?$",
    r"(^|/)code[-_]?of[-_]?conduct(\..*)?$",
    r"(^|/)contributing(\..*)?$",
    r"(^|/)governance(\..*)?$",
    r"(^|/)security(\..*)?$",
    r"(^|/)authors(\..*)?$",
    r"(^|/)changelog(\..*)?$",
    r"(^|/)environment\.ya?ml$",
    r"(^|/)requirements.*\.txt$",
    r"(^|/)pyproject\.toml$",
    r"(^|/)setup\.(py|cfg)$",
    r"(^|/)dockerfile$",
    r"(^|/)docker-compose\.ya?ml$",
    r"(^|/)\.github/workflows/.*\.ya?ml$",
    r"(^|/)docs/.*\.(md|rst|txt)$",
    r"(^|/)documentation/.*\.(md|rst|txt)$",
    r"(^|/)examples?/.*\.(md|rst|py|ipynb)$",
    r"(^|/)tests?/.*\.(md|rst|py)$",
]


def important_path(path: str) -> bool:
    lower = path.lower()
    return any(re.search(pattern, lower) for pattern in IMPORTANT_FILE_PATTERNS)


def collect_github_evidence(
    project_url: str,
    max_files: int,
    max_file_chars: int,
    max_total_chars: int,
) -> tuple[str, list[EvidenceItem]]:
    owner_repo = parse_github_repo(project_url)
    if owner_repo is None:
        raise ValueError("Not a GitHub repository URL")

    owner, repo = owner_repo
    api_root = f"https://api.github.com/repos/{owner}/{repo}"

    repo_meta = github_api_get(api_root)
    default_branch = repo_meta.get("default_branch", "main")

    items: list[EvidenceItem] = [
        EvidenceItem(
            label="GitHub repository metadata",
            url=project_url,
            text=json.dumps(
                {
                    "full_name": repo_meta.get("full_name"),
                    "description": repo_meta.get("description"),
                    "homepage": repo_meta.get("homepage"),
                    "license": repo_meta.get("license", {}).get("spdx_id")
                    if repo_meta.get("license")
                    else None,
                    "default_branch": default_branch,
                    "created_at": repo_meta.get("created_at"),
                    "updated_at": repo_meta.get("updated_at"),
                    "open_issues_count": repo_meta.get("open_issues_count"),
                    "topics": repo_meta.get("topics", []),
                },
                indent=2,
            ),
        )
    ]

    tree_url = f"{api_root}/git/trees/{quote(default_branch, safe='')}?recursive=1"
    tree = github_api_get(tree_url).get("tree", [])

    paths = [
        entry["path"]
        for entry in tree
        if entry.get("type") == "blob" and important_path(entry.get("path", ""))
    ]

    # Prefer top-level governance/documentation files before deep examples/tests.
    paths = sorted(paths, key=lambda p: (p.count("/"), p.lower()))[:max_files]

    total_chars = sum(len(item.text) for item in items)

    for path in paths:
        if total_chars >= max_total_chars:
            break

        raw_url = github_raw_url(owner, repo, default_branch, path)
        try:
            response = http_get(raw_url)
            text = extract_text_from_response(response, raw_url)
            text = compact_text(text, max_file_chars)
        except Exception as exc:
            text = f"[Could not fetch file: {exc}]"

        remaining = max_total_chars - total_chars
        if remaining <= 0:
            break
        text = compact_text(text, min(max_file_chars, remaining))

        items.append(EvidenceItem(label=path, url=raw_url, text=text))
        total_chars += len(text)

    bundle_lines = [
        f"PROJECT URL: {project_url}",
        f"GITHUB REPOSITORY: {owner}/{repo}",
        f"DEFAULT BRANCH: {default_branch}",
        "",
        "Collected evidence artifacts:",
    ]

    for i, item in enumerate(items, start=1):
        bundle_lines.append(f"\n\n### Evidence {i}: {item.label}\nURL: {item.url}\n{item.text}")

    return "\n".join(bundle_lines), items


def collect_generic_evidence(project_url: str, max_chars: int) -> tuple[str, list[EvidenceItem]]:
    text = fetch_url_text(project_url, max_chars=max_chars)
    item = EvidenceItem(label="Input URL text extraction", url=project_url, text=text)
    bundle = f"PROJECT OR REPORT URL: {project_url}\n\n### Evidence 1: {item.label}\nURL: {item.url}\n{text}"
    return bundle, [item]


def collect_evidence(args: argparse.Namespace) -> tuple[str, list[EvidenceItem]]:
    if parse_github_repo(args.project_url):
        return collect_github_evidence(
            project_url=args.project_url,
            max_files=args.max_evidence_files,
            max_file_chars=args.max_file_chars,
            max_total_chars=args.max_evidence_chars,
        )

    return collect_generic_evidence(args.project_url, max_chars=args.max_evidence_chars)


# -----------------------------
# Prompting
# -----------------------------

SYSTEM_PROMPT = """You are an expert evaluator of open science, open-source software, environmental evidence chains, reproducibility, and scientific traceability.

Assess the supplied project or report using the Open Traceability definition supplied by the user. You must score stages 1-6 from 0 to 100. Use only the supplied assessment definition and supplied evidence bundle. Do not invent facts. If evidence is absent, score conservatively and say what evidence is missing.

Scoring calibration:
0-20: little or no public evidence for this dimension.
21-40: partial, fragmentary, or hard-to-verify evidence.
41-60: moderate evidence, but important gaps remain.
61-80: strong public evidence with some limitations.
81-100: excellent, explicit, versioned, reusable, externally verifiable evidence chain.

The six stages are:
1. Open Input Data and Measurement Evidence.
2. Open-Source Models, Methods, and Software.
3. Open Execution and Reproducibility.
4. Open Community and Review.
5. Open Publications and Communication.
6. Open Linkage.

For every stage:
- Give an integer score from 0 to 100.
- Provide a score derivation that explains why the score is not higher and not lower.
- Include references from the evidence bundle. Each reference must have a URL and concrete finding.
- If direct evidence is missing, include that absence in the derivation.
"""


def build_user_prompt(
    *,
    run_number: int,
    runs: int,
    project_url: str,
    definition_url: str,
    definition_text: str,
    evidence_bundle: str,
) -> tuple[str, str]:
    """Return ``(static_prefix, dynamic_suffix)`` for one assessment run.

    The static prefix (definition + evidence bundle + output requirements) is
    byte-identical across every run of a given assessment, so it forms a stable,
    cacheable prompt prefix: OpenAI caches it automatically, and the Anthropic path
    marks it with ``cache_control`` (see ``run_assessment_*``). Only the dynamic
    suffix — the run number — changes per run, and it is placed last so it never
    invalidates the cached prefix. Caching is a prefix match, so the run number must
    not appear before the evidence bundle.
    """
    static_prefix = f"""
Perform an Open Traceability Assessment of the project/report below.

Definition source URL:
{definition_url}

Open Traceability definition text:
{definition_text}

Project/report URL:
{project_url}

Evidence bundle:
{evidence_bundle}

Output requirements:
- Score stages 1-6 independently from 0 to 100.
- Treat this as an independent run; do not try to match imagined prior runs.
- Leave total_score and total_score_derivation null; the runner computes the total locally.
- Provide a single-paragraph summary.
- Include limitations, especially where the evidence bundle is incomplete.
""".strip()

    dynamic_suffix = f"This is assessment run {run_number} of {runs}."

    return static_prefix, dynamic_suffix


# -----------------------------
# Model calls
# -----------------------------

def finalize_run(
    parsed: AssessmentRun,
    *,
    run_number: int,
    project_url: str,
    model: str,
    include_total: bool,
) -> AssessmentRun:
    """Apply run metadata, model attribution, and total-score behavior locally.

    Shared across providers so the score/total semantics are identical no matter
    which model produced the assessment.
    """
    parsed.run_number = run_number
    parsed.project_url = project_url
    parsed.model_name = model

    if include_total:
        stage_scores = [stage.score for stage in parsed.stages]
        computed_total = round(statistics.mean(stage_scores))
        parsed.total_score = computed_total
        parsed.total_score_derivation = (
            f"Computed locally as round(mean({stage_scores})) = {computed_total}."
        )
    else:
        parsed.total_score = None
        parsed.total_score_derivation = None

    return parsed


def run_assessment_openai(
    client: "OpenAI",
    *,
    model: str,
    reasoning_effort: str,
    static_prefix: str,
    dynamic_suffix: str,
) -> AssessmentRun:
    # The system prompt and static prefix are identical across every run, so OpenAI's
    # automatic prefix caching reuses them; the per-run suffix is kept last so it
    # never invalidates that cached prefix.
    kwargs = {
        "model": model,
        "input": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{static_prefix}\n\n{dynamic_suffix}"},
        ],
        "text_format": AssessmentRun,
    }
    if reasoning_effort != "none":
        kwargs["reasoning"] = {"effort": reasoning_effort}

    response = client.responses.parse(**kwargs)
    return response.output_parsed


def run_assessment_anthropic(
    client,
    *,
    model: str,
    reasoning_effort: str,
    static_prefix: str,
    dynamic_suffix: str,
) -> AssessmentRun:
    # Caching is a prefix match in render order tools -> system -> messages, so the
    # cache_control breakpoint on the static prefix block caches the system prompt and
    # the (large) evidence bundle together. Cache reads bill at ~0.1x, so every run
    # after the first reuses that prefix for ~90% less input cost. The per-run suffix
    # is a separate, uncached block placed after the breakpoint. The evidence bundle is
    # well above Opus's 4096-token minimum cacheable prefix.
    kwargs = {
        "model": model,
        "max_tokens": 16000,
        "system": SYSTEM_PROMPT,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": static_prefix,
                        "cache_control": {"type": "ephemeral"},
                    },
                    {"type": "text", "text": dynamic_suffix},
                ],
            }
        ],
        "output_format": AssessmentRun,
    }
    # The Anthropic equivalent of OpenAI's reasoning effort is adaptive thinking
    # combined with the effort parameter.
    if reasoning_effort != "none":
        kwargs["thinking"] = {"type": "adaptive"}
        kwargs["output_config"] = {"effort": reasoning_effort}

    response = client.messages.parse(**kwargs)
    return response.parsed_output


def run_assessment(
    *,
    provider: str,
    openai_client,
    anthropic_client,
    model: str,
    reasoning_effort: str,
    run_number: int,
    runs: int,
    project_url: str,
    definition_url: str,
    definition_text: str,
    evidence_bundle: str,
    include_total: bool,
) -> AssessmentRun:
    static_prefix, dynamic_suffix = build_user_prompt(
        run_number=run_number,
        runs=runs,
        project_url=project_url,
        definition_url=definition_url,
        definition_text=definition_text,
        evidence_bundle=evidence_bundle,
    )

    if provider == "anthropic":
        parsed = run_assessment_anthropic(
            anthropic_client,
            model=model,
            reasoning_effort=reasoning_effort,
            static_prefix=static_prefix,
            dynamic_suffix=dynamic_suffix,
        )
    else:
        parsed = run_assessment_openai(
            openai_client,
            model=model,
            reasoning_effort=reasoning_effort,
            static_prefix=static_prefix,
            dynamic_suffix=dynamic_suffix,
        )

    return finalize_run(
        parsed,
        run_number=run_number,
        project_url=project_url,
        model=model,
        include_total=include_total,
    )


# -----------------------------
# Reporting
# -----------------------------

def slugify(value: str, fallback: str = "project") -> str:
    """Turn an arbitrary string into a lowercase, filesystem-safe slug."""
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return slug or fallback


def model_to_dict(model_obj: BaseModel) -> dict:
    if hasattr(model_obj, "model_dump"):
        return model_obj.model_dump()
    return model_obj.dict()


def stage_by_number(run: AssessmentRun, stage_number: int) -> StageAssessment:
    matches = [stage for stage in run.stages if stage.stage == stage_number]
    if not matches:
        raise ValueError(f"Run {run.run_number} missing stage {stage_number}")
    return matches[0]


def md_escape(value: object) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", " ").strip()


def normalize_url(url: str) -> str:
    """Normalize a URL for comparison against the collected evidence URLs."""
    return url.strip().rstrip("/")


def consolidate_references(
    runs: list[AssessmentRun], stage_number: int, evidence_urls: set[str]
) -> list[dict]:
    """Collect every reference cited for a stage across all runs, deduplicated by URL.

    Returns one entry per unique URL with the runs that cited it, sorted by how many
    runs cited it (consensus first), then by first appearance. Each entry is marked
    ``verified`` when its URL was part of the collected evidence bundle, so references
    the model may have invented can be flagged in the report.
    """
    by_url: dict[str, dict] = {}
    order: list[str] = []
    for run in runs:
        stage = stage_by_number(run, stage_number)
        for ref in stage.references:
            key = ref.url.strip() or ref.label.strip()
            if key not in by_url:
                by_url[key] = {
                    "label": ref.label,
                    "url": ref.url,
                    "finding": ref.quote_or_finding,
                    "verified": normalize_url(ref.url) in evidence_urls,
                    "runs": [],
                }
                order.append(key)
            if run.run_number not in by_url[key]["runs"]:
                by_url[key]["runs"].append(run.run_number)
    items = [by_url[key] for key in order]
    items.sort(key=lambda entry: len(entry["runs"]), reverse=True)
    return items


def uncertainty_distribution(runs: list[AssessmentRun], stage_number: int) -> tuple[str, dict[str, int]]:
    """Return the modal uncertainty level and the level counts for a stage across runs."""
    counts = {"low": 0, "medium": 0, "high": 0}
    for run in runs:
        level = stage_by_number(run, stage_number).uncertainty
        if level in counts:
            counts[level] += 1
    modal = max(counts, key=lambda level: counts[level])
    return modal, counts


def consolidate_limitations(runs: list[AssessmentRun]) -> list[str]:
    """Collect limitations across all runs, deduplicated by normalized text."""
    seen: dict[str, str] = {}
    order: list[str] = []
    for run in runs:
        for limitation in run.limitations:
            norm = re.sub(r"\s+", " ", limitation).strip().lower()
            if norm and norm not in seen:
                seen[norm] = limitation.strip()
                order.append(norm)
    return [seen[norm] for norm in order]


def models_with_runs(runs: list[AssessmentRun]) -> list[tuple[str, list[int]]]:
    """Return the distinct models used, in first-seen order, each with its run numbers."""
    mapping: dict[str, list[int]] = {}
    order: list[str] = []
    for run in runs:
        model = run.model_name or "unknown"
        if model not in mapping:
            mapping[model] = []
            order.append(model)
        mapping[model].append(run.run_number)
    return [(model, mapping[model]) for model in order]


def format_run_numbers(numbers: list[int]) -> str:
    """Compress a list of run numbers into compact ranges, e.g. [1,2,3,5] -> '1–3, 5'."""
    numbers = sorted(numbers)
    ranges: list[tuple[int, int]] = []
    start = prev = numbers[0]
    for number in numbers[1:]:
        if number == prev + 1:
            prev = number
        else:
            ranges.append((start, prev))
            start = prev = number
    ranges.append((start, prev))
    return ", ".join(str(a) if a == b else f"{a}–{b}" for a, b in ranges)


def make_final_summary(runs: list[AssessmentRun], include_total: bool) -> str:
    stage_avgs = {}
    for stage_number in range(1, 7):
        scores = [stage_by_number(run, stage_number).score for run in runs]
        name = stage_by_number(runs[0], stage_number).stage_name
        stage_avgs[stage_number] = (name, statistics.mean(scores))

    strongest = max(stage_avgs.items(), key=lambda item: item[1][1])
    weakest = min(stage_avgs.items(), key=lambda item: item[1][1])

    total_text = ""
    if include_total:
        totals = [run.total_score for run in runs if run.total_score is not None]
        if totals:
            total_text = f" The average total score across runs is {statistics.mean(totals):.1f}."

    return (
        f"Across {len(runs)} independent assessment runs, the project appears strongest on "
        f"{strongest[1][0]} with an average score of {strongest[1][1]:.1f}, and weakest on "
        f"{weakest[1][0]} with an average score of {weakest[1][1]:.1f}.{total_text} "
        f"The scores should be interpreted as evidence-bundle-based traceability estimates rather than scientific validation: "
        f"high scores indicate externally inspectable artifacts and linkages, while lower scores indicate missing, implicit, "
        f"or insufficiently versioned evidence in the collected material."
    )


def host_of(url: str) -> str:
    """Return a lowercased hostname for grouping followed sources, or '' if unparseable."""
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return ""


def write_markdown_report(
    runs: list[AssessmentRun],
    *,
    output_path: Path,
    project_url: str,
    definition_url: str,
    include_total: bool,
    evidence_items: list[EvidenceItem],
) -> None:
    model_runs = models_with_runs(runs)
    evidence_urls = {normalize_url(item.url) for item in evidence_items}

    lines: list[str] = []
    lines.append("# Open Traceability Assessment Report")
    lines.append("")
    lines.append(f"- Project/report URL: {project_url}")
    lines.append(f"- Assessment definition URL: {definition_url}")
    if len(model_runs) == 1:
        lines.append(f"- Model: {model_runs[0][0]}")
    else:
        joined = "; ".join(
            f"{model} (runs {format_run_numbers(numbers)})" for model, numbers in model_runs
        )
        lines.append(f"- Models: {joined}")
    lines.append(f"- Number of runs: {len(runs)}")
    lines.append("")

    lines.append("## Final single-paragraph summary")
    lines.append("")
    lines.append(make_final_summary(runs, include_total=include_total))
    lines.append("")

    lines.append("## Score table across runs")
    lines.append("")

    header = ["Stage", "Stage name"] + [f"Run {run.run_number}" for run in runs] + ["Average", "Std dev"]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * len(header)) + " |")

    for stage_number in range(1, 7):
        stages = [stage_by_number(run, stage_number) for run in runs]
        scores = [stage.score for stage in stages]
        avg = statistics.mean(scores)
        std = statistics.pstdev(scores) if len(scores) > 1 else 0.0

        row = [
            str(stage_number),
            stages[0].stage_name,
            *[str(score) for score in scores],
            f"{avg:.1f}",
            f"{std:.1f}",
        ]
        lines.append("| " + " | ".join(md_escape(cell) for cell in row) + " |")

    if len(model_runs) > 1:
        lines.append("")
        lines.append("## Average score by model")
        lines.append("")
        header = ["Stage", "Stage name"] + [model for model, _ in model_runs]
        lines.append("| " + " | ".join(header) + " |")
        lines.append("| " + " | ".join(["---"] * len(header)) + " |")
        for stage_number in range(1, 7):
            stage_name = stage_by_number(runs[0], stage_number).stage_name
            row = [str(stage_number), stage_name]
            for model, _ in model_runs:
                model_scores = [
                    stage_by_number(run, stage_number).score
                    for run in runs
                    if (run.model_name or "unknown") == model
                ]
                row.append(f"{statistics.mean(model_scores):.1f}" if model_scores else "—")
            lines.append("| " + " | ".join(md_escape(cell) for cell in row) + " |")

    if include_total:
        totals = [run.total_score for run in runs if run.total_score is not None]
        if totals:
            avg = statistics.mean(totals)
            std = statistics.pstdev(totals) if len(totals) > 1 else 0.0
            lines.append("")
            lines.append("## Total score")
            lines.append("")
            lines.append("| Run | Total score |")
            lines.append("| --- | ---: |")
            for run in runs:
                lines.append(f"| {run.run_number} | {run.total_score} |")
            lines.append("")
            lines.append(f"Average total score: **{avg:.1f}**; population standard deviation: **{std:.1f}**.")
            lines.append("")

    lines.append("## Sources followed during the assessment")
    lines.append("")
    lines.append(
        "Every URL that was actually fetched and supplied to the model as evidence. This "
        "covers the project repository, its GitHub namespace, and each individual file, "
        "documentation page, or linked resource that was followed. Scores and references "
        "below are derived only from these sources."
    )
    lines.append("")
    lines.append(f"- Project/report URL followed: [{md_escape(project_url)}]({md_escape(project_url)})")
    lines.append(
        f"- Assessment definition URL followed: "
        f"[{md_escape(definition_url)}]({md_escape(definition_url)})"
    )
    lines.append("")

    # Group the fetched evidence artifacts by host so repositories, raw-content hosts,
    # GitHub namespaces, and any external linked data are clearly separated.
    by_host: dict[str, list[EvidenceItem]] = {}
    host_order: list[str] = []
    for item in evidence_items:
        host = host_of(item.url) or "other"
        if host not in by_host:
            by_host[host] = []
            host_order.append(host)
        by_host[host].append(item)

    lines.append(
        f"A total of {len(evidence_items)} source artifact(s) were followed across "
        f"{len(host_order)} host(s)."
    )
    lines.append("")
    for host in host_order:
        lines.append(f"### {host}")
        lines.append("")
        for item in by_host[host]:
            label = md_escape(item.label)
            url = md_escape(item.url)
            lines.append(f"- [{label}]({url})")
        lines.append("")

    lines.append("## Consolidated references by stage")
    lines.append("")
    lines.append(
        "References cited across all runs, deduplicated by URL. The runs that cited each "
        "reference are noted in parentheses; references cited by more runs appear first. "
        "References marked ⚠️ point to a URL that was not part of the collected evidence "
        "bundle and could not be verified (the model may have introduced them)."
    )
    lines.append("")

    run_count = len(runs)
    for stage_number in range(1, 7):
        stages = [stage_by_number(run, stage_number) for run in runs]
        scores = [stage.score for stage in stages]
        avg = statistics.mean(scores)
        modal_uncertainty, uncertainty_counts = uncertainty_distribution(runs, stage_number)
        lines.append(f"### Stage {stage_number}: {stages[0].stage_name}")
        lines.append("")
        lines.append(
            f"Average score {avg:.1f} (range {min(scores)}–{max(scores)} across {run_count} runs). "
            f"Reported uncertainty: mostly {modal_uncertainty} "
            f"(low {uncertainty_counts['low']}, medium {uncertainty_counts['medium']}, "
            f"high {uncertainty_counts['high']})."
        )
        lines.append("")

        references = consolidate_references(runs, stage_number, evidence_urls)
        if not references:
            lines.append("No references supplied across runs.")
            lines.append("")
            continue

        for ref in references:
            label = md_escape(ref["label"])
            url = md_escape(ref["url"])
            finding = md_escape(ref["finding"])
            cited = ", ".join(str(n) for n in sorted(ref["runs"]))
            marker = "" if ref["verified"] else " ⚠️"
            lines.append(
                f"- [{label}]({url}){marker}: {finding} "
                f"_(cited in {len(ref['runs'])}/{run_count} runs: {cited})_"
            )
        lines.append("")

    lines.append("## Consolidated limitations across runs")
    lines.append("")
    limitations = consolidate_limitations(runs)
    if limitations:
        lines.append(
            "Distinct limitations raised by one or more runs (deduplicated):"
        )
        for limitation in limitations:
            lines.append(f"- {limitation}")
        lines.append("")
    else:
        lines.append("No limitations were reported across runs.")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


# -----------------------------
# CLI
# -----------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run an Open Traceability Assessment multiple times with the OpenAI and/or Anthropic API."
    )
    parser.add_argument("--project-url", default=DEFAULT_PROJECT_URL)
    parser.add_argument("--definition-url", default=DEFAULT_DEFINITION_URL)
    parser.add_argument("--runs", type=int, default=3, help="Number of runs per selected provider.")
    parser.add_argument(
        "--provider",
        choices=["openai", "anthropic", "both"],
        default="openai",
        help="Which model provider(s) to assess with. 'both' runs the full set of runs with each.",
    )
    parser.add_argument("--model", default="gpt-5.5", help="OpenAI model id.")
    parser.add_argument("--anthropic-model", default="claude-opus-4-8", help="Anthropic (Claude) model id.")
    parser.add_argument(
        "--reasoning-effort",
        choices=["none", "low", "medium", "high", "xhigh"],
        default="medium",
        help=(
            "Reasoning effort. For OpenAI this maps to the reasoning parameter; for Anthropic it maps to "
            "adaptive thinking plus the effort parameter. Use 'none' to disable."
        ),
    )
    parser.add_argument(
        "--include-total",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Include or omit numeric total assessment scores.",
    )
    parser.add_argument("--output-dir", default="reports")
    parser.add_argument("--out-prefix", default="open_traceability_assessment")
    parser.add_argument("--sleep-seconds", type=float, default=1.0)
    parser.add_argument("--max-evidence-files", type=int, default=60)
    parser.add_argument("--max-file-chars", type=int, default=5_000)
    parser.add_argument("--max-evidence-chars", type=int, default=120_000)
    parser.add_argument("--max-definition-chars", type=int, default=20_000)
    return parser.parse_args()


def build_clients(provider: str) -> tuple[object, object]:
    """Construct the API client(s) needed for the selected provider, importing lazily."""
    openai_client = None
    anthropic_client = None

    if provider in ("openai", "both"):
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not set.")
        from openai import OpenAI

        openai_client = OpenAI()

    if provider in ("anthropic", "both"):
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise RuntimeError("ANTHROPIC_API_KEY is not set.")
        import anthropic

        anthropic_client = anthropic.Anthropic()

    return openai_client, anthropic_client


def main() -> None:
    args = parse_args()

    if args.runs < 1:
        raise ValueError("--runs must be at least 1")

    # (provider, model) pairs to assess with, in order. 'both' runs each provider.
    if args.provider == "openai":
        provider_models = [("openai", args.model)]
    elif args.provider == "anthropic":
        provider_models = [("anthropic", args.anthropic_model)]
    else:
        provider_models = [("openai", args.model), ("anthropic", args.anthropic_model)]

    openai_client, anthropic_client = build_clients(args.provider)

    print(f"Fetching Open Traceability definition from: {args.definition_url}")
    definition_text = fetch_url_text(args.definition_url, max_chars=args.max_definition_chars)

    print(f"Collecting evidence from: {args.project_url}")
    evidence_bundle, evidence_items = collect_evidence(args)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    total_runs = args.runs * len(provider_models)
    runs: list[AssessmentRun] = []
    failures: list[tuple[int, str]] = []
    run_dir: Optional[Path] = None
    json_path: Optional[Path] = None
    md_path: Optional[Path] = None

    run_number = 0
    for provider, model in provider_models:
        for _ in range(args.runs):
            run_number += 1
            print(f"Running assessment {run_number}/{total_runs} ({provider}: {model})...")
            try:
                run = run_assessment(
                    provider=provider,
                    openai_client=openai_client,
                    anthropic_client=anthropic_client,
                    model=model,
                    reasoning_effort=args.reasoning_effort,
                    run_number=run_number,
                    runs=total_runs,
                    project_url=args.project_url,
                    definition_url=args.definition_url,
                    definition_text=definition_text,
                    evidence_bundle=evidence_bundle,
                    include_total=args.include_total,
                )
            except Exception as exc:  # noqa: BLE001 - one failed run must not lose the others
                print(f"  Run {run_number} failed: {exc}")
                failures.append((run_number, str(exc)))
                continue

            runs.append(run)

            # Persist after every successful run so a later failure cannot discard prior work.
            if run_dir is None:
                name_prefix = f"{slugify(run.project_name)}_{args.out_prefix}"
                run_dir = Path(args.output_dir) / f"{timestamp}_{name_prefix}"
                run_dir.mkdir(parents=True, exist_ok=True)
                json_path = run_dir / f"{name_prefix}.runs.json"
                md_path = run_dir / f"{name_prefix}.report.md"

            json_path.write_text(
                json.dumps([model_to_dict(r) for r in runs], indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            print(f"  Saved {len(runs)} run(s) so far to {json_path}")

            if run_number < total_runs and args.sleep_seconds > 0:
                time.sleep(args.sleep_seconds)

    if not runs:
        raise RuntimeError(
            f"All {total_runs} assessment run(s) failed; no report generated. "
            f"Last error: {failures[-1][1] if failures else 'unknown'}"
        )

    write_markdown_report(
        runs,
        output_path=md_path,
        project_url=args.project_url,
        definition_url=args.definition_url,
        include_total=args.include_total,
        evidence_items=evidence_items,
    )

    print(f"Wrote structured run data ({len(runs)} run(s)): {json_path}")
    print(f"Wrote Markdown report: {md_path}")
    if failures:
        failed_numbers = ", ".join(str(number) for number, _ in failures)
        print(f"Note: {len(failures)} run(s) failed and were skipped: {failed_numbers}")


if __name__ == "__main__":
    main()