# /// script
# requires-python = ">=3.13"
# dependencies = [
#   openai>=1.99.0
#   requests>=2.32.0
#   beautifulsoup4>=4.12.0
#   pydantic>=2.8.0
#   pypdf>=4.3.0
#   pyyaml>=6.0
# ]
# ///
"""
Run an Open Traceability Assessment multiple times against an open project,
open-science project, or report URL, then produce JSON and Markdown reports.

Example:
  export OPENAI_API_KEY="sk-..."

  uv run open_traceability_assessment.py \
    --project-url https://github.com/natcap/invest \
    --runs 5 \
    --include-total \
    --out-prefix invest_open_traceability

  uv run open_traceability_assessment.py \
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
import time
from dataclasses import dataclass
from datetime import datetime
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

# Canonical stage names, owned by the runner. The model never outputs stage names
# (or any other runner-owned metadata); finalize_run() fills them in locally so
# every stored run carries identical labels without spending output tokens on them.
STAGE_NAMES: dict[int, str] = {
    1: "Open Input Data and Measurement Evidence",
    2: "Open-Source Models, Methods, and Software",
    3: "Open Execution and Reproducibility",
    4: "Open Community and Review",
    5: "Open Publications and Communication",
    6: "Open Linkage",
}


class EvidenceReference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str = Field(
        description="Short human-readable label for the referenced artifact."
    )
    url: str = Field(
        description="URL of the artifact, page, repository file, issue tracker, paper, docs page, etc."
    )
    quote_or_finding: str = Field(
        description="Brief quote, paraphrase, or concrete observed finding."
    )
    relevance: str = Field(description="Why this reference supports the score.")


# --- Model-facing schemas ---------------------------------------------------
# These contain only the fields the model must actually produce. Runner-owned
# metadata (run number, project URL, model attribution, totals, stage names)
# lives on the storage models below and is applied locally by finalize_run();
# making the model generate it was pure output-token waste.


class StageAssessmentOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stage: int = Field(ge=1, le=6)
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
    uncertainty_reason: str = Field(
        description="One sentence explaining the uncertainty level."
    )
    references: list[EvidenceReference] = Field(
        description="The strongest supporting references for this score, at most 3."
    )


class AssessmentOutput(BaseModel):
    """Full narrative schema, used for the first --full-runs runs per provider."""

    model_config = ConfigDict(extra="forbid")

    project_name: str
    stages: list[StageAssessmentOutput]
    single_paragraph_summary: str
    limitations: list[str]


class SlimStageOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stage: int = Field(ge=1, le=6)
    score: int = Field(ge=0, le=100)
    uncertainty: Literal["low", "medium", "high"] = Field(
        description="Overall confidence in this stage's score given the available evidence."
    )
    reference_urls: list[str] = Field(
        description="URLs from the evidence bundle that most support the score, at most 3."
    )


class SlimAssessmentOutput(BaseModel):
    """Scores-only schema for repeat runs beyond --full-runs.

    Repeat runs exist to measure score variance, which only needs the numbers —
    regenerating the narrative every run multiplied the (expensive) output tokens
    for no analytical gain. Uncertainty and bare reference URLs are kept so the
    report's consensus counting and uncertainty distribution still work.
    """

    model_config = ConfigDict(extra="forbid")

    stages: list[SlimStageOutput]


def output_schema_for(slim: bool) -> type[BaseModel]:
    return SlimAssessmentOutput if slim else AssessmentOutput


# --- Storage models ----------------------------------------------------------
# What lands in the .runs.json file: a model output merged with runner-owned
# metadata and the token usage reported by the provider.


class TokenUsage(BaseModel):
    input_tokens: int = 0
    cached_input_tokens: int = 0  # served from the prompt cache (heavily discounted)
    cache_creation_input_tokens: int = 0  # written to the cache (Anthropic only)
    output_tokens: int = 0
    reasoning_output_tokens: int = 0  # OpenAI reports reasoning separately; Anthropic includes it in output_tokens


class StageAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stage: int
    stage_name: str
    score: int
    score_derivation: str
    uncertainty: Literal["low", "medium", "high"]
    uncertainty_reason: str
    references: list[EvidenceReference]


class AssessmentRun(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_number: int
    project_name: str
    project_url: str
    stages: list[StageAssessment]
    total_score: Optional[int] = None
    total_score_derivation: Optional[str] = None
    single_paragraph_summary: str
    limitations: list[str]
    model_name: Optional[str] = None
    schema_variant: Literal["full", "slim"] = "full"
    usage: Optional[TokenUsage] = None


# Schema for the optional manifest-expansion step (--suggest-references). The model is
# asked to propose ADDITIONAL evidence URLs, grounded in the curated bundle, that a
# curator could add to the manifest. The dimension literals mirror MANIFEST_DIMENSIONS
# (defined further down); keep the two in sync if the canonical keys ever change.
class SuggestedReference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dimension: Literal[
        "open_data",
        "open_software",
        "open_execution",
        "open_community",
        "open_publications",
    ] = Field(
        description="Which Open Traceability dimension (stages 1-5) this URL would strengthen."
    )
    url: str = Field(
        description="A concrete public URL NOT already in the manifest that adds evidence for this dimension."
    )
    title: str = Field(description="Short human-readable title for the suggested artifact.")
    rationale: str = Field(
        description="Why this URL strengthens the dimension's evidence chain and what it is expected to contain."
    )


class ReferenceSuggestions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    suggestions: list[SuggestedReference]


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
                pages.append(
                    f"\n\n--- PDF page {i + 1} ---\n{page.extract_text() or ''}"
                )
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
        bundle_lines.append(
            f"\n\n### Evidence {i}: {item.label}\nURL: {item.url}\n{item.text}"
        )

    return "\n".join(bundle_lines), items


def collect_generic_evidence(
    project_url: str, max_chars: int
) -> tuple[str, list[EvidenceItem]]:
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
# Open Traceability manifest
# -----------------------------

# Canonical manifest keys, in stage order. Stage 6 (Open Linkage) has no key of its
# own: the manifest file *is* the linkage artifact, since it explicitly connects a
# claim to evidence across every other dimension.
MANIFEST_DIMENSIONS: list[tuple[str, int, str]] = [
    ("open_data", 1, "Open Input Data and Measurement Evidence"),
    ("open_software", 2, "Open-Source Models, Methods, and Software"),
    ("open_execution", 3, "Open Execution and Reproducibility"),
    ("open_community", 4, "Open Community and Review"),
    ("open_publications", 5, "Open Publications and Communication"),
]

# Friendly aliases accepted in the manifest and normalized to a canonical key above,
# so the headings from the original sketch (e.g. "Open Access") still parse.
MANIFEST_KEY_ALIASES: dict[str, str] = {
    "opendata": "open_data",
    "open_input_data": "open_data",
    "data": "open_data",
    "software": "open_software",
    "open_source": "open_software",
    "open_models": "open_software",
    "execution": "open_execution",
    "reproducibility": "open_execution",
    "community": "open_community",
    "review": "open_community",
    "open_access": "open_publications",
    "publications": "open_publications",
    "open_publication": "open_publications",
}


def normalize_manifest_key(key: str) -> Optional[str]:
    """Map a user-written section heading to its canonical dimension key, or None."""
    norm = re.sub(r"[^a-z0-9]+", "_", key.strip().lower()).strip("_")
    if norm in {k for k, _, _ in MANIFEST_DIMENSIONS}:
        return norm
    return MANIFEST_KEY_ALIASES.get(norm)


@dataclass
class ManifestEntry:
    url: str
    note: str = ""


@dataclass
class Manifest:
    claim: str
    claim_url: str
    namespaces: list[ManifestEntry]
    source: str
    dimensions: dict[str, list[ManifestEntry]]


def _coerce_entries(raw: object) -> list[ManifestEntry]:
    """Accept either a bare URL string or a mapping with url/note per list item."""
    if isinstance(raw, (str, dict)):
        raw = [raw]
    entries: list[ManifestEntry] = []
    for item in raw or []:
        if isinstance(item, str):
            url, note = item.strip(), ""
        elif isinstance(item, dict):
            url = str(item.get("url", "")).strip()
            note = str(item.get("note", "") or "").strip()
        else:
            continue
        if url:
            entries.append(ManifestEntry(url=url, note=note))
    return entries


def load_manifest(source: str) -> Manifest:
    """Load an Open Traceability manifest from a local path or URL.

    The manifest is a small YAML file that names, per dimension, the URLs a curator
    considers relevant evidence for a claim. Pinning the evidence set like this makes
    every run use the same bundle, which is the whole point: reproducibility.
    """
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("Reading a manifest requires: pip install pyyaml") from exc

    path = Path(source)
    text = path.read_text(encoding="utf-8") if path.exists() else http_get(source).text

    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"Manifest {source} is not a YAML mapping")

    dimensions: dict[str, list[ManifestEntry]] = {}
    for raw_key, raw_value in data.items():
        canonical = normalize_manifest_key(str(raw_key))
        if canonical is not None:
            dimensions.setdefault(canonical, []).extend(_coerce_entries(raw_value))

    if not any(dimensions.values()):
        recognized = ", ".join(k for k, _, _ in MANIFEST_DIMENSIONS)
        raise ValueError(
            f"Manifest {source} contains no URLs under any recognized dimension ({recognized})."
        )

    return Manifest(
        claim=str(data.get("claim", "") or "").strip(),
        claim_url=str(data.get("claim_url", "") or "").strip(),
        namespaces=_coerce_entries(data.get("namespace") or data.get("namespaces")),
        source=source,
        dimensions=dimensions,
    )


def collect_manifest_evidence(
    manifest: Manifest,
    *,
    max_file_chars: int,
    max_total_chars: int,
) -> tuple[str, list[EvidenceItem]]:
    """Fetch every URL named in the manifest, grouped and labelled by dimension."""
    items: list[EvidenceItem] = []

    bundle_lines = [
        "OPEN TRACEABILITY MANIFEST (curated evidence set)",
        f"CLAIM: {manifest.claim or '(not stated)'}",
        f"CLAIM URL: {manifest.claim_url or '(not stated)'}",
        f"MANIFEST SOURCE: {manifest.source}",
        "",
        "The evidence below was curated by a human and grouped by the dimension it was "
        "nominated for. Score each stage independently; a URL listed under one dimension "
        "may still inform another.",
    ]

    total_chars = 0
    evidence_index = 0

    # The namespace (e.g. the GitHub organization home) is general context for every
    # dimension: it shows the organization behind the claim, its other repositories,
    # and governance signals, so it is fetched once up front rather than per stage.
    if manifest.namespaces:
        bundle_lines.append("\n\n## Namespace (organization / project home)")
        for entry in manifest.namespaces:
            if total_chars >= max_total_chars:
                break
            try:
                text = fetch_url_text(entry.url, max_chars=max_file_chars)
            except Exception as exc:
                text = f"[Could not fetch: {exc}]"
            text = compact_text(text, min(max_file_chars, max_total_chars - total_chars))

            evidence_index += 1
            label = "Namespace" + (f" · {entry.note}" if entry.note else "")
            items.append(EvidenceItem(label=label, url=entry.url, text=text))
            total_chars += len(text)

            note_line = f" (curator note: {entry.note})" if entry.note else ""
            bundle_lines.append(f"\n### Evidence {evidence_index}: {entry.url}{note_line}\n{text}")

    for key, stage_number, stage_name in MANIFEST_DIMENSIONS:
        entries = manifest.dimensions.get(key, [])
        bundle_lines.append(f"\n\n## Stage {stage_number}: {stage_name} ({key})")
        if not entries:
            bundle_lines.append("(no sources nominated for this dimension)")
            continue

        for entry in entries:
            if total_chars >= max_total_chars:
                break
            try:
                text = fetch_url_text(entry.url, max_chars=max_file_chars)
            except Exception as exc:
                text = f"[Could not fetch: {exc}]"

            remaining = max_total_chars - total_chars
            text = compact_text(text, min(max_file_chars, remaining))

            evidence_index += 1
            label = f"Stage {stage_number} · {key}" + (f" · {entry.note}" if entry.note else "")
            items.append(EvidenceItem(label=label, url=entry.url, text=text))
            total_chars += len(text)

            note_line = f" (curator note: {entry.note})" if entry.note else ""
            bundle_lines.append(f"\n### Evidence {evidence_index}: {entry.url}{note_line}\n{text}")

    return "\n".join(bundle_lines), items


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

Investigate related and linked projects across Git repositories, URLs, and other referenced documents within the URL starter for the assessment. 
Create a full evidence chain from input data (1) to (5), then use this chain of evidence to create your assessment.
"""


FULL_OUTPUT_RULES = """
Output requirements:
- Score stages 1-6 independently from 0 to 100.
- Treat this as an independent run; do not try to match imagined prior runs.
- For each stage cite at most the 3 strongest references from the evidence bundle.
- Provide a single-paragraph summary.
- Include limitations, especially where the evidence bundle is incomplete.
""".strip()

SLIM_OUTPUT_RULES = """
Output requirements:
- Score stages 1-6 independently from 0 to 100.
- Treat this as an independent run; do not try to match imagined prior runs.
- This is a scores-only run: for each stage return only the score, the uncertainty
  level, and the URLs from the evidence bundle (at most 3) that most support the
  score. Do not write any derivation prose.
""".strip()


def build_user_prompt(
    *,
    run_number: int,
    runs: int,
    project_url: str,
    definition_url: str,
    definition_text: str,
    evidence_bundle: str,
    slim: bool = False,
) -> tuple[str, str, str]:
    """Return ``(shared_core, variant_rules, dynamic_suffix)`` for one assessment run.

    The parts are ordered from most to least stable because prompt caching is a
    prefix match:

    - ``shared_core`` (definition + evidence bundle) is byte-identical across every
      run of an assessment, full or slim, so all runs share one big cached prefix.
    - ``variant_rules`` (the output requirements) differ between the full and slim
      schemas, so they sit after the core on their own cache breakpoint: slim runs
      still reuse the shared-core prefix written by the first full run.
    - ``dynamic_suffix`` (just the run number) changes every run and is placed
      last, after all cache breakpoints.

    Never move per-run varying text ahead of the evidence bundle: caching is a
    prefix match, so that would break the cache for everything after it.
    """
    shared_core = f"""
Perform an Open Traceability Assessment of the project/report below.

Definition source URL:
{definition_url}

Open Traceability definition text:
{definition_text}

Project/report URL:
{project_url}

Evidence bundle:
{evidence_bundle}
""".strip()

    variant_rules = SLIM_OUTPUT_RULES if slim else FULL_OUTPUT_RULES
    dynamic_suffix = f"This is assessment run {run_number} of {runs}."

    return shared_core, variant_rules, dynamic_suffix


# -----------------------------
# Model calls
# -----------------------------


def openai_input(shared_core: str, variant_rules: str, dynamic_suffix: str) -> list[dict]:
    """OpenAI message list; automatic prefix caching reuses the stable leading parts."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"{shared_core}\n\n{variant_rules}\n\n{dynamic_suffix}"},
    ]


def anthropic_message_content(
    shared_core: str, variant_rules: str, dynamic_suffix: str
) -> list[dict]:
    """Anthropic user content with two cache breakpoints.

    Caching is a prefix match in render order tools -> system -> messages. The first
    breakpoint caches the system prompt plus the (large) shared core, so full and
    slim runs share it; the second caches the variant rules, so repeat runs of the
    same variant are fully cached. Cache reads bill at ~0.1x. The per-run suffix
    stays after every breakpoint so it never invalidates them.
    """
    return [
        {
            "type": "text",
            "text": shared_core,
            "cache_control": {"type": "ephemeral"},
        },
        {
            "type": "text",
            "text": variant_rules,
            "cache_control": {"type": "ephemeral"},
        },
        {"type": "text", "text": dynamic_suffix},
    ]


def _usage_field(container: object, key: str) -> int:
    """Read one numeric usage field from an SDK object or a plain dict, default 0."""
    if container is None:
        value = None
    elif isinstance(container, dict):
        value = container.get(key)
    else:
        value = getattr(container, key, None)
    return int(value or 0)


def usage_from_openai(usage: object) -> Optional[TokenUsage]:
    if usage is None:
        return None
    if isinstance(usage, dict):
        input_details = usage.get("input_tokens_details")
        output_details = usage.get("output_tokens_details")
    else:
        input_details = getattr(usage, "input_tokens_details", None)
        output_details = getattr(usage, "output_tokens_details", None)
    return TokenUsage(
        input_tokens=_usage_field(usage, "input_tokens"),
        cached_input_tokens=_usage_field(input_details, "cached_tokens"),
        output_tokens=_usage_field(usage, "output_tokens"),
        reasoning_output_tokens=_usage_field(output_details, "reasoning_tokens"),
    )


def usage_from_anthropic(usage: object) -> Optional[TokenUsage]:
    if usage is None:
        return None
    return TokenUsage(
        input_tokens=_usage_field(usage, "input_tokens"),
        cached_input_tokens=_usage_field(usage, "cache_read_input_tokens"),
        cache_creation_input_tokens=_usage_field(usage, "cache_creation_input_tokens"),
        output_tokens=_usage_field(usage, "output_tokens"),
    )


def format_usage(usage: Optional[TokenUsage]) -> str:
    if usage is None:
        return "usage unavailable"
    return (
        f"input {usage.input_tokens} (cache read {usage.cached_input_tokens}, "
        f"cache write {usage.cache_creation_input_tokens}), "
        f"output {usage.output_tokens} (reasoning {usage.reasoning_output_tokens})"
    )


def finalize_run(
    parsed: AssessmentOutput | SlimAssessmentOutput,
    *,
    run_number: int,
    project_url: str,
    model: str,
    include_total: bool,
    usage: Optional[TokenUsage] = None,
) -> AssessmentRun:
    """Build the stored run from a model output plus runner-owned metadata.

    Run number, project URL, stage names, model attribution, totals, and token
    usage never round-trip through the model. Shared across providers so the
    score/total semantics are identical no matter which model produced the run.
    """
    slim = isinstance(parsed, SlimAssessmentOutput)

    if slim:
        stages = [
            StageAssessment(
                stage=s.stage,
                stage_name=STAGE_NAMES.get(s.stage, f"Stage {s.stage}"),
                score=s.score,
                score_derivation="",
                uncertainty=s.uncertainty,
                uncertainty_reason="",
                references=[
                    EvidenceReference(label=url, url=url, quote_or_finding="", relevance="")
                    for url in s.reference_urls
                ],
            )
            for s in parsed.stages
        ]
        project_name, summary, limitations = "", "", []
    else:
        stages = [
            StageAssessment(
                stage=s.stage,
                stage_name=STAGE_NAMES.get(s.stage, f"Stage {s.stage}"),
                score=s.score,
                score_derivation=s.score_derivation,
                uncertainty=s.uncertainty,
                uncertainty_reason=s.uncertainty_reason,
                references=s.references,
            )
            for s in parsed.stages
        ]
        project_name = parsed.project_name
        summary = parsed.single_paragraph_summary
        limitations = parsed.limitations

    run = AssessmentRun(
        run_number=run_number,
        project_name=project_name,
        project_url=project_url,
        stages=stages,
        single_paragraph_summary=summary,
        limitations=limitations,
        model_name=model,
        schema_variant="slim" if slim else "full",
        usage=usage,
    )

    if include_total:
        stage_scores = [stage.score for stage in run.stages]
        computed_total = round(statistics.mean(stage_scores))
        run.total_score = computed_total
        run.total_score_derivation = (
            f"Computed locally as round(mean({stage_scores})) = {computed_total}."
        )

    return run


def run_assessment_openai(
    client: "OpenAI",
    *,
    model: str,
    reasoning_effort: str,
    output_schema: type[BaseModel],
    shared_core: str,
    variant_rules: str,
    dynamic_suffix: str,
) -> tuple[BaseModel, Optional[TokenUsage]]:
    # The system prompt and shared core are identical across every run, so OpenAI's
    # automatic prefix caching reuses them; the variant rules and per-run suffix are
    # kept last so they never invalidate that cached prefix.
    kwargs = {
        "model": model,
        "input": openai_input(shared_core, variant_rules, dynamic_suffix),
        "text_format": output_schema,
    }
    if reasoning_effort != "none":
        kwargs["reasoning"] = {"effort": reasoning_effort}

    response = client.responses.parse(**kwargs)
    return response.output_parsed, usage_from_openai(getattr(response, "usage", None))


def run_assessment_anthropic(
    client,
    *,
    model: str,
    reasoning_effort: str,
    output_schema: type[BaseModel],
    shared_core: str,
    variant_rules: str,
    dynamic_suffix: str,
) -> tuple[BaseModel, Optional[TokenUsage]]:
    # Cache breakpoints are set inside anthropic_message_content(); the evidence
    # bundle is well above Opus's minimum cacheable prefix.
    kwargs = {
        "model": model,
        "max_tokens": 16000,
        "system": SYSTEM_PROMPT,
        "messages": [
            {
                "role": "user",
                "content": anthropic_message_content(
                    shared_core, variant_rules, dynamic_suffix
                ),
            }
        ],
        "output_format": output_schema,
    }
    # The Anthropic equivalent of OpenAI's reasoning effort is adaptive thinking
    # combined with the effort parameter.
    if reasoning_effort != "none":
        kwargs["thinking"] = {"type": "adaptive"}
        kwargs["output_config"] = {"effort": reasoning_effort}

    response = client.messages.parse(**kwargs)
    return response.parsed_output, usage_from_anthropic(getattr(response, "usage", None))


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
    slim: bool = False,
) -> AssessmentRun:
    shared_core, variant_rules, dynamic_suffix = build_user_prompt(
        run_number=run_number,
        runs=runs,
        project_url=project_url,
        definition_url=definition_url,
        definition_text=definition_text,
        evidence_bundle=evidence_bundle,
        slim=slim,
    )
    output_schema = output_schema_for(slim)

    if provider == "anthropic":
        parsed, usage = run_assessment_anthropic(
            anthropic_client,
            model=model,
            reasoning_effort=reasoning_effort,
            output_schema=output_schema,
            shared_core=shared_core,
            variant_rules=variant_rules,
            dynamic_suffix=dynamic_suffix,
        )
    else:
        parsed, usage = run_assessment_openai(
            openai_client,
            model=model,
            reasoning_effort=reasoning_effort,
            output_schema=output_schema,
            shared_core=shared_core,
            variant_rules=variant_rules,
            dynamic_suffix=dynamic_suffix,
        )

    return finalize_run(
        parsed,
        run_number=run_number,
        project_url=project_url,
        model=model,
        include_total=include_total,
        usage=usage,
    )


# -----------------------------
# Batch mode (--batch)
# -----------------------------
# Both providers' Batch APIs bill all tokens at 50% of the synchronous price. The
# N runs of an assessment are fully independent, so they submit as one batch per
# provider. Trade-offs: results arrive together (no incremental per-run saving)
# and batches can take minutes to hours (up to 24h in the worst case).


@dataclass
class RunSpec:
    run_number: int
    provider: str
    model: str
    slim: bool


def openai_text_format(schema_cls: type[BaseModel]) -> dict:
    """Raw ``text.format`` param for a Pydantic schema.

    Batch request bodies bypass ``responses.parse``, so the strict-schema
    conversion the SDK normally performs is invoked here directly (with a plain
    Pydantic-schema fallback if the private helper moves).
    """
    try:
        from openai.lib._pydantic import to_strict_json_schema

        schema = to_strict_json_schema(schema_cls)
    except Exception:
        schema = schema_cls.model_json_schema()
    return {
        "type": "json_schema",
        "name": schema_cls.__name__,
        "strict": True,
        "schema": schema,
    }


def anthropic_output_format(schema_cls: type[BaseModel]) -> dict:
    """Raw ``output_config.format`` for a Pydantic schema (batches bypass parse())."""
    try:
        from anthropic import transform_schema

        schema = transform_schema(schema_cls)
    except Exception:
        schema = schema_cls.model_json_schema()
    return {"type": "json_schema", "schema": schema}


def _run_number_of(custom_id: str) -> int:
    return int(custom_id.rsplit("-", 1)[1])


def run_batch_openai(
    client,
    specs: list[RunSpec],
    *,
    model: str,
    reasoning_effort: str,
    prompt_parts_for,
    poll_seconds: float,
) -> tuple[dict[int, tuple[BaseModel, Optional[TokenUsage]]], dict[int, str]]:
    """Submit one provider's runs as an OpenAI batch and collect the results."""
    lines = []
    for spec in specs:
        shared_core, variant_rules, dynamic_suffix = prompt_parts_for(spec)
        body = {
            "model": model,
            "input": openai_input(shared_core, variant_rules, dynamic_suffix),
            "text": {"format": openai_text_format(output_schema_for(spec.slim))},
        }
        if reasoning_effort != "none":
            body["reasoning"] = {"effort": reasoning_effort}
        lines.append(
            json.dumps(
                {
                    "custom_id": f"run-{spec.run_number}",
                    "method": "POST",
                    "url": "/v1/responses",
                    "body": body,
                },
                ensure_ascii=False,
            )
        )

    batch_file = client.files.create(
        file=("assessment_batch.jsonl", "\n".join(lines).encode("utf-8")),
        purpose="batch",
    )
    batch = client.batches.create(
        input_file_id=batch_file.id,
        endpoint="/v1/responses",
        completion_window="24h",
    )
    print(f"  OpenAI batch {batch.id} submitted ({len(specs)} run(s)).")

    terminal = {"completed", "failed", "expired", "cancelled"}
    while batch.status not in terminal:
        time.sleep(poll_seconds)
        batch = client.batches.retrieve(batch.id)
        counts = getattr(batch, "request_counts", None)
        completed = getattr(counts, "completed", "?") if counts else "?"
        print(f"  OpenAI batch status: {batch.status} ({completed}/{len(specs)} completed)")

    outputs: dict[int, tuple[BaseModel, Optional[TokenUsage]]] = {}
    errors: dict[int, str] = {}
    spec_by_run = {spec.run_number: spec for spec in specs}

    result_file_ids = [
        file_id
        for file_id in (batch.output_file_id, getattr(batch, "error_file_id", None))
        if file_id
    ]
    if not result_file_ids:
        raise RuntimeError(f"OpenAI batch {batch.id} ended with status {batch.status} and no result files")

    for file_id in result_file_ids:
        for raw_line in client.files.content(file_id).text.splitlines():
            if not raw_line.strip():
                continue
            record = json.loads(raw_line)
            run_number = _run_number_of(record["custom_id"])
            response = record.get("response") or {}
            body = response.get("body") or {}
            if record.get("error") or response.get("status_code") != 200:
                errors[run_number] = json.dumps(
                    record.get("error") or body.get("error") or {"status_code": response.get("status_code")}
                )
                continue
            text = "".join(
                content.get("text", "")
                for item in body.get("output", [])
                if item.get("type") == "message"
                for content in item.get("content", [])
                if content.get("type") == "output_text"
            )
            try:
                parsed = output_schema_for(spec_by_run[run_number].slim).model_validate_json(text)
            except Exception as exc:
                errors[run_number] = f"Could not parse structured output: {exc}"
                continue
            outputs[run_number] = (parsed, usage_from_openai(body.get("usage")))

    for spec in specs:
        if spec.run_number not in outputs and spec.run_number not in errors:
            errors[spec.run_number] = f"No result returned (batch status {batch.status})"

    return outputs, errors


def run_batch_anthropic(
    client,
    specs: list[RunSpec],
    *,
    model: str,
    reasoning_effort: str,
    prompt_parts_for,
    poll_seconds: float,
) -> tuple[dict[int, tuple[BaseModel, Optional[TokenUsage]]], dict[int, str]]:
    """Submit one provider's runs as an Anthropic Message Batch and collect the results."""
    requests_payload = []
    for spec in specs:
        shared_core, variant_rules, dynamic_suffix = prompt_parts_for(spec)
        # Prompt caching also applies inside batches (best effort), so the same
        # cache breakpoints used in the synchronous path are kept here.
        params = {
            "model": model,
            "max_tokens": 16000,
            "system": SYSTEM_PROMPT,
            "messages": [
                {
                    "role": "user",
                    "content": anthropic_message_content(
                        shared_core, variant_rules, dynamic_suffix
                    ),
                }
            ],
            "output_config": {
                "format": anthropic_output_format(output_schema_for(spec.slim))
            },
        }
        if reasoning_effort != "none":
            params["thinking"] = {"type": "adaptive"}
            params["output_config"]["effort"] = reasoning_effort
        requests_payload.append(
            {"custom_id": f"run-{spec.run_number}", "params": params}
        )

    batch = client.messages.batches.create(requests=requests_payload)
    print(f"  Anthropic batch {batch.id} submitted ({len(specs)} run(s)).")

    while batch.processing_status != "ended":
        time.sleep(poll_seconds)
        batch = client.messages.batches.retrieve(batch.id)
        counts = batch.request_counts
        print(
            f"  Anthropic batch status: {batch.processing_status} "
            f"(succeeded {counts.succeeded}, errored {counts.errored}, "
            f"processing {counts.processing})"
        )

    outputs: dict[int, tuple[BaseModel, Optional[TokenUsage]]] = {}
    errors: dict[int, str] = {}
    spec_by_run = {spec.run_number: spec for spec in specs}

    for result in client.messages.batches.results(batch.id):
        run_number = _run_number_of(result.custom_id)
        if result.result.type != "succeeded":
            detail = getattr(getattr(result.result, "error", None), "type", "")
            errors[run_number] = f"Batch item {result.result.type}" + (
                f": {detail}" if detail else ""
            )
            continue
        message = result.result.message
        text = next((b.text for b in message.content if b.type == "text"), "")
        try:
            parsed = output_schema_for(spec_by_run[run_number].slim).model_validate_json(text)
        except Exception as exc:
            errors[run_number] = f"Could not parse structured output: {exc}"
            continue
        outputs[run_number] = (parsed, usage_from_anthropic(message.usage))

    for spec in specs:
        if spec.run_number not in outputs and spec.run_number not in errors:
            errors[spec.run_number] = "No result returned for this run"

    return outputs, errors


# -----------------------------
# Manifest expansion (--suggest-references)
# -----------------------------

SUGGESTION_SYSTEM_PROMPT = """You are an expert research librarian for open science, \
open-source software, and environmental evidence chains.

You are given a curated Open Traceability manifest (a human-nominated set of evidence \
URLs grouped by dimension) and the fetched text of those sources. Propose ADDITIONAL \
public references that a curator could add to strengthen the evidence chain.

Rules:
- Only suggest URLs that are NOT already present in the manifest.
- Ground every suggestion in what the supplied evidence references, links to, or \
implies; do not invent URLs you are not confident actually exist.
- Prefer concrete, durable, directly-citable artifacts: datasets and data portals, \
source repositories, CI/workflow configs, peer-reviewed papers and DOIs, documentation \
pages, release pages, and public issue trackers.
- Assign each suggestion to exactly one dimension: the one it most strengthens.
- If you cannot responsibly suggest anything for a dimension, suggest nothing for it \
rather than guessing.
- A human will review and verify every suggestion, so be precise about what each URL \
is expected to contain and why it matters.
"""


def build_suggestion_prompt(
    *,
    manifest: "Manifest",
    definition_url: str,
    definition_text: str,
    evidence_bundle: str,
) -> str:
    """Prompt for the expansion step: lists what is already pinned, then asks for more."""
    existing_lines = []
    for key, stage_number, stage_name in MANIFEST_DIMENSIONS:
        entries = manifest.dimensions.get(key, [])
        urls = "\n".join(f"  - {e.url}" for e in entries) or "  (none nominated yet)"
        existing_lines.append(f"Stage {stage_number} — {stage_name} ({key}):\n{urls}")
    existing = "\n".join(existing_lines)

    return f"""
Suggest additional Open Traceability evidence URLs for the claim below.

Definition source URL:
{definition_url}

Open Traceability definition text:
{definition_text}

CLAIM: {manifest.claim or '(not stated)'}
CLAIM URL: {manifest.claim_url or '(not stated)'}

URLs already pinned in the manifest (do NOT repeat these):
{existing}

Evidence bundle (fetched text of the pinned URLs):
{evidence_bundle}

Return only genuinely new, concrete, publicly reachable URLs, each assigned to the one
dimension it most strengthens, with a short title and a rationale.
""".strip()


def suggest_references(
    *,
    provider: str,
    openai_client,
    anthropic_client,
    model: str,
    reasoning_effort: str,
    manifest: "Manifest",
    definition_url: str,
    definition_text: str,
    evidence_bundle: str,
) -> ReferenceSuggestions:
    """Ask one model for additional evidence URLs, validated against ReferenceSuggestions."""
    prompt = build_suggestion_prompt(
        manifest=manifest,
        definition_url=definition_url,
        definition_text=definition_text,
        evidence_bundle=evidence_bundle,
    )

    if provider == "anthropic":
        kwargs = {
            "model": model,
            "max_tokens": 8000,
            "system": SUGGESTION_SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": prompt}],
            "output_format": ReferenceSuggestions,
        }
        if reasoning_effort != "none":
            kwargs["thinking"] = {"type": "adaptive"}
            kwargs["output_config"] = {"effort": reasoning_effort}
        return anthropic_client.messages.parse(**kwargs).parsed_output

    kwargs = {
        "model": model,
        "input": [
            {"role": "system", "content": SUGGESTION_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "text_format": ReferenceSuggestions,
    }
    if reasoning_effort != "none":
        kwargs["reasoning"] = {"effort": reasoning_effort}
    return openai_client.responses.parse(**kwargs).output_parsed


def check_url_reachable(url: str) -> bool:
    """Best-effort liveness probe; http_get raises on 4xx/5xx, so success means reachable."""
    try:
        http_get(url, timeout=15)
        return True
    except Exception:
        return False


def _entry_to_yaml(url: str, note: str) -> object:
    """A manifest item is a bare URL when it has no note, else a {url, note} mapping."""
    return {"url": url, "note": note} if note else url


def write_expanded_manifest(
    *,
    manifest: "Manifest",
    suggestions: ReferenceSuggestions,
    model: str,
    run_dir: Path,
    verify: bool = True,
) -> Path:
    """Write a runnable manifest that merges the curated set with AI-suggested URLs.

    The original entries are preserved verbatim; each suggested entry is appended to its
    dimension with a note that unmistakably attributes it to the model and marks it
    UNVERIFIED, so a human reviewer can see at a glance what the AI added. The producing
    model is also encoded in the filename and an ``ai_expansion`` provenance block.
    """
    import yaml

    by_dim: dict[str, list[SuggestedReference]] = {}
    for s in suggestions.suggestions:
        by_dim.setdefault(s.dimension, []).append(s)

    reachable: dict[str, bool] = {}
    if verify:
        for s in suggestions.suggestions:
            if s.url not in reachable:
                print(f"  Checking suggested URL: {s.url}")
                reachable[s.url] = check_url_reachable(s.url)

    body: dict[str, object] = {}
    if manifest.claim:
        body["claim"] = manifest.claim
    if manifest.claim_url:
        body["claim_url"] = manifest.claim_url
    body["ai_expansion"] = {
        "model": model,
        "generated_from": manifest.source,
        "disclaimer": (
            "Entries whose note begins with [AI-SUGGESTED] were proposed by an LLM and "
            "are UNVERIFIED. Review each one before relying on it."
        ),
    }
    if manifest.namespaces:
        ns = [_entry_to_yaml(e.url, e.note) for e in manifest.namespaces]
        body["namespace"] = ns[0] if len(ns) == 1 else ns

    for key, _stage_number, _stage_name in MANIFEST_DIMENSIONS:
        out = [_entry_to_yaml(e.url, e.note) for e in manifest.dimensions.get(key, [])]
        for s in by_dim.get(key, []):
            reach = "yes" if reachable.get(s.url, True) else "no"
            note = (
                f"[AI-SUGGESTED · {model} · UNVERIFIED · reachable={reach}] "
                f"{s.title}: {s.rationale}"
            )
            out.append({"url": s.url, "note": note})
        if out:
            body[key] = out

    header = (
        "# Open Traceability manifest — AI-EXPANDED\n"
        f"# Generated from: {manifest.source}\n"
        f"# Suggestion model: {model}\n"
        "# Entries marked [AI-SUGGESTED] are UNVERIFIED LLM proposals; review before use.\n\n"
    )
    dumped = yaml.safe_dump(body, sort_keys=False, allow_unicode=True, default_flow_style=False)

    stem = Path(manifest.source).name.rsplit(".", 1)[0] or "manifest"
    out_path = run_dir / f"{slugify(stem)}.ai-expanded.{slugify(model)}.yml"
    out_path.write_text(header + dumped, encoding="utf-8")
    return out_path


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


# Human-review gate mirrored from the report's Markdown checkbox. `approved` starts
# false; a human flips it to true after validating every claim against the references.
HUMAN_REVIEW_INSTRUCTIONS = (
    "Validate all claims in this report against the references provided, then review, "
    "edit, and approve its contents. Set approved to true once done."
)


def build_runs_payload(runs: list[AssessmentRun]) -> dict:
    totals = TokenUsage()
    runs_counted = 0
    for run in runs:
        if run.usage is None:
            continue
        runs_counted += 1
        totals.input_tokens += run.usage.input_tokens
        totals.cached_input_tokens += run.usage.cached_input_tokens
        totals.cache_creation_input_tokens += run.usage.cache_creation_input_tokens
        totals.output_tokens += run.usage.output_tokens
        totals.reasoning_output_tokens += run.usage.reasoning_output_tokens

    return {
        "human_review": {
            "approved": False,
            "instructions": HUMAN_REVIEW_INSTRUCTIONS,
        },
        "token_usage": {
            "runs_counted": runs_counted,
            "totals": totals.model_dump(),
        },
        "runs": [model_to_dict(r) for r in runs],
    }


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


def uncertainty_distribution(
    runs: list[AssessmentRun], stage_number: int
) -> tuple[str, dict[str, int]]:
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

    project_name = next((run.project_name for run in runs if run.project_name), "")

    lines: list[str] = []
    if project_name:
        lines.append(f"# Open Traceability Assessment Report: {project_name}")
    else:
        lines.append("# Open Traceability Assessment Report")
    lines.append("")
    lines.append(
        "- [ ] **Human reviewer:** I have validated all claims in this report against the "
        "references provided, and reviewed, edited, and approved its contents."
    )
    lines.append("")
    lines.append(f"- Project/report URL: {project_url}")
    lines.append(f"- Assessment definition URL: {definition_url}")
    if len(model_runs) == 1:
        lines.append(f"- Model: {model_runs[0][0]}")
    else:
        joined = "; ".join(
            f"{model} (runs {format_run_numbers(numbers)})"
            for model, numbers in model_runs
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

    header = (
        ["Stage", "Stage name"]
        + [f"Run {run.run_number}" for run in runs]
        + ["Average", "Std dev"]
    )
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
                row.append(
                    f"{statistics.mean(model_scores):.1f}" if model_scores else "—"
                )
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
            lines.append(
                f"Average total score: **{avg:.1f}**; population standard deviation: **{std:.1f}**."
            )
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
    lines.append(
        f"- Project/report URL followed: [{md_escape(project_url)}]({md_escape(project_url)})"
    )
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
        modal_uncertainty, uncertainty_counts = uncertainty_distribution(
            runs, stage_number
        )
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
            # Slim (scores-only) runs cite bare URLs, so a reference may have no finding.
            finding_part = f": {finding}" if finding else ""
            lines.append(
                f"- [{label}]({url}){marker}{finding_part} "
                f"_(cited in {len(ref['runs'])}/{run_count} runs: {cited})_"
            )
        lines.append("")

    lines.append("## Consolidated limitations across runs")
    lines.append("")
    limitations = consolidate_limitations(runs)
    if limitations:
        lines.append("Distinct limitations raised by one or more runs (deduplicated):")
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
    parser.add_argument(
        "--manifest",
        default=None,
        help=(
            "Path or URL to an Open Traceability manifest (YAML) that pins the evidence "
            "set per dimension. When set, it replaces --project-url crawling so every run "
            "uses the same curated bundle. See examples/open-traceability.yml."
        ),
    )
    parser.add_argument(
        "--suggest-references",
        action="store_true",
        help=(
            "After collecting evidence, ask one model (the first selected provider) to "
            "propose ADDITIONAL evidence URLs and write a runnable, AI-attributed expanded "
            "manifest (<stem>.ai-expanded.<model>.yml) into the report folder. Requires "
            "--manifest. Suggestions are marked UNVERIFIED for human review."
        ),
    )
    parser.add_argument(
        "--suggest-references-provider",
        choices=["openai", "anthropic"],
        default=None,
        help=(
            "Provider for the --suggest-references step. Defaults to the first selected "
            "assessment provider. May differ from --provider (its SDK/key must be available)."
        ),
    )
    parser.add_argument(
        "--suggest-references-model",
        default=None,
        help=(
            "Model id for the --suggest-references step. Defaults to the suggestion "
            "provider's assessment model, so you can expand with a different model than "
            "you score with."
        ),
    )
    parser.add_argument("--definition-url", default=DEFAULT_DEFINITION_URL)
    parser.add_argument(
        "--runs", type=int, default=3, help="Number of runs per selected provider."
    )
    parser.add_argument(
        "--full-runs",
        type=int,
        default=1,
        help=(
            "Per provider, how many runs use the full narrative schema (derivations, "
            "summary, limitations). The remaining runs use a slim scores-only schema "
            "(score, uncertainty, reference URLs) that costs a fraction of the output "
            "tokens — repeat runs exist to measure variance, which only needs the "
            "numbers. Set >= --runs to make every run full (the old behavior)."
        ),
    )
    parser.add_argument(
        "--batch",
        action=argparse.BooleanOptionalAction,
        default=False,
        help=(
            "Submit all runs per provider through the provider's Batch API: every "
            "token bills at 50%% of the synchronous price, but results arrive "
            "together after the batch ends (minutes to hours; incremental per-run "
            "saving is not possible)."
        ),
    )
    parser.add_argument(
        "--batch-poll-seconds",
        type=float,
        default=30.0,
        help="How often to poll batch status when --batch is set.",
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "anthropic", "both"],
        default="openai",
        help="Which model provider(s) to assess with. 'both' runs the full set of runs with each.",
    )
    parser.add_argument("--openai-model", default="gpt-5.5", help="OpenAI model id.")
    parser.add_argument(
        "--anthropic-model",
        default="claude-opus-4-8",
        help="Anthropic (Claude) model id.",
    )
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


def build_clients(providers: set[str]) -> tuple[object, object]:
    """Construct the API client(s) for the given providers, importing each SDK lazily."""
    openai_client = None
    anthropic_client = None

    if "openai" in providers:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not set.")
        from openai import OpenAI

        openai_client = OpenAI()

    if "anthropic" in providers:
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise RuntimeError("ANTHROPIC_API_KEY is not set.")
        import anthropic

        anthropic_client = anthropic.Anthropic()

    return openai_client, anthropic_client


def main() -> None:
    args = parse_args()

    if args.runs < 1:
        raise ValueError("--runs must be at least 1")

    if args.full_runs < 0:
        raise ValueError("--full-runs must be >= 0")

    if args.suggest_references and not args.manifest:
        raise ValueError(
            "--suggest-references expands a curated manifest, so it requires --manifest."
        )

    # (provider, model) pairs to assess with, in order. 'both' runs each provider.
    if args.provider == "openai":
        provider_models = [("openai", args.openai_model)]
    elif args.provider == "anthropic":
        provider_models = [("anthropic", args.anthropic_model)]
    else:
        provider_models = [
            ("openai", args.openai_model),
            ("anthropic", args.anthropic_model),
        ]

    # The suggestion step may use a different provider/model than the assessment, so
    # resolve it up front and make sure both providers' clients (and keys) are available.
    needed_providers = {provider for provider, _ in provider_models}
    sugg_provider = sugg_model = None
    if args.suggest_references:
        sugg_provider = args.suggest_references_provider or provider_models[0][0]
        default_sugg_model = (
            args.anthropic_model if sugg_provider == "anthropic" else args.openai_model
        )
        sugg_model = args.suggest_references_model or default_sugg_model
        needed_providers.add(sugg_provider)

    openai_client, anthropic_client = build_clients(needed_providers)

    print(f"Fetching Open Traceability definition from: {args.definition_url}")
    definition_text = fetch_url_text(
        args.definition_url, max_chars=args.max_definition_chars
    )

    if args.manifest:
        print(f"Loading Open Traceability manifest from: {args.manifest}")
        manifest = load_manifest(args.manifest)
        project_url = manifest.claim_url or args.manifest
        print(f"Collecting curated evidence for claim: {project_url}")
        evidence_bundle, evidence_items = collect_manifest_evidence(
            manifest,
            max_file_chars=args.max_file_chars,
            max_total_chars=args.max_evidence_chars,
        )
    else:
        project_url = args.project_url
        print(f"Collecting evidence from: {project_url}")
        evidence_bundle, evidence_items = collect_evidence(args)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Build the per-run plan up front: the first --full-runs runs per provider use
    # the full narrative schema, the rest the slim scores-only schema.
    run_specs: list[RunSpec] = []
    run_number = 0
    for provider, model in provider_models:
        for index in range(args.runs):
            run_number += 1
            run_specs.append(
                RunSpec(
                    run_number=run_number,
                    provider=provider,
                    model=model,
                    slim=index >= args.full_runs,
                )
            )

    total_runs = len(run_specs)
    runs: list[AssessmentRun] = []
    failures: list[tuple[int, str]] = []
    run_dir: Optional[Path] = None
    json_path: Optional[Path] = None
    md_path: Optional[Path] = None

    def ensure_run_dir(project_name: str) -> None:
        nonlocal run_dir, json_path, md_path
        if run_dir is not None:
            return
        name_prefix = f"{slugify(project_name)}_{args.out_prefix}"
        run_dir = Path(args.output_dir) / f"{timestamp}_{name_prefix}"
        run_dir.mkdir(parents=True, exist_ok=True)
        json_path = run_dir / f"{name_prefix}.runs.json"
        md_path = run_dir / f"{name_prefix}.report.md"

    def save_runs() -> None:
        # Slim runs carry no project name, so take it from the first run that has one.
        ensure_run_dir(next((r.project_name for r in runs if r.project_name), "project"))
        json_path.write_text(
            json.dumps(build_runs_payload(runs), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def prompt_parts_for(spec: RunSpec) -> tuple[str, str, str]:
        return build_user_prompt(
            run_number=spec.run_number,
            runs=total_runs,
            project_url=project_url,
            definition_url=args.definition_url,
            definition_text=definition_text,
            evidence_bundle=evidence_bundle,
            slim=spec.slim,
        )

    if args.batch:
        batch_runners = {"openai": run_batch_openai, "anthropic": run_batch_anthropic}
        clients = {"openai": openai_client, "anthropic": anthropic_client}
        for provider, model in provider_models:
            specs = [s for s in run_specs if s.provider == provider and s.model == model]
            print(f"Submitting {len(specs)} run(s) as one {provider} batch ({model})...")
            try:
                outputs, errors = batch_runners[provider](
                    clients[provider],
                    specs,
                    model=model,
                    reasoning_effort=args.reasoning_effort,
                    prompt_parts_for=prompt_parts_for,
                    poll_seconds=args.batch_poll_seconds,
                )
            except Exception as exc:  # noqa: BLE001 - one provider's batch must not lose the other's
                print(f"  {provider} batch failed: {exc}")
                failures.extend((spec.run_number, str(exc)) for spec in specs)
                continue

            for spec in specs:
                if spec.run_number in outputs:
                    parsed, usage = outputs[spec.run_number]
                    run = finalize_run(
                        parsed,
                        run_number=spec.run_number,
                        project_url=project_url,
                        model=model,
                        include_total=args.include_total,
                        usage=usage,
                    )
                    runs.append(run)
                    print(f"  Run {spec.run_number} succeeded; tokens: {format_usage(usage)}")
                else:
                    message = errors.get(spec.run_number, "unknown batch error")
                    print(f"  Run {spec.run_number} failed: {message}")
                    failures.append((spec.run_number, message))

        runs.sort(key=lambda run: run.run_number)
        failures.sort(key=lambda failure: failure[0])
        if runs:
            save_runs()
            print(f"Saved {len(runs)} run(s) to {json_path}")
    else:
        for spec in run_specs:
            variant = "slim" if spec.slim else "full"
            print(
                f"Running assessment {spec.run_number}/{total_runs} "
                f"({spec.provider}: {spec.model}, {variant} schema)..."
            )
            try:
                run = run_assessment(
                    provider=spec.provider,
                    openai_client=openai_client,
                    anthropic_client=anthropic_client,
                    model=spec.model,
                    reasoning_effort=args.reasoning_effort,
                    run_number=spec.run_number,
                    runs=total_runs,
                    project_url=project_url,
                    definition_url=args.definition_url,
                    definition_text=definition_text,
                    evidence_bundle=evidence_bundle,
                    include_total=args.include_total,
                    slim=spec.slim,
                )
            except Exception as exc:  # noqa: BLE001 - one failed run must not lose the others
                print(f"  Run {spec.run_number} failed: {exc}")
                failures.append((spec.run_number, str(exc)))
                continue

            runs.append(run)
            print(f"  Tokens: {format_usage(run.usage)}")

            # Persist after every successful run so a later failure cannot discard prior work.
            save_runs()
            print(f"  Saved {len(runs)} run(s) so far to {json_path}")

            if spec.run_number < total_runs and args.sleep_seconds > 0:
                time.sleep(args.sleep_seconds)

    # Optional manifest expansion: ask one model for additional evidence URLs and write
    # an AI-attributed, human-reviewable manifest. Done independently of assessment
    # success so the suggestions survive even if every assessment run failed.
    if args.suggest_references:
        print(f"Suggesting additional references ({sugg_provider}: {sugg_model})...")
        try:
            suggestions = suggest_references(
                provider=sugg_provider,
                openai_client=openai_client,
                anthropic_client=anthropic_client,
                model=sugg_model,
                reasoning_effort=args.reasoning_effort,
                manifest=manifest,
                definition_url=args.definition_url,
                definition_text=definition_text,
                evidence_bundle=evidence_bundle,
            )
        except Exception as exc:  # noqa: BLE001 - suggestion failure must not lose the report
            print(f"  Reference suggestion failed: {exc}")
            suggestions = None

        if suggestions is not None and suggestions.suggestions:
            ensure_run_dir(manifest.claim or "project")
            expanded_path = write_expanded_manifest(
                manifest=manifest,
                suggestions=suggestions,
                model=sugg_model,
                run_dir=run_dir,
            )
            print(
                f"  {len(suggestions.suggestions)} suggestion(s); "
                f"wrote AI-expanded manifest: {expanded_path}"
            )
        elif suggestions is not None:
            print("  Model suggested no additional references.")

    if not runs:
        raise RuntimeError(
            f"All {total_runs} assessment run(s) failed; no report generated. "
            f"Last error: {failures[-1][1] if failures else 'unknown'}"
        )

    write_markdown_report(
        runs,
        output_path=md_path,
        project_url=project_url,
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
