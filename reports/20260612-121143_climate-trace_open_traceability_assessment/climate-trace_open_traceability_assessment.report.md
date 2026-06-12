# Open Traceability Assessment Report

- Project/report URL: https://climatetrace.org/
- Assessment definition URL: https://raw.githubusercontent.com/protontypes/open-traceability/refs/heads/main/docs/definition.md
- Model: gpt-5.5
- Number of runs: 5

## Final single-paragraph summary

Across 5 independent assessment runs, the project appears strongest on Open Publications and Communication with an average score of 65.4, and weakest on Open-Source Models, Methods, and Software with an average score of 18.0. The average total score across runs is 38.2. The scores should be interpreted as evidence-bundle-based traceability estimates rather than scientific validation: high scores indicate externally inspectable artifacts and linkages, while lower scores indicate missing, implicit, or insufficiently versioned evidence in the collected material.

## Score table across runs

| Stage | Stage name | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Average | Std dev |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Open Input Data and Measurement Evidence | 48 | 52 | 48 | 55 | 46 | 49.8 | 3.2 |
| 2 | Open-Source Models, Methods, and Software | 18 | 14 | 18 | 24 | 16 | 18.0 | 3.3 |
| 3 | Open Execution and Reproducibility | 22 | 16 | 22 | 28 | 22 | 22.0 | 3.8 |
| 4 | Open Community and Review | 47 | 44 | 43 | 52 | 43 | 45.8 | 3.4 |
| 5 | Open Publications and Communication | 68 | 66 | 61 | 68 | 64 | 65.4 | 2.7 |
| 6 | Open Linkage | 27 | 24 | 26 | 36 | 29 | 28.4 | 4.1 |

## Total score

| Run | Total score |
| --- | ---: |
| 1 | 38 |
| 2 | 36 |
| 3 | 36 |
| 4 | 44 |
| 5 | 37 |

Average total score: **38.2**; population standard deviation: **3.0**.

## Consolidated references by stage

References cited across all runs, deduplicated by URL. The runs that cited each reference are noted in parentheses; references cited by more runs appear first. References marked ⚠️ point to a URL that was not part of the collected evidence bundle and could not be verified (the model may have introduced them).

### Stage 1: Open Input Data and Measurement Evidence

Average score 49.8 (range 46–55 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 3, high 2).

- [Climate TRACE homepage data-scope statement](https://climatetrace.org/): The page states: “Open Data” and “Track Global Emissions from 745 million sources of greenhouse gases and air pollutants worldwide,” with “744,678,997 emitting assets” and data for “10+ years” with monthly data from 2021. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_

### Stage 2: Open-Source Models, Methods, and Software

Average score 18.0 (range 14–24 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 3, high 2).

- [Climate TRACE homepage method summary](https://climatetrace.org/): The page states: “We use satellites, other remote sensing techniques, and artificial intelligence” to provide global emissions tracking. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_

### Stage 3: Open Execution and Reproducibility

Average score 22.0 (range 16–28 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 3, high 2).

- [Climate TRACE homepage release note](https://climatetrace.org/): The page lists: “Climate TRACE Releases March 2026 Emissions Data” and says “May release 5.7.0 includes monthly emissions data through March 2026.” _(cited in 5/5 runs: 1, 2, 3, 4, 5)_

### Stage 4: Open Community and Review

Average score 45.8 (range 43–52 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 3, high 2).

- [Climate TRACE homepage response to critique](https://climatetrace.org/): The news section includes: “Climate TRACE Road Transportation Emissions: Correcting the Record on City-Level Accuracy,” described as a response to a study from Northern Arizona University regarding city-level road transportation emissions. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_

### Stage 5: Open Publications and Communication

Average score 65.4 (range 61–68 across 5 runs). Reported uncertainty: mostly medium (low 2, medium 3, high 0).

- [Climate TRACE homepage public claims and scope](https://climatetrace.org/): The homepage describes Climate TRACE as “Independent Greenhouse gas Emissions Tracking” and says it tracks emissions from 745 million sources across 10 sectors, 67 subsectors, 3 greenhouse gases, and 8 non-GHG air pollutants. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_

### Stage 6: Open Linkage

Average score 28.4 (range 24–36 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 3, high 2).

- [Climate TRACE homepage combined claim-data-method communication](https://climatetrace.org/): The page links the public claim of tracking greenhouse gas emissions to “Open Data,” data coverage statements, and a “How it Works” section describing satellites, remote sensing, and AI. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_

## Consolidated limitations across runs

Distinct limitations raised by one or more runs (deduplicated):
- The evidence bundle contains only text extracted from the Climate TRACE homepage, not the actual open data portal, downloadable datasets, metadata, or API documentation.
- No open-source repositories, software licenses, model cards, dependency files, or infrastructure documentation were supplied.
- No workflow scripts, run manifests, computational environment specifications, notebooks, containers, or reproducibility instructions were supplied.
- No primary measurement records, source-specific provenance, uncertainty estimates, quality-control procedures, or transformation documentation were supplied.
- No detailed peer-review documents, public issue trackers, governance records, correction logs, or full critique-response records were supplied.
- No explicit artifact-level linkage was supplied connecting a specific environmental claim to exact dataset versions, code versions, model configurations, workflow runs, review records, and publications.
- The assessment is based only on the supplied evidence bundle, which contains homepage text extraction and not the actual open data portal, data files, documentation, or metadata.
- No source-code repositories, open-source licenses, model documentation, dependencies, or software infrastructure evidence were supplied.
- No workflow scripts, computational environments, run logs, parameters, notebooks, containers, or reproducibility instructions were supplied.
- No detailed data provenance, primary measurement records, uncertainty estimates, quality-control procedures, or transformation documentation were supplied.
- The evidence mentions a release version but does not provide persistent dataset identifiers, archived snapshots, checksums, or exact claim-to-version mappings.
- No formal peer-review records, public issue tracker, governance documents, correction log, or detailed community review process were supplied.
- News items are referenced in the homepage text, but the underlying article contents were not included in the evidence bundle.
- The evidence bundle contains only homepage text extraction; no actual open-data portal contents, downloadable files, API documentation, metadata, or licenses were supplied.
- No code repositories, model documentation, dependency manifests, software licenses, or infrastructure documentation were included.
- No reproducible workflow artifacts, workflow run logs, notebooks, containers, parameters, or computational environment specifications were provided.
- No public issue tracker, peer-review reports, correction logs, governance records, or detailed community discussion archives were supplied.
- The assessment could not verify whether “Access Open Data,” news links, surveys, or reports on the live site provide additional traceability because only the supplied evidence bundle was used.
- Scores are conservative where direct evidence is absent, even if such evidence may exist elsewhere on the Climate TRACE website or related repositories.
- The evidence bundle contains only text extracted from the Climate TRACE homepage; no linked open-data portal contents, downloadable datasets, documentation pages, methodology reports, repositories, licenses, or APIs were supplied.
- Scores do not assess whether Climate TRACE’s emissions estimates are scientifically correct; they assess only the public traceability evidence provided.
- Where the homepage mentions “Open Data,” the assessment cannot verify data format, license, metadata completeness, primary-data lineage, uncertainty quantification, or reuse conditions from the supplied evidence.
- No direct evidence was supplied for open-source code, model implementations, dependencies, computational environments, workflow runs, or reproducibility instructions.
- No detailed evidence was supplied for public peer review, issue tracking, governance records, correction logs, or systematic handling of external criticism beyond one visible response item.
- The assessment cannot determine whether stronger linkage exists inside the Climate TRACE data portal or documentation because those artifacts were not included in the evidence bundle.
- The assessment is based only on the supplied evidence bundle, which consists of a text extraction from the Climate TRACE homepage; no linked data portal pages, downloads, methods documents, repositories, or reports were available for inspection.
- The homepage claims 'Open Data,' but the bundle does not evidence data licences, file formats, API terms, persistent identifiers, archival/versioning practices, or direct access to underlying primary data.
- No supplied evidence demonstrates open-source software, model code, dependencies, configuration, or infrastructure documentation.
- No supplied evidence demonstrates reproducible execution artefacts such as workflow scripts, notebooks, containers, run logs, parameters, or archived computational outputs.
- Review evidence is limited to homepage-level references to a coalition, feedback, and a response to an external study; the underlying review records or correction processes were not included.
- The linkage score is constrained because the evidence does not connect specific environmental claims to exact datasets, code versions, model runs, review events, and publications.
