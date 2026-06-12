# Open Traceability Assessment Report

- Project/report URL: https://github.com/pypsa-meets-earth/pypsa-earth
- Assessment definition URL: https://raw.githubusercontent.com/protontypes/open-traceability/refs/heads/main/docs/definition.md
- Model: gpt-5.5
- Number of runs: 5

## Final single-paragraph summary

Across 5 independent assessment runs, the project appears strongest on Open-Source Models, Methods, and Software with an average score of 86.0, and weakest on Open Input Data and Measurement Evidence with an average score of 54.4. The average total score across runs is 71.6. The scores should be interpreted as evidence-bundle-based traceability estimates rather than scientific validation: high scores indicate externally inspectable artifacts and linkages, while lower scores indicate missing, implicit, or insufficiently versioned evidence in the collected material.

## Score table across runs

| Stage | Stage name | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Average | Std dev |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Open Input Data and Measurement Evidence | 55 | 52 | 55 | 54 | 56 | 54.4 | 1.4 |
| 2 | Open-Source Models, Methods, and Software | 86 | 84 | 86 | 88 | 86 | 86.0 | 1.3 |
| 3 | Open Execution and Reproducibility | 78 | 72 | 76 | 78 | 78 | 76.4 | 2.3 |
| 4 | Open Community and Review | 74 | 68 | 73 | 74 | 73 | 72.4 | 2.2 |
| 5 | Open Publications and Communication | 80 | 78 | 82 | 79 | 79 | 79.6 | 1.4 |
| 6 | Open Linkage | 63 | 58 | 60 | 62 | 62 | 61.0 | 1.8 |

## Total score

| Run | Total score |
| --- | ---: |
| 1 | 73 |
| 2 | 69 |
| 3 | 72 |
| 4 | 72 |
| 5 | 72 |

Average total score: **71.6**; population standard deviation: **1.4**.

## Consolidated references by stage

References cited across all runs, deduplicated by URL. The runs that cited each reference are noted in parentheses; references cited by more runs appear first. References marked ⚠️ point to a URL that was not part of the collected evidence bundle and could not be verified (the model may have introduced them).

### Stage 1: Open Input Data and Measurement Evidence

Average score 54.4 (range 52–56 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 5, high 0).

- [README.md](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/README.md): States that all data needed for a simulation are automatically and flexibly retrieved from open sources, including energy demand, generation capacities, networks, and renewable energy potentials. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Contributing guide](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/doc/community/contributing.md): Encourages contribution of new datasets, suggests uploading datasets to public storage such as Zenodo, and adding specifications to configs/bundle_config.yaml. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Repository description](https://github.com/pypsa-meets-earth/pypsa-earth): Repository topics and description identify PyPSA-Earth as an open optimisation model for global energy-system futures and scenario analysis. _(cited in 2/5 runs: 2, 3)_

### Stage 2: Open-Source Models, Methods, and Software

Average score 86.0 (range 84–88 across 5 runs). Reported uncertainty: mostly low (low 5, medium 0, high 0).

- [GitHub repository metadata](https://github.com/pypsa-meets-earth/pypsa-earth): Public repository described as 'PyPSA-Earth: A flexible Python-based open optimisation model to study energy system futures around the world.' _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [README.md](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/README.md): README includes an AGPL v3 licence badge and describes PyPSA-Earth as an open-source global energy system model. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [CITATION.cff](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/CITATION.cff): SPDX-License-Identifier: AGPL-3.0-or-later; repository-code points to the GitHub repository; version 1.0.0 and release date are given. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [envs/environment.yaml](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/envs/environment.yaml): Lists Python version constraints and many model dependencies including pypsa, atlite, snakemake-minimal, geopandas, xarray, glpk, and gurobi. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Dockerfile](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/Dockerfile): Builds from condaforge/mambaforge, creates a pypsa-earth conda environment from envs/linux-64.lock.yaml, and activates it. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_

### Stage 3: Open Execution and Reproducibility

Average score 76.4 (range 72–78 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 5, high 0).

- [Test workflow](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/.github/workflows/test.yml): Runs tests on ubuntu, macos, and windows; sets up conda environments from lock files or the base environment; runs make test; uploads logs and results; extracts objective-function values from solver logs. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Update locked environments workflow](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/.github/workflows/update-locked-env.yml): Generates conda lockfiles for linux-64, osx-64, win-64, and osx-arm64 using conda-lock and creates a pull request with updated locked environments. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Objective extraction utility](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/test/utils/extract_ref_objective.py): Reads test/utils/obj_ref.csv and returns reference objective values for named run folders and log files. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Update reference objectives workflow](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/.github/workflows/update-ref-objectives.yml): Manual workflow runs tests, extracts objective values from logs, writes updated_obj_ref.csv, and creates a pull request to update test/utils/obj_ref.csv. _(cited in 4/5 runs: 1, 2, 3, 5)_
- [Dockerfile](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/Dockerfile): The Dockerfile creates a pypsa-earth conda environment from temp/linux-64.lock.yaml and configures the container to run with that environment. _(cited in 4/5 runs: 2, 3, 4, 5)_
- [Configuration snippets README](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/doc/configtables/snippets/README.md): Explains that documentation snippets are extracted from config.default.yaml so configuration examples stay in sync with the actual config file. _(cited in 3/5 runs: 1, 3, 4)_

### Stage 4: Open Community and Review

Average score 72.4 (range 68–74 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 5, high 0).

- [GitHub repository metadata](https://github.com/pypsa-meets-earth/pypsa-earth): Repository has open_issues_count: 298. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Contributing guide](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/doc/community/contributing.md): Invites contributors to submit questions and feedback, propose features, report bugs, submit fixes, improve documentation, share regional modelling insights, and contribute datasets. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [README.md](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/README.md): Includes a Discord badge/link and states that the initiative looks for users, co-developers, and leaders. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Lint workflow](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/.github/workflows/lint.yml): Runs pre-commit checks, docstring coverage reporting, and mypy type checking on pull requests to main. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [CodeQL workflow](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/.github/workflows/codeql.yml): Runs CodeQL analysis on push, pull_request, and scheduled events for Python. _(cited in 3/5 runs: 1, 2, 3)_
- [Publication metadata](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/CITATION.cff): CITATION.cff identifies an Applied Energy article with DOI 10.1016/j.apenergy.2023.121096. _(cited in 1/5 runs: 4)_

### Stage 5: Open Publications and Communication

Average score 79.6 (range 78–82 across 5 runs). Reported uncertainty: mostly medium (low 2, medium 3, high 0).

- [README.md](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/README.md): Links to documentation at pypsa-earth.readthedocs.io and lists Applied Energy publications with DOIs 10.1016/j.apenergy.2023.121096 and 10.1016/j.apenergy.2025.125316. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [CITATION.cff](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/CITATION.cff): Provides title, abstract, repository-code URL, version 1.0.0, release date 2023-04-18, DOI 10.1016/j.apenergy.2023.121096, and author metadata. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Docs workflow](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/.github/workflows/docs.yml): Builds documentation with mkdocs build --strict and checks spelling on pull requests affecting docs and markdown files. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Documentation requirements](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/doc/requirements.txt): Lists MkDocs, mkdocs-material, mkdocstrings, table-reader, git-revision-date plugin, and other documentation dependencies. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Contributing documentation licence](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/doc/community/contributing.md): The contributing page includes SPDX-License-Identifier: CC-BY-4.0. _(cited in 1/5 runs: 4)_
- [Configuration snippets documentation](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/doc/configtables/snippets/README.md): Snippet README explains that YAML snippets are extracted from config.default.yaml so documentation pages stay in sync with the actual config file. _(cited in 1/5 runs: 5)_

### Stage 6: Open Linkage

Average score 61.0 (range 58–63 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 5, high 0).

- [CITATION.cff](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/CITATION.cff): Links the Applied Energy paper metadata to repository-code https://github.com/pypsa-meets-earth/pypsa-earth, version 1.0.0, and release date 2023-04-18. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [README.md](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/README.md): Connects model claims to documentation, DOI publications, PyPSA-Earth-Status, Discord, and Google Drive links. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Test workflow](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/.github/workflows/test.yml): Builds environments from specific environment files, runs make test, uploads logs/results, and extracts objective-function values from solver logs. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Configuration snippets README](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/doc/configtables/snippets/README.md): Configuration documentation snippets are extracted from config.default.yaml so documentation examples stay in sync with actual config. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Update reference objectives workflow](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/.github/workflows/update-ref-objectives.yml): Extracts objective values from a manual CI run and creates a pull request updating test/utils/obj_ref.csv. _(cited in 3/5 runs: 1, 3, 4)_
- [Update locked environments workflow](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/.github/workflows/update-locked-env.yml): The workflow generates and updates lock files for multiple platforms and creates pull requests for those changes. _(cited in 2/5 runs: 2, 5)_
- [Reference objective utility](https://raw.githubusercontent.com/pypsa-meets-earth/pypsa-earth/main/test/utils/extract_ref_objective.py): extract_obj_for_path maps a run folder and log file to an objective value in test/utils/obj_ref.csv. _(cited in 1/5 runs: 5)_

## Consolidated limitations across runs

Distinct limitations raised by one or more runs (deduplicated):
- The assessment uses only the supplied evidence bundle and does not inspect repository files or documentation pages not included in the bundle.
- The bundle does not include a top-level LICENSE file, although multiple SPDX headers and README badges indicate AGPL-3.0-or-later or other open licences for specific files.
- The bundle does not include the actual data-source registry, bundle_config.yaml, dataset DOIs, data licences, primary measurement methods, quality controls, or uncertainty estimates.
- The bundle does not include complete reproduction instructions or archived workflow records for the Applied Energy publication results.
- The bundle does not include examples of actual issue discussions, pull-request reviews, correction notices, governance records, or peer-review reports.
- The GitHub test workflow evidence is truncated, so some details of the testing and objective-comparison process may be incomplete.
- Dynamic resources mentioned in the README, such as PyPSA-Earth-Status or Google Drive materials, were not assessed because their contents were not provided.
- The assessment uses only the supplied evidence bundle and did not inspect repository files, documentation pages, issues, pull requests, releases, or papers beyond the provided excerpts.
- The evidence bundle does not include the actual data-source catalogue, bundle_config.yaml, input-data licenses, primary dataset identifiers, measurement methods, uncertainty estimates, or quality-control documentation.
- The evidence bundle does not include the full model code, Snakefile, configuration files, example scenarios, or complete method documentation, so method inspectability is inferred from repository and environment evidence.
- The evidence bundle includes CI workflow definitions but not actual successful workflow run logs, run IDs, artifacts, or archived outputs for published results.
- The evidence bundle identifies journal publications by DOI but does not include their full text, licensing/open-access status, peer-review reports, or detailed artifact citations.
- Open community evidence is limited to metadata, contribution guidance, and workflow files; actual issue discussions, pull-request reviews, governance records, correction notices, and replication attempts were not supplied.
- Open Linkage scoring is limited because no specific environmental claim was provided with an exact chain to datasets, code commit, configuration, workflow execution, review record, and publication output.
- The evidence bundle does not include the full data-source registry, `configs/bundle_config.yaml`, or concrete dataset metadata, so input-data provenance, licensing, uncertainty, and primary-data traceability could not be fully assessed.
- The evidence bundle does not include a LICENSE file, although README badges and SPDX headers indicate AGPL-3.0-or-later and Creative Commons licensing for specific files.
- The full documentation site, model-method pages, configuration files, Snakefile, and example workflows were not supplied, limiting assessment of method completeness and end-to-end reproducibility.
- No complete published-result reproduction package was provided linking a specific claim, figure, or table to exact input data versions, code commit/tag, configuration, solver settings, run logs, and outputs.
- GitHub Actions logs and uploaded artifacts were not inspected; the test workflow says artifacts are retained for 3 days, which limits long-term external verification of CI run outputs.
- Issue discussions, pull-request reviews, governance records, correction notices, and peer-review reports were not included, so community review was assessed mainly from open channels and automated checks rather than actual review content.
- The full papers linked by DOI were not included in the evidence bundle, so publication access conditions, licensing, and detailed methods in the articles could not be verified.
- The bundle does not include the actual data-source catalogue, bundle_config.yaml, dataset URLs, dataset licences, primary measurement methods, quality-control records, or uncertainty estimates.
- The evidence does not include specific published result configurations, scenario files, input-data snapshots, archived workflow runs, or output archives for the DOI-linked papers.
- GitHub repository metadata reports license as null even though README and file headers show AGPL/CC SPDX licensing signals; this inconsistency limits certainty about repository-level licensing metadata.
- The evidence shows public issue counts and contribution channels but not the substance of issue discussions, pull-request reviews, peer-review reports, correction notices, or replication attempts.
- The openness and licensing status of the external Applied Energy publications themselves are not shown in the evidence bundle.
- Dynamic outputs such as PyPSA-Earth-Status are mentioned but their data sources, update cycles, indicator definitions, and version history are not included.
- The assessment used only the supplied evidence bundle; it did not inspect repository files, documentation pages, issues, pull requests, releases, data bundles, or publications beyond the provided excerpts.
- The actual data-source catalogue, configs/bundle_config.yaml, dataset metadata, licences, provenance, primary-data links, transformations, uncertainty estimates, and quality-control procedures were not supplied.
- The evidence does not include exact workflow runs, scenario configurations, input-data versions, archived outputs, or computational notebooks corresponding to the cited Applied Energy claims.
- The full LICENSE file was not supplied, and GitHub metadata in the bundle reports license as null despite SPDX and README/CITATION licence statements.
- Issue and pull-request contents, governance records, correction notices, peer-review reports, and replication attempts were not included, limiting assessment of community review depth.
- The full ReadTheDocs documentation and full publication accessibility/licensing terms were not supplied, so publication and communication scoring relies on repository references rather than complete inspection.
- Some evidence artifacts are truncated, especially README.md and test.yml, which may omit relevant details. The scoring therefore remains conservative where direct evidence is incomplete.
