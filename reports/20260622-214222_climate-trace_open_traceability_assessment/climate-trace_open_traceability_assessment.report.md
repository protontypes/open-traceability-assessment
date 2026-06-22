# Open Traceability Assessment Report: Climate TRACE

- [ ] **Human reviewer:** I have validated all claims in this report against the references provided, and reviewed, edited, and approved its contents.

- Project/report URL: https://climatetrace.org
- Assessment definition URL: https://raw.githubusercontent.com/protontypes/open-traceability/refs/heads/main/docs/definition.md
- Model: gpt-5.5
- Number of runs: 5

## Final single-paragraph summary

Across 5 independent assessment runs, the project appears strongest on Open Publications and Communication with an average score of 74.6, and weakest on Open Execution and Reproducibility with an average score of 22.4. The average total score across runs is 50.2. The scores should be interpreted as evidence-bundle-based traceability estimates rather than scientific validation: high scores indicate externally inspectable artifacts and linkages, while lower scores indicate missing, implicit, or insufficiently versioned evidence in the collected material.

## Score table across runs

| Stage | Stage name | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Average | Std dev |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Open Input Data and Measurement Evidence | 68 | 66 | 72 | 64 | 64 | 66.8 | 3.0 |
| 2 | Open-Source Models, Methods, and Software | 55 | 48 | 46 | 55 | 48 | 50.4 | 3.8 |
| 3 | Open Execution and Reproducibility | 24 | 24 | 28 | 18 | 18 | 22.4 | 3.9 |
| 4 | Open Community and Review | 37 | 34 | 43 | 43 | 35 | 38.4 | 3.9 |
| 5 | Open Publications and Communication | 74 | 74 | 74 | 78 | 73 | 74.6 | 1.7 |
| 6 | Open Linkage | 49 | 46 | 50 | 49 | 47 | 48.2 | 1.5 |

## Total score

| Run | Total score |
| --- | ---: |
| 1 | 51 |
| 2 | 49 |
| 3 | 52 |
| 4 | 51 |
| 5 | 48 |

Average total score: **50.2**; population standard deviation: **1.5**.

## Sources followed during the assessment

Every URL that was actually fetched and supplied to the model as evidence. This covers the project repository, its GitHub namespace, and each individual file, documentation page, or linked resource that was followed. Scores and references below are derived only from these sources.

- Project/report URL followed: [https://climatetrace.org](https://climatetrace.org)
- Assessment definition URL followed: [https://raw.githubusercontent.com/protontypes/open-traceability/refs/heads/main/docs/definition.md](https://raw.githubusercontent.com/protontypes/open-traceability/refs/heads/main/docs/definition.md)

A total of 6 source artifact(s) were followed across 3 host(s).

### github.com

- [Namespace · Climate TRACE coalition GitHub organization.](https://github.com/climatetracecoalition)
- [Stage 2 · open_software · Public repository of per-sector methodology documents behind the estimates.](https://github.com/climatetracecoalition/methodology-documents)
- [Stage 4 · open_community · Public issue tracker where the methodology is questioned and corrected.](https://github.com/climatetracecoalition/methodology-documents/issues)

### climatetrace.org

- [Stage 1 · open_data · Emissions data portal — downloadable country/sector/asset-level inventory.](https://climatetrace.org/data)
- [Stage 5 · open_publications · News/press updates announcing releases and explaining the inventory.](https://climatetrace.org/news)

### api.climatetrace.org

- [Stage 1 · open_data · Public REST API (Swagger) exposing the emissions data programmatically.](https://api.climatetrace.org/v6/swagger/index.html)

## Consolidated references by stage

References cited across all runs, deduplicated by URL. The runs that cited each reference are noted in parentheses; references cited by more runs appear first. References marked ⚠️ point to a URL that was not part of the collected evidence bundle and could not be verified (the model may have introduced them).

### Stage 1: Open Input Data and Measurement Evidence

Average score 66.8 (range 64–72 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 5, high 0).

- [Climate TRACE data downloads portal](https://climatetrace.org/data): States that Climate TRACE emissions data are free and publicly available for download and via API, with bulk packages for countries or sectors containing annual country-level emissions, monthly source-level emissions, confidence, and ownership where available. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Climate TRACE public API reference](https://api.climatetrace.org/v6/swagger/index.html): Evidence bundle identifies this as the v6 API Reference exposing the emissions data programmatically. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Climate TRACE methodology repository](https://github.com/climatetracecoalition/methodology-documents): The repository is described as containing detailed, sector-specific methodology documents, with folders for prior years and a 2025 folder for current methodologies. _(cited in 1/5 runs: 3)_
- [Climate TRACE project claim/home](https://climatetrace.org) ⚠️: The curated claim describes an independent global greenhouse-gas emissions inventory derived from satellite observations and other remote sensing combined with AI. _(cited in 1/5 runs: 4)_

### Stage 2: Open-Source Models, Methods, and Software

Average score 50.4 (range 46–55 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 5, high 0).

- [Climate TRACE methodology-documents repository](https://github.com/climatetracecoalition/methodology-documents): Public GitHub repository described as 'Detailed, sector specific methodology documents' with README stating that the 2025 folder contains the most up-to-date methodologies and previous years are available in respective folders. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Climate TRACE GitHub organization](https://github.com/climatetracecoalition): Organization lists public repositories including methodology-documents, climate-trace-tools, peer-reviewed-publications, and public-api-examples. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Climate TRACE data page](https://climatetrace.org/data): The data portal directs users to sector pages, methodology PDFs, FAQs, resources, guidance, and API reference for understanding how Climate TRACE data are created and structured. _(cited in 1/5 runs: 3)_

### Stage 3: Open Execution and Reproducibility

Average score 22.4 (range 18–28 across 5 runs). Reported uncertainty: mostly low (low 2, medium 1, high 2).

- [Climate TRACE data downloads portal](https://climatetrace.org/data): Download packages include CSVs, data guide, detailed data schema, and the page refers users to a GitHub changelog for changes from the last release. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Climate TRACE methodology-documents repository](https://github.com/climatetracecoalition/methodology-documents): README directs users to year-specific sector methodologies and previous years' methodologies. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [No nominated execution evidence](https://climatetrace.org) ⚠️: The evidence bundle explicitly lists '(no sources nominated for this dimension)' under Stage 3: Open Execution and Reproducibility. _(cited in 3/5 runs: 1, 4, 5)_
- [API reference](https://api.climatetrace.org/v6/swagger/index.html): The v6 API Reference exposes Climate TRACE data programmatically. _(cited in 1/5 runs: 2)_
- [Climate TRACE GitHub organization](https://github.com/climatetracecoalition): The organization lists public repositories including climate-trace-tools and public-api-examples, but the evidence bundle does not provide details showing that these reproduce the published inventory. _(cited in 1/5 runs: 3)_

### Stage 4: Open Community and Review

Average score 38.4 (range 34–43 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 5, high 0).

- [Methodology documents issue tracker](https://github.com/climatetracecoalition/methodology-documents/issues): Public GitHub issues page is visible, but shows 'Issue creation is restricted in this repository' and the open-issues search shows no results. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [News item responding to external accuracy critique](https://climatetrace.org/news): News listing includes 'Climate TRACE Road Transportation Emissions: Correcting the Record on City-Level Accuracy,' described as a response to a recent study from Northern Arizona University researchers. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Climate TRACE GitHub organization](https://github.com/climatetracecoalition): Organization lists a public 'peer-reviewed-publications' repository. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_

### Stage 5: Open Publications and Communication

Average score 74.6 (range 73–78 across 5 runs). Reported uncertainty: mostly medium (low 2, medium 3, high 0).

- [Climate TRACE data downloads portal](https://climatetrace.org/data): States that the page offers bulk download packages, beta API information, FAQs/resources/guidance, sector methodological summaries, data schema, licensing, citations, Zenodo previous versions, and a GitHub changelog. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Climate TRACE news and insights](https://climatetrace.org/news): Lists release and explanatory items such as 'Climate TRACE Releases March 2026 Emissions Data,' 'Climate TRACE Releases February 2026 Emissions Data,' ownership-data guidance, and articles applying the data. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Climate TRACE methodology-documents repository](https://github.com/climatetracecoalition/methodology-documents): README says the repository contains sector-specific methodology documents and directs users to the most up-to-date 2025 folder and previous-year folders. _(cited in 4/5 runs: 1, 2, 3, 4)_
- [Climate TRACE project home](https://climatetrace.org) ⚠️: The evidence bundle identifies the main claim URL as the Climate TRACE homepage for an independent, openly available global inventory of greenhouse-gas emissions. _(cited in 3/5 runs: 1, 3, 5)_

### Stage 6: Open Linkage

Average score 48.2 (range 46–50 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 5, high 0).

- [Data portal linkage to methods, schema, versions, and changelog](https://climatetrace.org/data): The data page directs users to FAQs, resources, sector methodological details, a data guide, detailed data schema, Zenodo previous versions, and a GitHub changelog. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Methodology-documents repository](https://github.com/climatetracecoalition/methodology-documents): README states that 2025 contains the most up-to-date methodologies and previous years' methodologies are available in their respective folders. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Public API reference](https://api.climatetrace.org/v6/swagger/index.html): Evidence bundle identifies this as the v6 API Reference for programmatic access to Climate TRACE emissions data. _(cited in 3/5 runs: 1, 3, 4)_
- [News release communications](https://climatetrace.org/news): News page lists release-specific announcements such as May release 5.7.0 including monthly emissions data through March 2026 and April release 5.6.0 including data through February 2026. _(cited in 3/5 runs: 1, 2, 3)_
- [Issue tracker limitation](https://github.com/climatetracecoalition/methodology-documents/issues): The captured issue tracker shows no open issue results and restricted issue creation. _(cited in 1/5 runs: 4)_
- [Climate TRACE GitHub namespace](https://github.com/climatetracecoalition): The public GitHub organization aggregates methodology-documents, climate-trace-tools, peer-reviewed-publications, and public-api-examples under the Climate TRACE namespace. _(cited in 1/5 runs: 5)_

## Consolidated limitations across runs

Distinct limitations raised by one or more runs (deduplicated):
- The assessment uses only the supplied evidence bundle and definition text; linked resources such as the full data guide, FAQs, sector methodology PDFs, Zenodo records, changelog files, and API details were not independently inspected beyond the provided excerpts.
- The evidence bundle does not include raw primary data sources, satellite product identifiers, training data, model weights, production code, workflow scripts, containers, parameter files, or run logs.
- The existence of repositories such as climate-trace-tools, public-api-examples, and peer-reviewed-publications is visible in the bundle, but their contents, licences, and relevance to production methods are not established by the supplied evidence.
- Uncertainty estimates are reported as available on request, but the supplied evidence does not show openly downloadable uncertainty datasets or detailed uncertainty methodology.
- Community and review evidence is incomplete: the issue tracker is visible but restricted, and no closed-issue discussions, pull-request reviews, governance records, or peer-review documents are included.
- Scores are conservative where evidence is referenced by the website but not actually included in the evidence bundle.
- The evidence bundle does not include the full contents of methodology PDFs, data guides, schemas, Zenodo records, or changelog files, so their depth could not be fully assessed.
- No direct evidence was supplied for executable workflows, workflow runs, containers, notebooks, parameters, or computational environments.
- No direct evidence was supplied that the core AI models, trained model artifacts, emissions-estimation code, or infrastructure software are open source or independently runnable.
- The underlying primary measurement evidence, including satellite/remote-sensing inputs and asset data sources, is not documented in the supplied evidence at the level required for full external verification.
- Uncertainty estimates are described as available on request, but the bundle does not show that they are openly downloadable for all sectors and releases.
- The issue tracker evidence shows restricted issue creation and no visible issue results, limiting assessment of public critique and correction processes.
- The assessment relies only on the curated evidence bundle and linked artifacts described there; inaccessible or truncated page content may omit relevant details.
- The assessment uses only the supplied evidence bundle; it does not verify the contents of linked PDFs, Zenodo records, changelog files, API endpoints, or repository files beyond the excerpts provided.
- No direct evidence was supplied for Stage 3 execution and reproducibility, so scoring is necessarily conservative.
- The bundle does not show whether the core AI models, training data, model weights, emissions-estimation pipelines, or production infrastructure are open source.
- The bundle does not provide primary satellite/remote-sensing datasets or asset-level provenance linking individual estimates to specific observations.
- Uncertainty estimates are described as available on request, but the evidence does not show open, downloadable uncertainty data for all sectors.
- The evidence mentions peer-reviewed publications but does not include the publication list, papers, review reports, or replication records.
- Licensing is clear for the data as Creative Commons 4.0, but the evidence does not establish licenses for all methodology documents, software repositories, or publications.
- The assessment uses only the supplied evidence bundle; some relevant details may exist on linked pages or inside downloadable packages that were not included in the captured evidence.
- The evidence bundle does not include the actual contents of data guides, schemas, Zenodo records, changelogs, methodology PDFs, or API endpoints, so their depth could not be fully evaluated.
- No direct evidence was supplied for primary satellite/remote-sensing datasets, raw measurements, calibration, quality controls, training data, or transformation lineage.
- No direct evidence was supplied for executable workflows, run logs, containers, dependency files, parameter files, or reproducibility instructions for generating the inventory.
- The GitHub pages in the evidence show repository summaries but not license files, full code contents, pull-request discussions, or closed issues.
- Publication and review evidence is mostly at the listing/announcement level; peer-review details, correction histories, and public governance records were not supplied.
- The assessment uses only the supplied evidence bundle and does not verify the contents of linked PDFs, data-guide files, Zenodo records, changelogs, API endpoints, or downloadable CSV packages beyond the provided excerpts.
- No direct evidence was supplied for Stage 3 execution and reproducibility, so the score is conservative and based on missing workflow/run-level artifacts in the bundle.
- The evidence does not show the underlying primary satellite observations, remote-sensing inputs, training data, ground measurements, or quality-control datasets used to produce the inventory.
- The evidence does not show the production AI/model source code, model weights, dependencies, containers, infrastructure code, or OSI-approved licenses for software components.
- The community/review assessment is limited because the peer-reviewed-publications repository contents and full critique-response articles were not included in the bundle.
- The API reference excerpt only establishes the existence of a public v6 API reference; it does not provide detailed endpoint behavior, provenance metadata, or reproducibility guarantees in the supplied text.
