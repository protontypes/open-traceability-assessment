# Open Traceability Assessment Report

- Project/report URL: https://github.com/natcap/invest
- Assessment definition URL: https://raw.githubusercontent.com/protontypes/open-traceability/refs/heads/main/docs/definition.md
- Number of runs: 5

## Final single-paragraph summary

Across 5 independent assessment runs, the project appears strongest on Open-Source Models, Methods, and Software with an average score of 89.2, and weakest on Open Input Data and Measurement Evidence with an average score of 41.0. The average total score across runs is 68.4. The scores should be interpreted as evidence-bundle-based traceability estimates rather than scientific validation: high scores indicate externally inspectable artifacts and linkages, while lower scores indicate missing, implicit, or insufficiently versioned evidence in the collected material.

## Score table across runs

| Stage | Stage name | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Average | Std dev |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Open Input Data and Measurement Evidence | 42 | 43 | 34 | 43 | 43 | 41.0 | 3.5 |
| 2 | Open-Source Models, Methods, and Software | 88 | 88 | 90 | 92 | 88 | 89.2 | 1.6 |
| 3 | Open Execution and Reproducibility | 76 | 72 | 72 | 76 | 76 | 74.4 | 2.0 |
| 4 | Open Community and Review | 74 | 68 | 72 | 72 | 69 | 71.0 | 2.2 |
| 5 | Open Publications and Communication | 69 | 74 | 78 | 78 | 74 | 74.6 | 3.3 |
| 6 | Open Verifiability | 60 | 61 | 58 | 60 | 66 | 61.0 | 2.7 |

## Total score

| Run | Total score |
| --- | ---: |
| 1 | 68 |
| 2 | 68 |
| 3 | 67 |
| 4 | 70 |
| 5 | 69 |

Average total score: **68.4**; population standard deviation: **1.0**.

## Consolidated references by stage

References cited across all runs, deduplicated by URL. The runs that cited each reference are noted in parentheses; references cited by more runs appear first.

### Stage 1: Open Input Data and Measurement Evidence

Average score 41.0 (range 34–43 across 5 runs).

- [README data repositories](https://raw.githubusercontent.com/natcap/invest/main/README.md): The README lists related repositories for the InVEST User's Guide, InVEST Sample Data, and InVEST Test Data, including sample data from InVEST 3.7.0-present and test data from InVEST 3.7.0-present. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [SDR test inputs](https://raw.githubusercontent.com/natcap/invest/main/tests/test_sdr.py): The SDR regression tests define inputs including biophysical_table.csv, dem.tif, erodibility, erosivity, landuse, watersheds, and model parameters. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Annual Water Yield test inputs](https://raw.githubusercontent.com/natcap/invest/main/tests/test_annual_water_yield.py): The Annual Water Yield regression tests define input paths for LULC, depth to root restricting layer, precipitation, PAWC, ETo, watersheds, and a biophysical table under data/invest-test-data/annual_water_yield. _(cited in 4/5 runs: 1, 2, 4, 5)_
- [Datastack tests](https://raw.githubusercontent.com/natcap/invest/main/tests/test_datastack.py): Tests exercise building and extracting datastack archives that collect model parameters and input files such as rasters, vectors, and nonspatial files. _(cited in 3/5 runs: 1, 2, 3)_
- [NDR regression inputs](https://raw.githubusercontent.com/natcap/invest/main/tests/test_ndr.py): The NDR test constructs base args with biophysical_table_path, dem_path, lulc_path, runoff_proxy_path, and watersheds_path under data/invest-test-data/ndr. _(cited in 1/5 runs: 4)_
- [Crop production model data paths](https://raw.githubusercontent.com/natcap/invest/main/tests/test_crop_production.py): Crop production tests define model-data and input paths including landcover, crop mapping, climate-bin, observed-yield, nutrient, percentile-yield, and regression-yield CSVs. _(cited in 1/5 runs: 5)_

### Stage 2: Open-Source Models, Methods, and Software

Average score 89.2 (range 88–92 across 5 runs).

- [Repository metadata](https://github.com/natcap/invest): The repository is public as natcap/invest, described as InVEST models that map and value ecosystem services, with license Apache-2.0 and default branch main. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Apache license](https://raw.githubusercontent.com/natcap/invest/main/LICENSE.txt): LICENSE.txt contains the Apache License Version 2.0 terms for use, reproduction, and distribution. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Python project metadata](https://raw.githubusercontent.com/natcap/invest/main/pyproject.toml): pyproject.toml defines project name natcap.invest, Python >=3.10, Apache-2.0 license, maintainers, classifiers, console script invest, and build-system requirements. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Runtime dependencies](https://raw.githubusercontent.com/natcap/invest/main/requirements.txt): requirements.txt records runtime requirements including GDAL, pandas, numpy, scipy, pygeoprocessing, taskgraph, geopandas, matplotlib, and other packages. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Dockerfile](https://raw.githubusercontent.com/natcap/invest/main/docker/Dockerfile): The Dockerfile builds InVEST in a micromamba container, installs conda-forge dependencies, builds a wheel, installs it, and defines an entrypoint. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [CITATION metadata](https://raw.githubusercontent.com/natcap/invest/main/CITATION.cff): CITATION.cff identifies InVEST as software, version 3.20.0, DOI 10.60793/natcap-invest-3.20.0, repository-code URL, release artifact URL, and Apache-2.0 license. _(cited in 2/5 runs: 1, 2)_
- [Build configuration](https://raw.githubusercontent.com/natcap/invest/main/setup.py): setup.py defines compiled Cython/GDAL extension modules for several InVEST model components and platform-specific build configuration. _(cited in 2/5 runs: 3, 5)_

### Stage 3: Open Execution and Reproducibility

Average score 74.4 (range 72–76 across 5 runs).

- [CLI reproducibility tests](https://raw.githubusercontent.com/natcap/invest/main/tests/test_cli.py): CLI tests run models using JSON datastacks, override workspaces, validate error cases, and check that file_registry.json is produced in the workspace. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Datastack archive tests](https://raw.githubusercontent.com/natcap/invest/main/tests/test_datastack.py): Datastack tests build archives from model args and model names, extract archives, validate args, and execute modules from extracted parameter sets. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Docker documentation](https://raw.githubusercontent.com/natcap/invest/main/docker/README.md): The Docker README states that Docker images and digests are published to GitHub Packages and points users to API docs for container usage. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Regression tests for SDR](https://raw.githubusercontent.com/natcap/invest/main/tests/test_sdr.py): The SDR base regression test executes the model with sample data, enables report generation and file registry saving, and checks expected watershed totals and raster outputs. _(cited in 4/5 runs: 1, 3, 4, 5)_
- [Regression tests for Carbon](https://raw.githubusercontent.com/natcap/invest/main/tests/test_carbon.py): The Carbon full model test creates input rasters and carbon-pools CSV, executes the model, and asserts expected raster and report values. _(cited in 4/5 runs: 1, 2, 4, 5)_
- [Development requirements](https://raw.githubusercontent.com/natcap/invest/main/requirements-dev.txt): requirements-dev.txt lists testing and build tools such as pytest, coverage, build, pyinstaller, setuptools_scm, and cython. _(cited in 3/5 runs: 2, 3, 5)_
- [Pytest configuration](https://raw.githubusercontent.com/natcap/invest/main/pyproject.toml): pyproject.toml includes pytest warning configuration and dependency/build metadata; requirements-dev.txt lists pytest, coverage, build, and related development dependencies. _(cited in 1/5 runs: 1)_
- [DelineateIt regression test](https://raw.githubusercontent.com/natcap/invest/main/tests/test_delineateit.py): The test defines explicit args for dem_path, outlet_vector_path, workspace_dir, snap_points, snap_distance, flow_threshold, results_suffix, and n_workers, executes MODEL_SPEC, then asserts expected feature counts and areas. _(cited in 1/5 runs: 2)_
- [Docker build environment](https://raw.githubusercontent.com/natcap/invest/main/docker/Dockerfile): Dockerfile specifies a micromamba Debian base image, Python and GDAL arguments, environment installation, wheel build, package installation, and cleanup. _(cited in 1/5 runs: 3)_

### Stage 4: Open Community and Review

Average score 71.0 (range 68–74 across 5 runs).

- [Repository issue metadata](https://github.com/natcap/invest): Repository metadata reports open_issues_count: 213. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [CONTRIBUTING bug process](https://raw.githubusercontent.com/natcap/invest/main/CONTRIBUTING.md): CONTRIBUTING.md instructs users to search InVEST Open Issues on GitHub and create a new issue using the Bug report template with details. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_

### Stage 5: Open Publications and Communication

Average score 74.6 (range 69–78 across 5 runs).

- [README overview and installation](https://raw.githubusercontent.com/natcap/invest/main/README.md): The README describes InVEST as tools for quantifying values of natural capital, links to the Natural Capital Alliance website, GitHub releases, software downloads, and API documentation. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [CITATION.cff](https://raw.githubusercontent.com/natcap/invest/main/CITATION.cff): CITATION.cff gives title InVEST, version 3.20.0, release date 2026-06-11, DOI 10.60793/natcap-invest-3.20.0, repository code URL, artifact URL, keywords, and an abstract. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Docker README](https://raw.githubusercontent.com/natcap/invest/main/docker/README.md): The Docker README points to published Docker images and to API documentation for container guidance. _(cited in 3/5 runs: 1, 2, 5)_
- [Python package metadata](https://raw.githubusercontent.com/natcap/invest/main/pyproject.toml): pyproject.toml classifies the project as Production/Stable, Intended Audience Science/Research, and Topic Scientific/Engineering GIS. _(cited in 2/5 runs: 1, 3)_
- [Documentation requirements](https://raw.githubusercontent.com/natcap/invest/main/requirements-docs.txt): requirements-docs.txt lists Sphinx and related packages used to build documentation. _(cited in 2/5 runs: 4, 5)_

### Stage 6: Open Verifiability

Average score 61.0 (range 58–66 across 5 runs).

- [Versioned citation and artifact](https://raw.githubusercontent.com/natcap/invest/main/CITATION.cff): CITATION.cff identifies version 3.20.0, DOI 10.60793/natcap-invest-3.20.0, repository-code URL, and repository-artifact URL. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Datastack archive functionality](https://raw.githubusercontent.com/natcap/invest/main/tests/test_datastack.py): Datastack tests build archives from args and model name, extract them, validate them, and execute the referenced model. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [CLI file registry output](https://raw.githubusercontent.com/natcap/invest/main/tests/test_cli.py): A CLI test asserts that running a model produces file_registry.json in the workspace, mapping expected output identifiers to paths. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [File registry tests](https://raw.githubusercontent.com/natcap/invest/main/tests/test_file_registry.py): Tests verify FileRegistry behavior, including unique output IDs and paths, patterned outputs, and directory creation for output paths. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Regression test output checks](https://raw.githubusercontent.com/natcap/invest/main/tests/test_sdr.py): The SDR regression test executes the model and checks expected aggregate values and raster-output properties. _(cited in 2/5 runs: 1, 5)_
- [Open community process](https://raw.githubusercontent.com/natcap/invest/main/CONTRIBUTING.md): CONTRIBUTING.md documents issue reporting, feature requests, peer review for major features, and science review for science-related changes. _(cited in 2/5 runs: 1, 2)_
- [Repository metadata](https://github.com/natcap/invest): The public repository has default branch main, creation/update timestamps, licence metadata, and public issue tracking. _(cited in 2/5 runs: 4, 5)_
- [Dockerfile build path](https://raw.githubusercontent.com/natcap/invest/main/docker/Dockerfile): The Dockerfile copies source, pyproject.toml, setup.py, requirements.txt, license files, and .git into the build context, builds a wheel, and installs it in the container. _(cited in 1/5 runs: 2)_
- [Docker publication note](https://raw.githubusercontent.com/natcap/invest/main/docker/README.md): Docker README states that Docker images and digests are published to GitHub Packages. _(cited in 1/5 runs: 3)_

## Consolidated limitations across runs

Distinct limitations raised by one or more runs (deduplicated):
- The evidence bundle assesses the InVEST repository as a software project, not a specific environmental claim or report output.
- The actual sample-data and test-data repositories are linked but their contents, metadata, licenses, provenance, and uncertainty documentation are not included in the bundle.
- No CI configuration, CI logs, release-build logs, checksums, or signed release verification records are included in the supplied evidence.
- Documentation pages, user-guide content, API docs, and scientific method publications are referenced by links but not included for direct assessment.
- The bundle does not include public pull-request review records, Platform Steering Committee records, NatCap science review reports, correction notices, or forum discussions.
- Dependency files are present, but the evidence does not show a fully pinned lockfile or exact computational environment for each release or test run.
- Some infrastructure described in the code-signing README depends on secrets and organization-controlled systems, so that part is not independently reproducible from public evidence alone.
- The assessment uses only the supplied evidence bundle and does not inspect external documentation, sample data repositories, test data repositories, GitHub issues, pull requests, releases, CI systems, or API docs beyond the URLs and excerpts provided.
- The project is a software suite rather than a single environmental report or claim, so stages involving claim-specific inputs, executions, publications, and verification were scored conservatively.
- Input-data provenance, measurement methods, quality controls, licensing, uncertainty estimates, and links to primary data are mostly absent from the supplied bundle.
- The evidence bundle references public review mechanisms but does not include concrete issue threads, pull request reviews, Platform Steering Committee records, NatCap science reviews, correction notices, or replication attempts.
- The bundle does not provide CI configuration or run logs, exact container image digests, environment lockfiles, dataset checksums, or a complete re-executable workflow for a published environmental claim.
- Some evidence artifacts are truncated, so details in omitted sections could affect scores but were not assumed.
- The assessment used only the supplied evidence bundle; it did not inspect files, issues, releases, documentation pages, sample-data repositories, or Docker package pages beyond the provided excerpts.
- The bundle contains many tests and configuration files but not the full model source code, full user guide, API documentation contents, CI workflow files, CI logs, or release checksums/container digests.
- The project is a general modeling software suite rather than a single environmental claim or report, so stages focused on input data, publications, and claim-level verifiability were scored conservatively.
- Links to sample and test data are present, but the bundle does not provide their dataset metadata, measurement provenance, uncertainty, quality controls, or licenses.
- The contribution guide states review processes, but the bundle does not include actual peer-review records, science-review outcomes, pull-request reviews, or correction histories.
- The evidence bundle is repository-focused and does not include the contents, licences, provenance metadata, quality controls, or uncertainty estimates for the referenced sample/test datasets.
- No complete environmental claim was supplied, so assessment of claim-to-evidence traceability is necessarily conservative.
- The bundle does not include CI configuration, CI results, workflow-run logs, checksums, or exact container image digests.
- The bundle references user guides, API docs, website pages, GitHub releases, Bitbucket data repositories, and a community forum, but their contents were not supplied for direct evaluation.
- Public review mechanisms are documented, but actual issue discussions, pull-request reviews, steering-committee records, science-review records, and correction histories were not included.
- Dependency specifications are visible, but many are minimum-version constraints rather than fully pinned, independently reproducible environment locks.
- The evidence bundle is centered on the software repository, not on a specific environmental claim or report generated with InVEST.
- Linked sample-data, test-data, user-guide, API documentation, release artifacts, container images, and community forum contents were referenced but not included for detailed inspection.
- The actual primary/secondary datasets used in tests or sample workflows were not supplied, so their provenance, measurement methods, uncertainty, quality controls, transformations, and licensing could not be evaluated.
- No CI configuration, CI run logs, build provenance attestations, checksums, or exact release workflow records were provided.
- No pull-request discussions, peer-review reports, Platform Steering Committee records, science-review records, issue-resolution examples, or correction notices were included.
- The assessment cannot verify scientific validity of model equations or environmental outputs; it only evaluates traceability evidence supplied in the bundle.
- Some evidence excerpts are truncated, limiting inspection of full contribution guidance and test implementations.
