# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A single-file CLI (`ota.py`) that runs an **Open Traceability Assessment**: it fetches a project's evidence (GitHub repo, web page, or PDF), bundles it, and asks an LLM (OpenAI and/or Anthropic) to score six traceability dimensions 0–100, repeated over multiple runs to expose model variance. Output is a structured JSON file plus a Markdown report, written into a timestamped per-run folder under `reports/`.

The whole program lives in `ota.py`; there is no package structure, test suite, or build step.

## Commands

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # NOTE: also `pip install anthropic>=0.69.0` for --provider anthropic/both

# Run (requires OPENAI_API_KEY and/or ANTHROPIC_API_KEY in the environment)
python ota.py --project-url https://github.com/natcap/invest --runs 5 --include-total --out-prefix invest

# Compare both providers in one report (--runs applies per provider)
python ota.py --project-url <url> --provider both --model gpt-5.5 --anthropic-model claude-opus-4-8
```

There are no tests or linters configured. To smoke-test a change, run against a small repo with `--runs 1`. Each real run sends a large evidence bundle and can cost up to ~$1.

## Architecture

The program is a linear pipeline in `main()`; understanding these stages is the key to the file:

1. **Evidence collection** has two entry points, both returning the same `(evidence_bundle string, list[EvidenceItem])` pair (the bundle goes to the model; the items are used later to verify the model's cited URLs):
   - **Crawled** (default, `collect_evidence`) branches on URL type:
     - GitHub URLs → `collect_github_evidence`: hits the GitHub API for repo metadata + the recursive file tree, filters paths through `IMPORTANT_FILE_PATTERNS` (README, LICENSE, CITATION, CI workflows, docs, etc.), sorts shallow-first, and fetches each via `raw.githubusercontent.com`. Bounded by `--max-evidence-files`, `--max-file-chars`, `--max-evidence-chars`.
     - Everything else → `collect_generic_evidence` → `fetch_url_text`, which handles HTML (BeautifulSoup text extraction), PDF (pypdf), and a HackMD `/download` special case (`candidate_text_urls`).
   - **Curated** (`--manifest`, `load_manifest` + `collect_manifest_evidence`): reads a YAML Open Traceability manifest (local path or URL) that pins the exact evidence URLs per dimension, then fetches each and builds a bundle grouped/labelled by stage. This makes runs reproducible (same bundle every time) and lets evidence include artifacts a crawl can't reach. Manifest keys map to stages 1–5 via `MANIFEST_DIMENSIONS` (+ aliases in `MANIFEST_KEY_ALIASES`, e.g. `open_access`→`open_publications`); there is intentionally no stage-6 key because the manifest file *is* the Open Linkage artifact. An optional top-level `namespace` (org/project home, single URL or list) is fetched once as cross-dimension context. When a manifest is used, `main()` sets the report's `project_url` to the manifest's `claim_url`. `pyyaml` is imported lazily here. Sample: `examples/open-traceability.yml`.

2. **Prompt construction** (`build_user_prompt`) deliberately splits each prompt into a `static_prefix` (definition + evidence bundle + output rules — byte-identical across all runs) and a tiny `dynamic_suffix` (just the run number). This ordering is load-bearing for **prompt caching**: OpenAI caches the prefix automatically; the Anthropic path marks it with `cache_control` ephemeral. Never move per-run varying text ahead of the evidence bundle or you break the cache.

3. **Model call** dispatches by provider (`run_assessment` → `run_assessment_openai` / `run_assessment_anthropic`). Both use the SDK's native structured-output parsing against the `AssessmentRun` Pydantic schema, so the model's output is validated, not hand-parsed. `reasoning_effort` maps to OpenAI's `reasoning` param vs. Anthropic's adaptive thinking + effort.

4. **`finalize_run`** applies provider-independent semantics locally: sets run metadata/`model_name` and computes `total_score` as the rounded mean of stage scores. The schema tells the model to leave `total_score` null — the runner owns it.

5. **Reporting** (`write_markdown_report` + helpers) aggregates across runs: per-dimension average/std-dev, optional per-model comparison table, and `consolidate_references`, which dedupes cited references by URL and marks any whose URL was **not** in the collected evidence bundle with ⚠️ (a hallucinated-reference guard — this is why `evidence_items` is threaded all the way through).

## Conventions that matter

- **Provider SDKs are imported lazily** in `build_clients` so users only install the provider they use. `requirements.txt` intentionally omits `anthropic`.
- **Results are written incrementally**: the JSON is re-saved after every successful run, and one failed run is caught and skipped rather than aborting the batch (see the try/except in `main`).
- **Pydantic models use `extra="forbid"`** — adding a field to the model output means adding it to the schema; the providers enforce the schema strictly.
- Output goes to `reports/<timestamp>_<project-slug>_<out-prefix>/` with `.runs.json` and `.report.md`. Both carry a human-review approval gate (`human_review.approved` / a Markdown checkbox) that starts unapproved by design — this tool assists, it does not certify.
