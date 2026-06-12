# Open Traceability Assessment Report

- Project/report URL: https://github.com/pypsa/pypsa-eur
- Assessment definition URL: https://raw.githubusercontent.com/protontypes/open-traceability/refs/heads/main/docs/definition.md
- Model: gpt-5.5
- Number of runs: 4

## Final single-paragraph summary

Across 4 independent assessment runs, the project appears strongest on Open-Source Models, Methods, and Software with an average score of 87.0, and weakest on Open Linkage with an average score of 66.2. The average total score across runs is 77.0. The scores should be interpreted as evidence-bundle-based traceability estimates rather than scientific validation: high scores indicate externally inspectable artifacts and linkages, while lower scores indicate missing, implicit, or insufficiently versioned evidence in the collected material.

## Score table across runs

| Stage | Stage name | Run 1 | Run 2 | Run 3 | Run 4 | Average | Std dev |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Open Input Data and Measurement Evidence | 72 | 76 | 74 | 74 | 74.0 | 1.4 |
| 2 | Open-Source Models, Methods, and Software | 88 | 88 | 84 | 88 | 87.0 | 1.7 |
| 3 | Open Execution and Reproducibility | 78 | 82 | 76 | 76 | 78.0 | 2.4 |
| 4 | Open Community and Review | 76 | 79 | 77 | 77 | 77.2 | 1.1 |
| 5 | Open Publications and Communication | 73 | 83 | 80 | 83 | 79.8 | 4.1 |
| 6 | Open Linkage | 64 | 68 | 69 | 64 | 66.2 | 2.3 |

## Total score

| Run | Total score |
| --- | ---: |
| 1 | 75 |
| 2 | 79 |
| 3 | 77 |
| 4 | 77 |

Average total score: **77.0**; population standard deviation: **1.4**.

## Sources followed during the assessment

Every URL that was actually fetched and supplied to the model as evidence. This covers the project repository, its GitHub namespace, and each individual file, documentation page, or linked resource that was followed. Scores and references below are derived only from these sources.

- Project/report URL followed: [https://github.com/pypsa/pypsa-eur](https://github.com/pypsa/pypsa-eur)
- Assessment definition URL followed: [https://raw.githubusercontent.com/protontypes/open-traceability/refs/heads/main/docs/definition.md](https://raw.githubusercontent.com/protontypes/open-traceability/refs/heads/main/docs/definition.md)

A total of 21 source artifact(s) were followed across 2 host(s).

### github.com

- [GitHub repository metadata](https://github.com/pypsa/pypsa-eur)

### raw.githubusercontent.com

- [CITATION.cff](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/CITATION.cff)
- [README.md](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/README.md)
- [doc/contributing.md](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/doc/contributing.md)
- [envs/environment.yaml](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/envs/environment.yaml)
- [test/__init__.py](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/test/__init__.py)
- [test/conftest.py](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/test/conftest.py)
- [test/test_base_network.py](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/test/test_base_network.py)
- [test/test_build_powerplants.py](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/test/test_build_powerplants.py)
- [test/test_build_shapes.py](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/test/test_build_shapes.py)
- [test/test_config_schema.py](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/test/test_config_schema.py)
- [test/test_data_versions_layer.py](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/test/test_data_versions_layer.py)
- [.github/workflows/codeql.yaml](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/codeql.yaml)
- [.github/workflows/push-images.yaml](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/push-images.yaml)
- [.github/workflows/release.yaml](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/release.yaml)
- [.github/workflows/security-scan.yaml](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/security-scan.yaml)
- [.github/workflows/test.yaml](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/test.yaml)
- [.github/workflows/update-lockfile.yaml](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/update-lockfile.yaml)
- [.github/workflows/validate.yaml](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/validate.yaml)
- [data/entsoegridkit/README.md](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/data/entsoegridkit/README.md)
- [docker/dev-env/Dockerfile](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/docker/dev-env/Dockerfile)

## Consolidated references by stage

References cited across all runs, deduplicated by URL. The runs that cited each reference are noted in parentheses; references cited by more runs appear first. References marked ⚠️ point to a URL that was not part of the collected evidence bundle and could not be verified (the model may have introduced them).

### Stage 1: Open Input Data and Measurement Evidence

Average score 74.0 (range 72–76 across 4 runs). Reported uncertainty: mostly medium (low 0, medium 4, high 0).

- [README data sources](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/README.md): States that PyPSA-Eur is built from open data using a Snakemake workflow and lists sources including OpenStreetMap, powerplantmatching, ENTSO-E Transparency Platform, ERA5/SARAH-3 via atlite, Eurostat, and JRC-IDEES. _(cited in 4/4 runs: 1, 2, 3, 4)_
- [ENTSO-E/GridKit dataset README](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/data/entsoegridkit/README.md): Documents that the dataset was generated from a March 2022 ENTSO-E interactive-map extract processed by GridKit, lists CSV contents and fields, and warns about inaccuracies such as approximate coordinates and inferred transformers. _(cited in 4/4 runs: 1, 2, 3, 4)_
- [Data versions validation test](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/test/test_data_versions_layer.py): Defines schema checks for `data/versions.csv`, including dataset, version, source, tags, added date, URL, archive URL requirements, and consistency of latest versions across sources. _(cited in 4/4 runs: 1, 2, 3, 4)_

### Stage 2: Open-Source Models, Methods, and Software

Average score 87.0 (range 84–88 across 4 runs). Reported uncertainty: mostly low (low 3, medium 1, high 0).

- [Repository metadata](https://github.com/pypsa/pypsa-eur): Repository is public-facing as `PyPSA/pypsa-eur`, described as `A Sector-Coupled Open Optimisation Model of the European Energy System`, with default branch `master` and many energy-system topics; metadata license field is null. _(cited in 4/4 runs: 1, 2, 3, 4)_
- [CITATION.cff](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/CITATION.cff): Specifies title, repository URL, version `v2026.02.0`, licence `MIT`, and author ORCIDs. _(cited in 4/4 runs: 1, 2, 3, 4)_
- [Environment file](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/envs/environment.yaml): Lists conda channels and dependencies such as pypsa, snakemake-minimal, atlite, linopy, geopandas, pandas, xarray, and solver packages. _(cited in 4/4 runs: 1, 2, 3, 4)_
- [Docker development environment](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/docker/dev-env/Dockerfile): Defines a development container based on pixi, installs from `pixi.toml` and `pixi.lock`, and labels the image source as the GitHub repository. _(cited in 4/4 runs: 1, 2, 3, 4)_
- [README open-source workflow statement](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/README.md): The README states that the model is built from open data using a Snakemake workflow and is fully open source, designed for import into PyPSA. _(cited in 2/4 runs: 2, 3)_

### Stage 3: Open Execution and Reproducibility

Average score 78.0 (range 76–82 across 4 runs). Reported uncertainty: mostly medium (low 0, medium 4, high 0).

- [README workflow statement](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/README.md): States that the model is built from open data using a Snakemake workflow and is fully open source. _(cited in 4/4 runs: 1, 2, 3, 4)_
- [GitHub test workflow](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/test.yaml): Runs unit tests and integration tests on pushes, pull requests, schedules, and manual dispatch; integration tests call `pixi run integration-tests` and upload logs, `.snakemake/log`, and results artifacts for 3 days. _(cited in 4/4 runs: 1, 2, 3, 4)_
- [Environment specification](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/envs/environment.yaml): Declares the conda environment name and extensive dependency list with version constraints. _(cited in 3/4 runs: 1, 2, 3)_
- [Image build workflow](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/push-images.yaml): Builds and pushes `ghcr.io/pypsa/eur-dev-env` images tagged with the GitHub commit SHA and `latest` on master. _(cited in 2/4 runs: 1, 4)_
- [Development container](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/docker/dev-env/Dockerfile): Builds a pixi-based development container from pixi.toml and pixi.lock and installs the default environment. _(cited in 2/4 runs: 2, 3)_
- [Validator workflow](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/validate.yaml): For pull requests from the same repository, a pypsa-validator action runs self-hosted validation using envs/environment.yaml and config/test/config.validator.yaml, then can create a report with plots such as energy, costs, and balances graphs. _(cited in 2/4 runs: 2, 4)_
- [Config schema synchronization tests](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/test/test_config_schema.py): Tests that config/config.default.yaml and config/schema.default.json are in sync with a generated Pydantic schema. _(cited in 1/4 runs: 3)_

### Stage 4: Open Community and Review

Average score 77.2 (range 76–79 across 4 runs). Reported uncertainty: mostly medium (low 0, medium 4, high 0).

- [Repository metadata issues](https://github.com/pypsa/pypsa-eur): Repository metadata reports `open_issues_count: 256`. _(cited in 4/4 runs: 1, 2, 3, 4)_
- [Contributing guide](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/doc/contributing.md): Invites contributions via issues and pull requests, points to `help wanted` issues, links a Discord server, and states that all code follows the four-eyes principle with review by a second person before incorporation. _(cited in 4/4 runs: 1, 2, 3, 4)_
- [Security scan workflow](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/security-scan.yaml): Generates an SBOM and vulnerability scan, uploads SARIF, and fails fork PRs on new high-severity CVEs relative to master. _(cited in 4/4 runs: 1, 2, 3, 4)_
- [Validation workflow](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/validate.yaml): Runs a PyPSA validator on pull requests from the same repository and can create a validation report comment with specified result plots. _(cited in 2/4 runs: 1, 3)_
- [CodeQL workflow](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/codeql.yaml): CodeQL analysis runs on pushes, pull requests, and a weekly schedule for Python. _(cited in 2/4 runs: 2, 4)_
- [Test workflow](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/test.yaml): Runs unit tests, integration tests, pylint checks, and Snakemake test workflows on pushes, pull requests, schedules, and manual dispatch. _(cited in 1/4 runs: 3)_

### Stage 5: Open Publications and Communication

Average score 79.8 (range 73–83 across 4 runs). Reported uncertainty: mostly low (low 2, medium 2, high 0).

- [README communication and warnings](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/README.md): Describes model coverage, included sectors and networks, provides diagrams, links documentation, Zenodo DOIs, papers, issues, and states that PyPSA-Eur is under active development with limitations users should understand. _(cited in 4/4 runs: 1, 2, 3, 4)_
- [CITATION.cff](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/CITATION.cff): Provides citation title, version `v2026.02.0`, repository, licence, and authors with ORCIDs. _(cited in 4/4 runs: 1, 2, 3, 4)_
- [Contributing documentation licence](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/doc/contributing.md): The contributing page carries SPDX-License-Identifier: CC-BY-4.0 and explains how to build documentation with pixi and mkdocs. _(cited in 3/4 runs: 2, 3, 4)_
- [Repository homepage metadata](https://github.com/pypsa/pypsa-eur): Repository metadata lists homepage `https://pypsa-eur.readthedocs.io/`. _(cited in 2/4 runs: 1, 2)_

### Stage 6: Open Linkage

Average score 66.2 (range 64–69 across 4 runs). Reported uncertainty: mostly medium (low 0, medium 4, high 0).

- [README source and publication links](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/README.md): Links releases, documentation, test workflow, Zenodo DOIs, Discord, input datasets, limitations, issues, and showcase papers from the project overview. _(cited in 4/4 runs: 1, 2, 3, 4)_
- [CITATION version linkage](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/CITATION.cff): Identifies repository `https://github.com/pypsa/pypsa-eur` and version `v2026.02.0`. _(cited in 4/4 runs: 1, 2, 3, 4)_
- [Data versions validation layer](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/test/test_data_versions_layer.py): Validates `data/versions.csv` fields for dataset, version, source, tags, added date, note, and URL, including archive URL requirements and latest-version consistency. _(cited in 4/4 runs: 1, 2, 3, 4)_
- [Release workflow](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/release.yaml): On version tags, validates/creates a release-preparation commit, runs `pixi run update-dags`, deletes and recreates the tag, and commits generated release changes. _(cited in 3/4 runs: 1, 2, 3)_
- [Image SHA tagging workflow](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/push-images.yaml): Builds or retags development-environment images as `ghcr.io/pypsa/eur-dev-env:${{ github.sha }}`. _(cited in 3/4 runs: 1, 3, 4)_
- [Test workflow execution artifacts](https://raw.githubusercontent.com/pypsa/pypsa-eur/master/.github/workflows/test.yaml): Integration tests run Snakemake test workflows and upload logs, .snakemake/log, and results artifacts. _(cited in 1/4 runs: 2)_

## Consolidated limitations across runs

Distinct limitations raised by one or more runs (deduplicated):
- The assessment uses only the supplied evidence bundle and does not inspect repository files or documentation pages not included in the bundle.
- The bundle omits central files that would affect scoring, such as the main Snakefile, `pixi.toml`/`pixi.lock`, root LICENSE file, `data/versions.csv`, full configuration files, release artifacts, and ReadTheDocs content.
- GitHub repository metadata reports `license: null`, while CITATION.cff and SPDX headers indicate MIT/CC licences; the assessment treats this as a licensing metadata inconsistency rather than resolving it externally.
- No specific environmental claim or publication result was supplied, so Stage 6 linkage was assessed at the project-infrastructure level rather than for a concrete claim-to-evidence chain.
- The evidence shows tests and CI workflows but not their current pass/fail status, durable logs, or the outputs of actual workflow runs beyond workflow definitions.
- The bundle includes references to peer-reviewed papers and Zenodo DOIs but not the paper texts, peer-review records, or archived release contents.
- The assessment uses only the supplied evidence bundle; it does not inspect files or web pages not included in the bundle, such as the full documentation site, full Snakefile/rules, actual data/versions.csv contents, release pages, Zenodo records, issue threads, pull-request reviews, or published papers.
- The GitHub metadata reports license as null, while CITATION.cff and SPDX headers indicate MIT/Creative Commons licensing; without the top-level LICENSE file in the bundle, licensing completeness cannot be fully verified.
- The evidence does not include a specific completed model run or scenario result, so execution and linkage scores are based on reproducibility infrastructure rather than verified reproduction of a particular reported claim.
- Input-data assessment is limited because the bundle lists and partly documents major datasets but does not include full upstream provenance, licences, uncertainty estimates, quality-control results, or primary-measurement traceability for every source.
- Community and review assessment is limited because mechanisms are documented, but concrete review discussions, correction histories, governance records, or peer-review reports are not included.
- The assessment uses only the supplied evidence bundle and does not inspect files or pages not included in that bundle.
- The actual data/versions.csv file is referenced by tests but not supplied, so dataset-version coverage could not be verified directly.
- The core Snakefile, scenario configuration files, model scripts, and run instructions are not included in the evidence bundle, limiting assessment of exact execution traceability.
- The top-level LICENSE file is not supplied and GitHub metadata reports a null licence, despite MIT/CC SPDX and CITATION evidence.
- The Zenodo records, ReadTheDocs documentation pages, GitHub releases, issue/PR discussions, and cited papers are linked but their contents are not included in the bundle.
- No specific environmental claim or published numerical result was supplied, so Open Linkage was assessed at project level rather than claim-level provenance.
- Quantified uncertainty/error metadata for all primary and secondary input datasets is not demonstrated in the supplied evidence.
- The evidence bundle does not include the root LICENSE file, pixi.lock, Snakefile, rules directory, full configuration files, full documentation pages, release notes, or the actual data/versions.csv.
- Input-data assessment is limited because complete dataset licences, access conditions, source manifests, transformations, and quantified uncertainties for all primary inputs are not supplied.
- Execution assessment is limited because no complete run record, logs, solver settings, scenario parameters, or output artifacts for a specific environmental claim are included.
- Community/review assessment is limited because actual issue threads, pull-request reviews, governance records, correction notices, and paper peer-review materials are not included.
- Publication assessment is limited because cited papers and Zenodo records are linked in the README but their full contents, licences, and exact artifact mappings are not included in the bundle.
- Open Linkage is constrained by lack of a concrete claim-level provenance graph connecting exact datasets, code versions, configurations, workflow runs, reviews, and publications.
