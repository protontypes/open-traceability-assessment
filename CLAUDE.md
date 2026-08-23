# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A single-file CLI (`open_traceability_assessment.py`) that runs an **Open Traceability Assessment**: it fetches a project's evidence (GitHub repo, web page, or PDF), bundles it, and asks an LLM (OpenAI and/or Anthropic) to score six traceability dimensions 0–100, repeated over multiple runs to expose model variance. Output is a structured JSON file plus a Markdown report, written into a timestamped per-run folder under `reports/`.

The whole program lives in `open_traceability_assessment.py`; there is no package structure, test suite, or build step.

## Commands

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # NOTE: also `pip install anthropic>=0.69.0` for --provider anthropic/both

# Run (requires OPENAI_API_KEY and/or ANTHROPIC_API_KEY in the environment)
python open_traceability_assessment.py --project-url https://github.com/natcap/invest --runs 5 --include-total --out-prefix invest

# Compare both providers in one report (--runs applies per provider)
python open_traceability_assessment.py --project-url <url> --provider both --openai-model gpt-5.5 --anthropic-model claude-opus-4-8

# Token-efficiency knobs: --full-runs N (full narrative schema for the first N runs
# per provider, slim scores-only schema for the rest; default 1) and --batch
# (submit runs through the providers' Batch APIs at 50% token price, results async)
```

There are no tests or linters configured. To smoke-test a change, run against a small repo with `--runs 1`. Each real run sends a large evidence bundle and can cost up to ~$1.

## Architecture

The program is a linear pipeline in `main()`; understanding these stages is the key to the file:

1. **Evidence collection** has two entry points, both returning the same `(evidence_bundle string, list[EvidenceItem])` pair (the bundle goes to the model; the items are used later to verify the model's cited URLs):
   - **Crawled** (default, `collect_evidence`) branches on URL type:
     - GitHub URLs → `collect_github_evidence`: hits the GitHub API for repo metadata + the recursive file tree, filters paths through `IMPORTANT_FILE_PATTERNS` (README, LICENSE, CITATION, CI workflows, docs, etc.), sorts shallow-first, and fetches each via `raw.githubusercontent.com`. Bounded by `--max-evidence-files`, `--max-file-chars`, `--max-evidence-chars`.
     - Everything else → `collect_generic_evidence` → `fetch_url_text`, which handles HTML (BeautifulSoup text extraction), PDF (pypdf), and a HackMD `/download` special case (`candidate_text_urls`).
   - **Curated** (`--manifest`, `load_manifest` + `collect_manifest_evidence`): reads a YAML Open Traceability manifest (local path or URL) that pins the exact evidence URLs per dimension, then fetches each and builds a bundle grouped/labelled by stage. This makes runs reproducible (same bundle every time) and lets evidence include artifacts a crawl can't reach. Manifest keys map to stages 1–5 via `MANIFEST_DIMENSIONS` (+ aliases in `MANIFEST_KEY_ALIASES`, e.g. `open_access`→`open_publications`); there is intentionally no stage-6 key because the manifest file *is* the Open Linkage artifact. An optional top-level `namespace` (org/project home, single URL or list) is fetched once as cross-dimension context. When a manifest is used, `main()` sets the report's `project_url` to the manifest's `claim_url`. `pyyaml` is imported lazily here. Sample: `examples/open-traceability.yml`.

2. **Prompt construction** (`build_user_prompt`) deliberately splits each prompt into three parts ordered from most to least stable: a `shared_core` (definition + evidence bundle — byte-identical across every run, full or slim), `variant_rules` (the output requirements, differing between the full and slim schemas), and a tiny `dynamic_suffix` (just the run number). This ordering is load-bearing for **prompt caching**: OpenAI caches the stable prefix automatically; the Anthropic path puts `cache_control` breakpoints after the core *and* after the variant rules, so slim runs still reuse the big core prefix written by the first full run. Never move per-run varying text ahead of the evidence bundle or you break the cache.

3. **Model call** dispatches by provider (`run_assessment` → `run_assessment_openai` / `run_assessment_anthropic`). Both use the SDK's native structured-output parsing against a **model-facing** Pydantic schema, so the model's output is validated, not hand-parsed, and both return the provider-reported token usage alongside the parsed output. Two schemas exist: `AssessmentOutput` (full narrative) for the first `--full-runs` runs per provider, and `SlimAssessmentOutput` (scores, uncertainty, bare reference URLs) for the remaining runs — repeat runs measure variance, which only needs the numbers, so they skip the expensive prose. `reasoning_effort` maps to OpenAI's `reasoning` param vs. Anthropic's adaptive thinking + effort. With `--batch`, `run_batch_openai` / `run_batch_anthropic` instead submit all of a provider's runs as one Batch API job (50% token price, async results, no incremental saving); the batch bodies build the raw structured-output params (`text.format` / `output_config.format`) that `parse()` would otherwise derive.

4. **`finalize_run`** builds the stored `AssessmentRun` from a model output plus everything runner-owned: run metadata, `model_name`, canonical `stage_name`s (`STAGE_NAMES`), token `usage`, the `schema_variant` marker, and `total_score` as the rounded mean of stage scores. The model-facing schemas contain none of these fields — making the model generate them was output-token waste.

5. **Reporting** (`write_markdown_report` + helpers) aggregates across runs: per-dimension average/std-dev, optional per-model comparison table, and `consolidate_references`, which dedupes cited references by URL and marks any whose URL was **not** in the collected evidence bundle with ⚠️ (a hallucinated-reference guard — this is why `evidence_items` is threaded all the way through).

**Optional manifest expansion** (`--suggest-references`, manifest-only): a side branch off the main pipeline. After evidence collection, `suggest_references` makes one extra model call (its own `SUGGESTION_SYSTEM_PROMPT` + `ReferenceSuggestions` schema, separate from `AssessmentRun` so it doesn't disturb the cached assessment prefix) asking for *additional* evidence URLs grounded in the bundle. `write_expanded_manifest` then merges those into a runnable YAML alongside the curated entries, with AI attribution in three places — filename (`<stem>.ai-expanded.<model>.yml`), an `ai_expansion` provenance block (ignored by `load_manifest` since it's not a recognized key), and a per-entry `[AI-SUGGESTED · <model> · UNVERIFIED · reachable=…]` note (reachability via best-effort `check_url_reachable`). The suggestion provider/model default to the first assessment pair but can be overridden (`--suggest-references-provider/-model`); `build_clients` now takes a **set** of providers so the suggestion provider's client is built even if the assessment didn't use it. Runs independently of assessment success and never aborts the report. The `SuggestedReference.dimension` literals must stay in sync with `MANIFEST_DIMENSIONS`.

## Conventions that matter

- **Provider SDKs are imported lazily** in `build_clients` so users only install the provider they use. `requirements.txt` intentionally omits `anthropic`.
- **Results are written incrementally** (synchronous mode): the JSON is re-saved after every successful run, and one failed run is caught and skipped rather than aborting the batch (see the try/except in `main`). In `--batch` mode results arrive together, so the JSON is written once per completed provider batch.
- **Token usage is recorded**: each stored run carries a `usage` block (input / cached / cache-write / output / reasoning tokens) and `runs.json` has a `token_usage` totals section — check `cached_input_tokens` there to confirm prompt caching is actually hitting.
- **Pydantic models use `extra="forbid"`** — adding a field to the model output means adding it to the schema; the providers enforce the schema strictly.
- Output goes to `reports/<timestamp>_<project-slug>_<out-prefix>/` with `.runs.json` and `.report.md`. Both carry a human-review approval gate (`human_review.approved` / a Markdown checkbox) that starts unapproved by design — this tool assists, it does not certify.
