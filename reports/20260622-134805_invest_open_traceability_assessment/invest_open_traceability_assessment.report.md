# Open Traceability Assessment Report: InVEST

- [ ] **Human reviewer:** I have validated all claims in this report against the references provided, and reviewed, edited, and approved its contents.

- Project/report URL: https://github.com/natcap/invest
- Assessment definition URL: https://raw.githubusercontent.com/protontypes/open-traceability/refs/heads/main/docs/definition.md
- Model: gpt-5.5
- Number of runs: 5

## Final single-paragraph summary

Across 5 independent assessment runs, the project appears strongest on Open-Source Models, Methods, and Software with an average score of 86.6, and weakest on Open Input Data and Measurement Evidence with an average score of 58.2. The average total score across runs is 73.6. The scores should be interpreted as evidence-bundle-based traceability estimates rather than scientific validation: high scores indicate externally inspectable artifacts and linkages, while lower scores indicate missing, implicit, or insufficiently versioned evidence in the collected material.

## Score table across runs

| Stage | Stage name | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Average | Std dev |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Open Input Data and Measurement Evidence | 64 | 54 | 58 | 57 | 58 | 58.2 | 3.2 |
| 2 | Open-Source Models, Methods, and Software | 86 | 86 | 86 | 87 | 88 | 86.6 | 0.8 |
| 3 | Open Execution and Reproducibility | 68 | 70 | 69 | 68 | 68 | 68.6 | 0.8 |
| 4 | Open Community and Review | 78 | 78 | 78 | 76 | 83 | 78.6 | 2.3 |
| 5 | Open Publications and Communication | 84 | 83 | 87 | 88 | 90 | 86.4 | 2.6 |
| 6 | Open Linkage | 62 | 64 | 63 | 64 | 65 | 63.6 | 1.0 |

## Total score

| Run | Total score |
| --- | ---: |
| 1 | 74 |
| 2 | 72 |
| 3 | 74 |
| 4 | 73 |
| 5 | 75 |

Average total score: **73.6**; population standard deviation: **1.0**.

## Sources followed during the assessment

Every URL that was actually fetched and supplied to the model as evidence. This covers the project repository, its GitHub namespace, and each individual file, documentation page, or linked resource that was followed. Scores and references below are derived only from these sources.

- Project/report URL followed: [https://github.com/natcap/invest](https://github.com/natcap/invest)
- Assessment definition URL followed: [https://raw.githubusercontent.com/protontypes/open-traceability/refs/heads/main/docs/definition.md](https://raw.githubusercontent.com/protontypes/open-traceability/refs/heads/main/docs/definition.md)

A total of 12 source artifact(s) were followed across 6 host(s).

### github.com

- [Namespace](https://github.com/natcap)
- [Stage 2 · open_software · Main InVEST toolset source, Apache-2.0 licensed.](https://github.com/natcap/invest)
- [Stage 2 · open_software · PyGeoprocessing — the geospatial processing library InVEST depends on.](https://github.com/natcap/pygeoprocessing)
- [Stage 2 · open_software · TaskGraph — the workflow engine all InVEST models use to organise execution.](https://github.com/natcap/taskgraph)
- [Stage 3 · open_execution · CI workflow that builds and tests InVEST on every change.](https://github.com/natcap/invest/blob/main/.github/workflows/build-and-test.yml)
- [Stage 4 · open_community · Public issue tracker where bugs are reported, discussed, and corrected.](https://github.com/natcap/invest/issues)
- [Stage 5 · open_publications · Versioned releases with changelogs, tying outputs to specific software versions.](https://github.com/natcap/invest/releases)

### bitbucket.org

- [Stage 1 · open_data · Versioned sample input datasets covering every InVEST model.](https://bitbucket.org/natcap/invest-sample-data)

### naturalcapitalalliance.stanford.edu

- [Stage 1 · open_data · Official downloads page listing InVEST data sources and guidance.](https://naturalcapitalalliance.stanford.edu/software/invest/invest-downloads-data)

### invest.readthedocs.io

- [Stage 3 · open_execution · Documented, versioned install procedure for reproducing the environment.](https://invest.readthedocs.io/en/latest/installing.html)

### community.naturalcapitalalliance.org

- [Stage 4 · open_community · Community forum for user support and model questions.](https://community.naturalcapitalalliance.org/)

### storage.googleapis.com

- [Stage 5 · open_publications · InVEST User Guide — the canonical documentation of models, methods, and data needs.](https://storage.googleapis.com/releases.naturalcapitalproject.org/invest-userguide/latest/en/index.html)

## Consolidated references by stage

References cited across all runs, deduplicated by URL. The runs that cited each reference are noted in parentheses; references cited by more runs appear first. References marked ⚠️ point to a URL that was not part of the collected evidence bundle and could not be verified (the model may have introduced them).

### Stage 1: Open Input Data and Measurement Evidence

Average score 58.2 (range 54–64 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 5, high 0).

- [Official InVEST downloads and data sources page](https://naturalcapitalalliance.stanford.edu/software/invest/invest-downloads-data): The page lists “Individual Sample Datasets for InVEST 3.20.0” and under “Data Sources” links to the Natural Capital Alliance Data Hub, Kc Calculator, Parameter Value Database, Nutrient Database, and Sediment Database. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [InVEST sample data repository](https://bitbucket.org/natcap/invest-sample-data): Curator note identifies this as “Versioned sample input datasets covering every InVEST model,” although the captured page content only shows a generic Bitbucket page. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [InVEST User Guide](https://storage.googleapis.com/releases.naturalcapitalproject.org/invest-userguide/latest/en/index.html): The table of contents lists model sections with “Data Needs,” “Limitations and Simplifications,” “Appendix: Data Sources,” and “References” for multiple models such as Annual Water Yield, Carbon Storage, and Coastal Vulnerability. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_

### Stage 2: Open-Source Models, Methods, and Software

Average score 86.6 (range 86–88 across 5 runs). Reported uncertainty: mostly low (low 5, medium 0, high 0).

- [Main InVEST GitHub repository](https://github.com/natcap/invest): The repository is public and described as “InVEST®: models that map and value the goods and services from nature that sustain and fulfill human life,” with visible Code, Issues, Pull requests, Discussions, Actions, Projects, Wiki, and Security tabs. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [PyGeoprocessing repository](https://github.com/natcap/pygeoprocessing): PyGeoprocessing is described as a Python/Cython library providing raster, vector, and hydrological GIS operations, developed to support InVEST; files include LICENSE.txt, README.rst, requirements.txt, setup.py, tests, and docs. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [TaskGraph repository](https://github.com/natcap/taskgraph): The public repository has visible Issues, Pull requests, Actions, Projects, and Security tabs; the curator note identifies it as the workflow engine all InVEST models use to organize execution. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Installation and dependency documentation](https://invest.readthedocs.io/en/latest/installing.html): The documentation states that InVEST is installable from conda-forge, PyPI, or directly from the git source tree, and lists dependencies including GDAL, pygeoprocessing, taskgraph, pandas, numpy, scipy, geopandas, and others. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Natural Capital Alliance GitHub organization](https://github.com/natcap): The pinned repository list shows “invest Public” with language Python and license “Apache-2.0”; related repositories include pygeoprocessing, taskgraph, and invest.users-guide. _(cited in 3/5 runs: 1, 2, 3)_

### Stage 3: Open Execution and Reproducibility

Average score 68.6 (range 68–70 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 5, high 0).

- [InVEST build-and-test workflow](https://github.com/natcap/invest/blob/main/.github/workflows/build-and-test.yml): Curator note identifies this as a CI workflow that builds and tests InVEST on every change; the captured GitHub page confirms the workflow file URL in the public repository but does not expose workflow contents. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [InVEST installation documentation](https://invest.readthedocs.io/en/latest/installing.html): The documentation gives commands for conda-forge installation, pip installation, and source installation from GitHub, and lists dependencies such as GDAL, pygeoprocessing, taskgraph, pandas, numpy, scipy, fiona, geopandas, and matplotlib. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [InVEST releases](https://github.com/natcap/invest/releases): Release 3.20.0 is shown as latest, dated 11 Jun, with commit fca8bf5 and a verified GitHub signature; release notes list model and infrastructure changes. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Official downloads page](https://naturalcapitalalliance.stanford.edu/software/invest/invest-downloads-data): Provides downloads for InVEST 3.20.0 Workbench for Windows and Mac, older/development versions, individual sample datasets, and user guides. _(cited in 3/5 runs: 2, 3, 5)_

### Stage 4: Open Community and Review

Average score 78.6 (range 76–83 across 5 runs). Reported uncertainty: mostly low (low 5, medium 0, high 0).

- [InVEST GitHub issues](https://github.com/natcap/invest/issues): The public repository interface shows Issues, Pull requests, Discussions, Actions, Projects, and Wiki tabs; the repository summary shows 207 issues and 6 pull requests in the captured page. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Natural Capital Alliance community forum](https://community.naturalcapitalalliance.org/): The forum lists active categories and recent posts such as “Water Yield Models to support economic analysis,” “InVEST 3.20.0 Released!,” “Regarding validation of model,” and “Negative Values - SDR Output,” with replies and views shown. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Release notes linked to issues](https://github.com/natcap/invest/releases): Release 3.20.0 changelog entries cite issue or pull-request numbers such as #2471, #2228, #2179, #2532, #2555, #2442, and #2573. _(cited in 3/5 runs: 3, 4, 5)_
- [InVEST User Guide contributor and correction note](https://storage.googleapis.com/releases.naturalcapitalproject.org/invest-userguide/latest/en/index.html): The guide lists many contributors and states that if someone is missing from the list and thinks they should be included, they should contact naturalcapitalalliance@stanford.edu. _(cited in 1/5 runs: 1)_

### Stage 5: Open Publications and Communication

Average score 86.4 (range 83–90 across 5 runs). Reported uncertainty: mostly low (low 5, medium 0, high 0).

- [InVEST User Guide](https://storage.googleapis.com/releases.naturalcapitalproject.org/invest-userguide/latest/en/index.html): The guide provides a suggested citation, “Natural Capital Alliance, 2026. InVEST 3.20.0. https://doi.org/10.60793/natcap-invest-3.20.0,” and includes sections for model summaries, introductions, models, limitations, data needs, interpreting results, appendices, and references. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Official downloads and user guide page](https://naturalcapitalalliance.stanford.edu/software/invest/invest-downloads-data): The page links to InVEST 3.20.0 Workbench downloads for Windows and Mac, the GitHub repository, older/development versions, sample datasets, user guides in English/Spanish/Chinese, plugin developer guide, data sources, citation guidance, and a usage-data notice. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Versioned GitHub releases](https://github.com/natcap/invest/releases): Release 3.20.0 includes a date, commit identifier, verified signature, and detailed changelog sections covering general changes, Workbench changes, and model-specific changes such as Annual Water Yield and Carbon Storage. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_

### Stage 6: Open Linkage

Average score 63.6 (range 62–65 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 5, high 0).

- [Official downloads page linking artifacts](https://naturalcapitalalliance.stanford.edu/software/invest/invest-downloads-data): The page gathers Workbench downloads, the InVEST GitHub repository, older/development versions, individual sample datasets, user guides, plugin developer guide, data sources, citation guidance, and usage-data notice. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [User Guide DOI and model documentation](https://storage.googleapis.com/releases.naturalcapitalproject.org/invest-userguide/latest/en/index.html): The guide gives a suggested citation with DOI for “InVEST 3.20.0” and organizes model documentation by summaries, methods, limitations, data needs, interpreting results, data-source appendices, and references. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [GitHub release version and commit](https://github.com/natcap/invest/releases): Release 3.20.0 is tied to commit fca8bf5 and a verified GitHub signature, with changelog entries referencing specific issue numbers such as #2471, #2228, #2179, #2532, and #2555. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Installation documentation linking environment and dependencies](https://invest.readthedocs.io/en/latest/installing.html): The install page documents conda-forge, PyPI, and git-source installation paths and lists package dependencies, including pygeoprocessing and taskgraph. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Community forum](https://community.naturalcapitalalliance.org/): The public forum includes recent posts on model validation, parameter databases, model errors, and release announcements. _(cited in 4/5 runs: 1, 2, 4, 5)_

## Consolidated limitations across runs

Distinct limitations raised by one or more runs (deduplicated):
- The evidence bundle does not expose detailed metadata, licenses, uncertainty estimates, or primary-measurement provenance for the sample datasets and data-source resources.
- The Bitbucket sample-data evidence is mostly represented by a curator note; the captured page content itself does not show repository contents or version tags.
- The captured GitHub workflow page does not include the actual build-and-test YAML contents, so CI details are inferred from the curator note and URL rather than directly inspected text.
- No specific environmental analysis run is included with exact input versions, parameter files, workflow run IDs, output hashes, logs, or archived computational environment.
- The assessment concerns the InVEST project/toolset, not the validity or traceability of any specific InVEST-derived environmental claim produced by a third party.
- The evidence bundle does not show formal peer-review records, governance documents, systematic correction notices, or independent replication attempts for individual models.
- The evidence bundle does not show an explicit Creative Commons or other open documentation license for the user guide/publication materials.
- The assessment uses only the supplied evidence bundle; no independent web retrieval or repository-file inspection was performed beyond the captured evidence text and curator notes.
- The Bitbucket sample-data evidence is sparse in the capture, so dataset versioning, metadata, licenses, quality controls, and uncertainty information could not be verified directly.
- The GitHub Actions workflow URL is included, but the captured evidence does not show the workflow YAML or CI results, limiting verification of automated build/test details.
- The evidence describes the InVEST toolset generally, not a specific environmental analysis or output, so claim-level provenance from inputs to outputs cannot be fully assessed.
- No complete dependency lockfile, container specification contents, datastack example, run manifest, or exact re-executable workflow artifact was provided.
- The user guide appears openly accessible and citable, but the evidence bundle does not show a Creative Commons or comparable open documentation license.
- Formal scientific peer review, governance records, correction notices, and replication attempts were not included in the bundle, although public issue/forum channels are visible.
- The evidence bundle is incomplete and several GitHub pages are truncated or show only repository headers, so file-level details, workflow contents, and licence files could not always be directly inspected.
- The Bitbucket sample-data evidence is represented mainly by a curator note; the actual datasets, metadata, provenance, uncertainty estimates, quality controls, and licences were not visible in the bundle.
- This assessment evaluates the InVEST platform claim, not a specific InVEST-derived environmental analysis; traceability of any individual map, valuation, or policy claim may be higher or lower depending on the data and workflow records supplied by that analysis.
- No evidence was provided of exact archived workflow runs tying specific inputs, parameters, software versions, dependency hashes, execution logs, and outputs together.
- No formal peer-review package, governance record, correction registry, or replication study was included, beyond public GitHub/forum review and support channels.
- Documentation appears open and citable, but the bundle does not clearly show a Creative Commons or equivalent licence for the User Guide or all communication artifacts.
- The assessment uses only the supplied evidence bundle; no additional live repository inspection was performed beyond the captured text and curator notes.
- The Bitbucket sample-data repository evidence was not captured in detail, so claims about versioned sample datasets rely heavily on the curator note and official downloads page.
- The bundle does not include dataset-level metadata, licenses, checksums, uncertainty estimates, primary measurement methods, or quality-control records for input datasets.
- The CI workflow URL is supplied, but the captured evidence does not show the YAML contents, run history, logs, or artifacts.
- No exact end-to-end model run is documented in the bundle with input versions, parameters, code commit, dependency environment, outputs, and review record.
- The assessment evaluates traceability of the InVEST toolset and its documentation, not the scientific validity or accuracy of any particular InVEST model output.
- Evidence for formal scientific peer review, governance, and correction policies is limited to public issue/forum/release infrastructure and does not include complete review records.
- The User Guide evidence uses a 'latest' URL; although it cites InVEST 3.20.0 and a DOI, the bundle does not fully demonstrate historical documentation archiving or licensing.
- The assessment uses only the supplied evidence bundle; no live repository inspection or independent download of files was performed.
- The Bitbucket sample-data repository evidence is represented mainly by a curator note, with no visible dataset contents, metadata, version tags, licenses, or uncertainty information in the bundle.
- The evidence concerns the InVEST platform/toolset rather than one specific environmental analysis; run-level traceability will vary by user project and input-data documentation.
- The CI workflow is identified by URL and curator note, but the supplied page extract does not show the workflow YAML contents or successful run history.
- No complete provenance artifact was supplied that links exact input datasets, parameters, code commit, dependency versions, workflow run, outputs, review discussion, and publication for a specific model result.
- The bundle does not provide formal peer-review records or governance documentation for individual model methods, though public issue/forum review channels are evident.
- Documentation licensing and archival/versioning details are not fully visible in the supplied evidence.
