# Open Traceability Assessment

A Python command-line tool for running repeated **Open Traceability Assessments** against an open-source project, open-science project, report, dashboard, or other public sustainability-related evidence artifact.

The tool uses the OpenAI API to assess how externally inspectable the evidence chain behind a project or claim is. It can run the same assessment multiple times, capture score variation across runs, preserve references used for scoring, show derivations for each score, and produce both structured JSON and a Markdown report.

⚠️ This is a prototype that is still in development and currently relies heavily on LLM-only assessments. The implementation of a more structured, verifiable assessment using standardised data platforms is in development. ⚠️

## Background

Rather than asking whether an environmental statement, insight, report or number is true or false, the Open Traceability Concept asks:

> How open, linked, and externally inspectable is the evidence chain behind a sustainability or environmental claim?

The concept is developed by the [Open Traceability Initiative](https://www.open-traceability-initiative.org/), which describes Open Traceability as the externally inspectable connection between an environmental claim and the specific evidence, methods, assumptions, and publications from which that claim was derived.

The project responds to a common weakness in sustainability decision-making: claims may be presented as evidence-based, but the chain linking evidence to the claim is often difficult to inspect. Data, models, assumptions, workflows, review processes, and publications may exist, but they are not always connected in ways that allow meaningful external scrutiny.

Open Traceability therefore shifts attention from openness of isolated artifacts to the inspectability of the **claim-support chain**. A dataset, repository, report, or paper may be public, but it is only traceable when the links between inputs, methods, execution, review, and outputs are explicit enough for others to examine.

## What this tool does

This repository provides a reusable assessment runner that:

- Fetches an Open Traceability definition and project evidence.
- Supports GitHub repositories, web pages, and PDF reports.
- Runs the assessment multiple independent times.
- Scores six Open Traceability dimensions from 0 to 100.
- Optionally computes an overall total score.
- Captures score derivations for every stage and run.
- Preserves references used by the model for each score.
- Produces a structured JSON file for downstream analysis.
- Produces a Markdown report with tables, references, limitations, and a single-paragraph summary.

The tool is intended as an assessment assistant. It does not prove that a claim is true, unbiased, or scientifically valid. Instead, it helps identify whether the evidence, assumptions, methods, limitations, uncertainty, and possible errors behind a claim can be inspected by others.

## The six Open Traceability dimensions

The assessment uses six dimensions derived from the Open Traceability definition.

### 1. Open Input Data and Measurement Evidence

Assesses whether the relevant inputs are identifiable, documented, attributable, reusable, verifiable, and versioned. Strong traceability means that external actors can inspect where the data came from, how it was collected or produced, how it was processed, what uncertainty or quality controls apply, and under what conditions it can be reused.

### 2. Open-Source Models, Methods, and Software

Assesses whether the analytical logic is visible through code, models, methods, dependencies, documentation, configuration, and licensing. Strong traceability normally requires version-controlled source code, clear methods, dependency information, and a recognized open-source license.

### 3. Open Execution and Reproducibility

Assesses whether workflows, scripts, parameters, computational environments, outputs, and provenance make the path from inputs to outputs inspectable. Strong execution traceability exists when an external actor can understand and, ideally, repeat the computation that produced the result.

### 4. Open Community and Review

Assesses whether critique, issue tracking, review, correction processes, and responses to challenge are visible. Strong review traceability means users can inspect not only the final claim, but also how it was questioned, tested, corrected, or improved.

### 5. Open Publications and Communication

Assesses whether reports, papers, dashboards, policy outputs, or explanatory materials are accessible and clearly documented. Strong publication traceability means public outputs state the claim clearly, describe the methods and evidence base, cite supporting artifacts, and preserve enough context for external scrutiny.

### 6. Open Verifiability / Linkage Quality

Assesses whether the full chain across data, methods, execution, review, and publications is explicit, specific, versioned, and externally verifiable. This dimension is critical because openness without linkage does not produce traceability. Public artifacts are not enough if they cannot be connected to the claim they support.

## Assessment architecture

The broader Open Traceability framework proposes using open digital infrastructure to support assessment, including:

- [OpenAlex](https://openalex.org/) for publication-layer evidence, citation networks, open-access status, licensing signals, and correction or retraction markers.
- [ecosyste.ms](https://ecosyste.ms/) for software metadata, repository health, dependencies, licensing, maintenance, and governance signals.
- [OpenSustain.tech](https://opensustain.tech/) as a catalog of open sustainability technology.
- Large language models as assessment assistants that can identify candidate claims, surface relevant artifacts, classify evidence types, and summarize likely gaps for human review.

This runner implements the LLM-assisted part of that architecture. It collects a bounded evidence bundle and asks the model to produce structured, reference-backed assessments.

## Installation

Create a virtual environment and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Example `requirements.txt`:

```txt
openai>=1.99.0
requests>=2.32.0
beautifulsoup4>=4.12.0
pydantic>=2.8.0
pypdf>=4.3.0
```

## OpenAI API key

Create an API key in the OpenAI Platform, then expose it as an environment variable:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

If you are assessing GitHub repositories and expect to fetch many files, you can also provide a GitHub token to reduce rate-limit issues:

```bash
export GITHUB_TOKEN="your_github_token_here"
```

## Usage

Run the assessment against the default example repository:

```bash
python open_traceability_assessment.py \
  --project-url https://github.com/natcap/invest \
  --runs 5 \
  --include-total \
  --out-prefix invest_open_traceability
```

Run the assessment against another project, report, or web page:

```bash
python open_traceability_assessment.py \
  --project-url https://example.org/report.pdf \
  --runs 3 \
  --include-total \
  --out-prefix example_report_traceability
```

Omit the overall total score while still scoring the six dimensions:

```bash
python open_traceability_assessment.py \
  --project-url https://github.com/natcap/invest \
  --runs 5 \
  --no-include-total
```

Use a different model:

```bash
python open_traceability_assessment.py \
  --project-url https://github.com/natcap/invest \
  --runs 3 \
  --model gpt-5.5 \
  --reasoning-effort medium
```

## Outputs

For an output prefix such as `invest_open_traceability`, the runner writes:

```text
invest_open_traceability.runs.json
invest_open_traceability.report.md
```

The JSON output contains the full structured assessment data for every run, including:

- Run number.
- Project name and URL.
- Six stage scores.
- Score derivations.
- Evidence references.
- Uncertainty notes.
- Optional total score.
- Per-run summary paragraph.
- Limitations.

The Markdown report contains:

- A final single-paragraph summary.
- A score table across runs.
- Average and standard deviation by dimension.
- Optional total score table.
- References and derivations by stage.
- Per-run limitations.

## Scoring guidance

The default scoring scale is:

| Score range | Interpretation |
| --- | --- |
| 0-20 | Little or no public evidence for this dimension |
| 21-40 | Partial, fragmentary, or hard-to-verify evidence |
| 41-60 | Moderate evidence, but important gaps remain |
| 61-80 | Strong public evidence with some limitations |
| 81-100 | Excellent, explicit, versioned, reusable, externally verifiable evidence chain |

Scores should be interpreted as evidence-bundle-based traceability estimates, not as a definitive judgment of scientific truth or project quality.

## Recommended workflow

1. Select a bounded project, report, dashboard, or claim.
2. Run the assessment with at least three independent runs.
3. Inspect the references and derivations, not only the scores.
4. Identify where missing links reduce traceability.
5. Manually validate important findings before publication or decision use.
6. Use the report as a draft traceability profile, not as a final audit.

## Example use cases

Open Traceability can be applied to:

- Open-source sustainability software.
- Scientific reports and assessment outputs.
- Environmental dashboards.
- Climate and energy policy evidence.
- Sustainability claims in journalism.
- Monitoring systems based on geospatial or operational data.
- Research outputs that have been corrected, retracted, or contested.

## Limitations

This tool has important limitations:

- It depends on the evidence it can fetch or is given.
- It may miss relevant artifacts that are not linked from the target URL.
- It cannot independently verify every scientific or technical claim.
- It may over- or under-score dimensions where evidence is ambiguous.
- It should be paired with human review, especially for policy-relevant or high-stakes assessments.
- Repeated runs expose variation, but they do not eliminate model uncertainty.

## Related resources

- [Open Traceability Initiative](https://www.open-traceability-initiative.org/)
- [Open Traceability Definition](https://hackmd.io/BctWeQSETuKNZehHwFnTsw)
- [Technical Foundation: Open Traceability for Sustainability Claims](https://hackmd.io/FQrXd1sbSbyXeSp7vqQSHQ)
- [OpenAlex](https://openalex.org/)
- [ecosyste.ms](https://ecosyste.ms/)
- [OpenSustain.tech](https://opensustain.tech/)

