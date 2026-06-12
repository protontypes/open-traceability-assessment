# Open Traceability Assessment Report

- Project/report URL: https://github.com/pypsa/pypsa-eur
- Assessment definition URL: https://raw.githubusercontent.com/protontypes/open-traceability/refs/heads/main/docs/definition.md
- Number of runs: 10

## Final single-paragraph summary

Across 10 independent assessment runs, the project appears strongest on Open-Source Models, Methods, and Software with an average score of 85.6, and weakest on Open Verifiability with an average score of 68.4. The average total score across runs is 76.7. The scores should be interpreted as evidence-bundle-based traceability estimates rather than scientific validation: high scores indicate externally inspectable artifacts and linkages, while lower scores indicate missing, implicit, or insufficiently versioned evidence in the collected material.

## Score table across runs

| Stage | Stage name | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Run 6 | Run 7 | Run 8 | Run 9 | Run 10 | Average | Std dev |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Open Input Data and Measurement Evidence | 68 | 74 | 68 | 72 | 72 | 70 | 72 | 72 | 72 | 72 | 71.2 | 1.8 |
| 2 | Open-Source Models, Methods, and Software | 84 | 87 | 86 | 87 | 88 | 88 | 83 | 85 | 84 | 84 | 85.6 | 1.7 |
| 3 | Open Execution and Reproducibility | 74 | 78 | 79 | 76 | 76 | 78 | 74 | 76 | 78 | 76 | 76.5 | 1.6 |
| 4 | Open Community and Review | 76 | 74 | 77 | 69 | 80 | 76 | 78 | 78 | 79 | 77 | 76.4 | 2.9 |
| 5 | Open Publications and Communication | 82 | 79 | 85 | 80 | 83 | 82 | 80 | 80 | 81 | 83 | 81.5 | 1.7 |
| 6 | Open Verifiability | 66 | 68 | 70 | 67 | 67 | 69 | 68 | 68 | 73 | 68 | 68.4 | 1.9 |

## Total score

| Run | Total score |
| --- | ---: |
| 1 | 75 |
| 2 | 77 |
| 3 | 78 |
| 4 | 75 |
| 5 | 78 |
| 6 | 77 |
| 7 | 76 |
| 8 | 76 |
| 9 | 78 |
| 10 | 77 |

Average total score: **76.7**; population standard deviation: **1.1**.

## Consolidated references by stage

References cited across all runs, deduplicated by URL. The runs that cited each reference are noted in parentheses; references cited by more runs appear first.

### Stage 1: Open Input Data and Measurement Evidence

Average score 71.2 (range 68–74 across 10 runs).

- [README input data sources](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/README.md): The README says the model is built from open data and lists inputs including OpenStreetMap/Zenodo grid data, powerplantmatching, ENTSO-E Transparency Platform demand, ERA5 and SARAH-3 via atlite, and Eurostat/JRC-IDEES energy balances. _(cited in 10/10 runs: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)_
- [ENTSO-E GridKit dataset documentation](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/data/entsoegridkit/README.md): Documents an unofficial ENTSO-E map extract from March 2022, processed by GridKit, with warnings about coordinate inaccuracies, voltage ranges, derived transformers, and generator-bus assignments; also describes CSV fields. _(cited in 10/10 runs: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)_
- [Data versions validation test](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/test/test_data_versions_layer.py): Defines schema checks for data/versions.csv including dataset, version, source, tags, added date, URL, latest-tag consistency, sorting, and archive URL requirements. _(cited in 10/10 runs: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)_
- [Test fixtures for external geodata](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/test/conftest.py): Test fixtures download Natural Earth country boundaries and include a disabled EEZ fixture because of unreliable data download. _(cited in 1/10 runs: 5)_
- [Repository metadata topics](https://github.com/pypsa/pypsa-eur): Repository topics include `energy-data`, `energy-system-model`, `europe`, `power-grid`, and `transmission-network`. _(cited in 1/10 runs: 10)_

### Stage 2: Open-Source Models, Methods, and Software

Average score 85.6 (range 83–88 across 10 runs).

- [Repository metadata](https://github.com/pypsa/pypsa-eur): Repository description: “PyPSA-Eur: A Sector-Coupled Open Optimisation Model of the European Energy System”; default branch master; topics include energy-system-model, snakemake, capacity-expansion-model; license field is null. _(cited in 10/10 runs: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)_
- [CITATION.cff](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/CITATION.cff): Lists title, repository URL, version v2026.02.0, license MIT, authors, and ORCIDs. _(cited in 10/10 runs: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)_
- [Conda environment file](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/envs/environment.yaml): Specifies dependencies such as pypsa, linopy, snakemake-minimal, atlite, geopandas, pandas, glpk, highspy, gurobi, and many geospatial/scientific libraries. _(cited in 10/10 runs: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)_
- [Development Dockerfile](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/docker/dev-env/Dockerfile): Builds from ghcr.io/prefix-dev/pixi, copies pixi.toml and pixi.lock, installs the default pixi environment, and sets an entrypoint for the environment. _(cited in 10/10 runs: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)_
- [README open-source workflow statement](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/README.md): The README states: “The model is built from open data using a Snakemake workflow and fully open source” and is designed for the open-source PyPSA framework. _(cited in 8/10 runs: 1, 2, 3, 5, 7, 8, 9, 10)_

### Stage 3: Open Execution and Reproducibility

Average score 76.5 (range 74–79 across 10 runs).

- [README Snakemake workflow](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/README.md): States that the model is built from open data using a Snakemake workflow. _(cited in 10/10 runs: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)_
- [Test workflow](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/test.yaml): Runs unit tests and integration tests on push, pull request, schedule, and workflow dispatch; integration tests run `pixi run integration-tests`; uploads logs, .snakemake/log, and results with 3-day retention. _(cited in 10/10 runs: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)_
- [Environment specification](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/envs/environment.yaml): Defines a named pypsa-eur environment with pinned/minimum versions for Python, PyPSA, Snakemake, geospatial packages, solvers, and scientific dependencies. _(cited in 8/10 runs: 1, 2, 3, 5, 7, 8, 9, 10)_
- [Development Dockerfile](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/docker/dev-env/Dockerfile): Installs the pixi environment from `pixi.toml` and `pixi.lock` into a container and sets an entrypoint for the activated environment. _(cited in 6/10 runs: 2, 5, 6, 7, 8, 9)_
- [Container image workflow](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/push-images.yaml): Builds and pushes ghcr.io/pypsa/eur-dev-env images tagged with the GitHub commit SHA, and tags latest on master. _(cited in 5/10 runs: 1, 4, 5, 8, 10)_
- [Configuration schema synchronization test](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/test/test_config_schema.py): Checks that config.default.yaml and schema.default.json are in sync with generated Pydantic schema, failing if generated and existing content differ. _(cited in 5/10 runs: 1, 3, 4, 6, 7)_
- [Release workflow](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/release.yaml): On version tags, validates release preparation and runs pixi run update-dags before committing prepared release changes. _(cited in 3/10 runs: 3, 9, 10)_
- [Validator workflow](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/validate.yaml): Runs `lkstrp/pypsa-validator` with `envs/environment.yaml` and `config/test/config.validator.yaml`, then creates a report/comment with plots if validation succeeds. _(cited in 1/10 runs: 2)_

### Stage 4: Open Community and Review

Average score 76.4 (range 69–80 across 10 runs).

- [Repository issue metadata](https://github.com/pypsa/pypsa-eur): Repository metadata reports open_issues_count: 256. _(cited in 10/10 runs: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)_
- [Contributing guide](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/doc/contributing.md): Invites bug reports, ideas, pull requests, help-wanted issue discussion, draft PRs, and Discord discussion; states all code contributions follow the four-eyes principle and are reviewed by a second person. _(cited in 10/10 runs: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)_
- [Validator bot workflow](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/validate.yaml): Runs a pypsa-validator on pull requests from the repository and creates validation reports with plots if validation passes. _(cited in 9/10 runs: 1, 3, 4, 5, 6, 7, 8, 9, 10)_
- [CodeQL workflow](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/codeql.yaml): Runs CodeQL analysis for Python on push, pull requests, and weekly schedule. _(cited in 6/10 runs: 1, 2, 5, 6, 7, 9)_
- [README community links and limitations](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/README.md): Links to GitHub issues for known topics and says users may help or make suggestions; includes a Discord badge/link and warns that documentation remains somewhat patchy. _(cited in 6/10 runs: 2, 5, 7, 8, 9, 10)_
- [Security scan workflow](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/security-scan.yaml): Generates SBOM on master and runs vulnerability scans using Anchore, uploading SARIF and checking fork PRs against baseline high+ CVEs. _(cited in 5/10 runs: 1, 2, 3, 8, 10)_
- [Test workflow on PRs](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/test.yaml): Configured to run on pull requests to master as well as pushes and scheduled runs. _(cited in 1/10 runs: 4)_

### Stage 5: Open Publications and Communication

Average score 81.5 (range 79–85 across 10 runs).

- [README documentation, DOIs, warnings](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/README.md): Includes release and ReadTheDocs badges, Zenodo DOI badges, model overview, data-source list, diagrams, warnings, limitations link, and references to Joule papers; also states documentation remains somewhat patchy. _(cited in 10/10 runs: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)_
- [CITATION.cff](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/CITATION.cff): Provides citation message, title, repository, version v2026.02.0, MIT license declaration, authors, and ORCIDs. _(cited in 10/10 runs: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)_
- [Documentation contribution guide](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/doc/contributing.md): Documentation files are under CC-BY-4.0 and contributors can build docs with `pixi run build-docs site` or preview with `mkdocs serve`. _(cited in 4/10 runs: 2, 5, 6, 10)_
- [Release workflow](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/release.yaml): Triggered on version tags v*.*.* and updates DAGs in documentation before preparing the release commit/tag. _(cited in 3/10 runs: 1, 5, 8)_
- [Repository metadata homepage](https://github.com/pypsa/pypsa-eur): Repository metadata lists homepage as https://pypsa-eur.readthedocs.io/. _(cited in 2/10 runs: 7, 9)_

### Stage 6: Open Verifiability

Average score 68.4 (range 66–73 across 10 runs).

- [CITATION version and repository](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/CITATION.cff): Lists repository https://github.com/pypsa/pypsa-eur and version v2026.02.0. _(cited in 10/10 runs: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)_
- [Data versions validation](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/test/test_data_versions_layer.py): Validates dataset/version/source/tag/date/URL metadata and enforces latest-version consistency across sources. _(cited in 10/10 runs: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)_
- [README source and output context](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/README.md): Connects the PyPSA-Eur model to major data sources, open-source Snakemake workflow, documentation, Zenodo DOIs, release badge, limitations, and example publications. _(cited in 9/10 runs: 1, 2, 3, 4, 5, 7, 8, 9, 10)_
- [SHA-tagged image workflow](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/push-images.yaml): Builds or re-tags development-environment container images using the GitHub commit SHA. _(cited in 9/10 runs: 1, 3, 4, 5, 6, 7, 8, 9, 10)_
- [Test workflow artifacts](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/test.yaml): Runs unit and integration tests and uploads logs, .snakemake/log, and results as artifacts with 3-day retention. _(cited in 8/10 runs: 1, 2, 3, 5, 6, 8, 9, 10)_
- [Release workflow](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/release.yaml): Release workflow triggers on tags `v*.*.*`, checks release preparation commits, updates DAGs in documentation, removes/recreates tags, and commits release-preparation changes. _(cited in 5/10 runs: 2, 4, 6, 7, 10)_
- [Config schema synchronization test](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/test/test_config_schema.py): Tests that config/config.default.yaml and config/schema.default.json are synchronized with the generated Pydantic schema. _(cited in 1/10 runs: 5)_

## Consolidated limitations across runs

Distinct limitations raised by one or more runs (deduplicated):
- Assessment used only the supplied evidence bundle and did not inspect repository files or documentation pages not included in the bundle.
- The evidence bundle omits central reproducibility artifacts such as Snakefile, rules, scenario configuration files, pixi.lock, data/versions.csv contents, complete outputs, and release notes.
- Input-data licensing, primary-data lineage, quality-control procedures, and quantified uncertainties are only partially evidenced.
- No specific environmental claim was supplied, so stage 6 was assessed against the project’s general ability to link claims to evidence rather than a concrete claim-level provenance chain.
- The GitHub metadata reports license as null, while CITATION.cff declares MIT and individual files contain SPDX headers; this inconsistency could not be resolved from the supplied evidence.
- Evidence of community review is mostly infrastructural; actual issue discussions, pull-request reviews, correction histories, and replication records were not provided.
- Assessment used only the supplied evidence bundle and did not inspect live repository files beyond the provided artifacts.
- The evidence bundle omits the root LICENSE file; licensing is inferred from CITATION.cff and SPDX headers, while GitHub metadata reports `license: null`.
- The full `data/versions.csv`, `pixi.lock`, Snakefile, Snakemake rules, model scripts, default/test configuration files, generated outputs, and ReadTheDocs pages are not included in the bundle.
- No claim-specific environmental result was supplied, so Stage 6 evaluates the project’s traceability infrastructure rather than a complete evidence chain for a specific claim.
- The bundle includes workflow definitions but not actual CI run logs, validation reports, issue discussions, pull-request reviews, correction records, or peer-review reports.
- Input-data uncertainty and licensing are only partially evidenced; complete provenance back to primary measurements is not demonstrated for all datasets.
- The assessment uses only the supplied evidence bundle and does not inspect files or web pages not included in that bundle.
- The actual data/versions.csv is referenced through tests but not supplied, limiting assessment of real dataset version coverage.
- The Snakefile, workflow rules, scenario configurations, solver settings, and full model scripts are not included in the bundle, limiting execution traceability assessment.
- The bundle links to ReadTheDocs, Zenodo DOI records, and papers but does not include their contents, licenses, version histories, or review records.
- GitHub issue and pull-request contents are not supplied, so community review is assessed from process documentation, counts, and workflows rather than actual discussions or corrections.
- No specific environmental claim or published result is supplied with its exact input datasets, code version, configuration, workflow run logs, and outputs, limiting the Open Verifiability score.
- Repository metadata reports license: null even though CITATION.cff and file headers provide license evidence; this inconsistency prevents a perfect open-source score.
- The evidence bundle covers selected repository files only and does not include the full documentation site, full codebase, full Snakemake workflow, or complete configuration files.
- The actual `data/versions.csv` is not included, so dataset-version traceability can only be assessed from tests that validate its schema, not from its contents.
- No specific environmental claim, scenario result, publication figure, or dashboard output was supplied for end-to-end tracing.
- No concrete GitHub issue threads, pull-request reviews, correction notices, or peer-review reports were included, only mechanisms for such review.
- No workflow run logs, execution artifacts, solver settings, full parameter sets, or output data files were included for reproducing a specific reported result.
- Repository metadata reports no detected license, while CITATION.cff and SPDX headers provide license evidence; the full license file was not supplied in the bundle.
- The assessment uses only the supplied evidence bundle and did not inspect repository files, issues, pull requests, releases, Zenodo records, documentation pages, or publications beyond the provided excerpts.
- The evidence bundle does not include the actual data/versions.csv file, full input datasets, dataset licenses, or quantified uncertainty metadata for most input sources.
- The bundle does not include a top-level LICENSE file, pixi.toml, pixi.lock, full Snakemake rules, scenario configuration files, or full documentation pages, although several artifacts refer to them.
- No specific environmental claim, model scenario, publication figure, or reported numerical output was supplied, so claim-specific traceability could not be verified.
- No persistent execution record with exact input versions, code commit, solver settings, logs, checksums, and outputs was included.
- The evidence shows public review mechanisms, but not concrete examples of issue resolution, pull-request review, correction notices, peer-review reports, or governance decisions.
- Assessment used only the supplied evidence bundle and did not inspect live repository files beyond the provided artifact text.
- The bundle does not include the full LICENSE file, Snakefile, rules, pixi.toml, pixi.lock, config files, data/versions.csv, release notes, or complete documentation pages.
- No specific environmental claim or published model result was supplied, so verifiability was assessed at the project/evidence-chain level rather than for a precise claim-output pair.
- The evidence includes references to Zenodo records, documentation pages, papers, and limitations pages, but their contents were not part of the bundle and were not independently evaluated.
- Scores are conservative where upstream dataset licences, primary-data uncertainty estimates, exact transformation provenance, and archived run artifacts were not visible in the evidence bundle.
- Assessment uses only the supplied evidence bundle and did not inspect live repository contents beyond the listed artifacts.
- The evidence bundle does not include key files such as the top-level LICENSE, Snakefile, rules directory, pixi.toml, pixi.lock, data/versions.csv, full configuration files, release notes, or generated documentation pages.
- No complete archived workflow run or result package was supplied that links a specific environmental claim to exact inputs, parameters, code version, computational environment, logs, and outputs.
- The actual GitHub issue and pull-request discussions were not included, so community review quality was inferred from documented processes and metadata rather than observed review records.
- Input-data uncertainties, primary-source licenses, and source-by-source provenance could not be fully verified for all datasets from the provided artifacts.
- The assessment uses only the supplied evidence bundle and does not inspect the live repository beyond the provided artifacts.
- The top-level LICENSE file, full ReadTheDocs documentation, full Snakefile/rules, configuration files, and data/versions.csv contents were not included in the bundle.
- The evidence does not provide complete primary-source licences, uncertainty estimates, or quality-control records for all input datasets.
- The evidence does not include a specific published model result with its exact input versions, configuration, run logs, solver settings, output files, and review history.
- GitHub metadata reports license=null, while CITATION.cff and SPDX headers indicate MIT/CC licences; this discrepancy could not be resolved from the bundle.
- CI artifacts shown in the test workflow have short retention, limiting long-term external verification of specific runs.
- The assessment uses only the supplied evidence bundle; referenced ReadTheDocs documentation, releases, Zenodo records, papers, issue discussions, pull requests, and full source tree were not inspected unless included in the bundle.
- The actual data/versions.csv file is not supplied, so the existence of a schema for data-version tracking could be assessed but not the completeness or correctness of the tracked dataset versions.
- The evidence bundle does not include a complete LICENSE file, although CITATION.cff and SPDX headers provide licensing evidence.
- No specific published environmental claim or scenario result was supplied with its exact datasets, configuration, solver settings, workflow run ID, output artifacts, and review history, limiting the Open Verifiability score.
- Quantified measurement uncertainties, quality-control procedures, and reuse licences are not evidenced for all primary and secondary input datasets.
- CI artifacts are described with short retention in the workflow, so long-term reproducibility of specific CI executions is not fully evidenced.
- The assessment uses only the supplied evidence bundle and did not inspect files or web pages not included in that bundle.
- The full source tree, Snakefile/rules, configuration files, `pixi.lock`, generated DAGs, outputs, logs, and run records were not supplied.
- The actual `data/versions.csv` was not supplied, so dataset-version coverage can only be inferred from validation tests, not verified directly.
- Primary datasets and their licences, access conditions, measurement methods, quality controls, and quantified uncertainties were not supplied for all named sources.
- The supplied evidence does not include actual issue discussions, pull-request review records, correction notices, governance records, or external replication attempts.
- The cited documentation site, Zenodo records, and Joule papers were referenced in the README but their contents were not included in the bundle.
- No explicit end-to-end provenance manifest was supplied linking a particular environmental claim or result to exact data versions, code commit, environment, workflow run, outputs, review artifacts, and publication.
