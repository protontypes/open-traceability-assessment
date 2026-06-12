# Open Traceability Assessment Report

- Project/report URL: https://github.com/wri/gfw
- Assessment definition URL: https://raw.githubusercontent.com/protontypes/open-traceability/refs/heads/main/docs/definition.md
- Number of runs: 5

## Final single-paragraph summary

Across 5 independent assessment runs, the project appears strongest on Open-Source Models, Methods, and Software with an average score of 75.2, and weakest on Open Linkage with an average score of 38.8. The average total score across runs is 52.0. The scores should be interpreted as evidence-bundle-based traceability estimates rather than scientific validation: high scores indicate externally inspectable artifacts and linkages, while lower scores indicate missing, implicit, or insufficiently versioned evidence in the collected material.

## Score table across runs

| Stage | Stage name | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Average | Std dev |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Open Input Data and Measurement Evidence | 45 | 44 | 38 | 38 | 38 | 40.6 | 3.2 |
| 2 | Open-Source Models, Methods, and Software | 76 | 78 | 76 | 74 | 72 | 75.2 | 2.0 |
| 3 | Open Execution and Reproducibility | 48 | 54 | 50 | 54 | 46 | 50.4 | 3.2 |
| 4 | Open Community and Review | 43 | 50 | 46 | 49 | 44 | 46.4 | 2.7 |
| 5 | Open Publications and Communication | 62 | 66 | 57 | 62 | 57 | 60.8 | 3.4 |
| 6 | Open Linkage | 36 | 40 | 40 | 42 | 36 | 38.8 | 2.4 |

## Total score

| Run | Total score |
| --- | ---: |
| 1 | 52 |
| 2 | 55 |
| 3 | 51 |
| 4 | 53 |
| 5 | 49 |

Average total score: **52.0**; population standard deviation: **2.0**.

## Consolidated references by stage

References cited across all runs, deduplicated by URL. The runs that cited each reference are noted in parentheses; references cited by more runs appear first.

### Stage 1: Open Input Data and Measurement Evidence

Average score 40.6 (range 38–45 across 5 runs).

- [README identifies dataset source API](https://raw.githubusercontent.com/wri/gfw/develop/README.md): “GFW Map layers and relevant datasets are stored in the RW-API” and an endpoint is provided: https://api.resourcewatch.org/v1/dataset?app=gfw&includes=layer,vocabulary,metadata&page[size]=200. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [GFW API dataset and metadata schema](https://raw.githubusercontent.com/wri/gfw/develop/docs/API_Documentation.md): Documents dataset syntax, vocabulary tags, metadata keys, layer syntax, ISO country fields, and legend/application configuration for GFW layers. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Climate widget input column and table reference](https://raw.githubusercontent.com/wri/gfw/develop/docs/ClimateWidgets.md): Above-ground biomass is said to come from the `whrc_aboveground_biomass_stock_2000__Mg` column within summary Geotrellis tables, with an example table UUID `998dd97a-389f-4a02-988f-17b184f507ac`. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Repository metadata](https://github.com/wri/gfw): Repository topics include deforestation, forest-monitoring, and satellite-imagery; description says it is an online, near-real-time forest monitoring tool. _(cited in 1/5 runs: 3)_
- [Widget calculation docs: raw weekly alert counts](https://raw.githubusercontent.com/wri/gfw/develop/docs/Widget_Calculations_Docs.md): Describes calculations using “raw, weekly aggregated data” and alert counts `alert__count` for GLAD and Fires widgets. _(cited in 1/5 runs: 5)_

### Stage 2: Open-Source Models, Methods, and Software

Average score 75.2 (range 72–78 across 5 runs).

- [Repository metadata and license](https://github.com/wri/gfw): Repository description: “Global Forest Watch: An online, global, near-real time forest monitoring tool”; license listed as MIT; default branch is `develop`. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [MIT license text](https://raw.githubusercontent.com/wri/gfw/develop/LICENSE): The license permits use, copy, modification, merge, publication, distribution, sublicensing, and sale of the software under MIT terms. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [README setup and stack](https://raw.githubusercontent.com/wri/gfw/develop/README.md): The app is built with Next.js, React, and Redux; setup commands include `git clone`, `yarn`, copying `.env.sample` to `.env.local`, and `yarn dev`. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Widget calculation methods](https://raw.githubusercontent.com/wri/gfw/develop/docs/Widget_Calculations_Docs.md): Documents statistical calculations for widgets, including weekly aggregation, zero filling, means, standard deviations, and smoothing. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [GFW API documentation](https://raw.githubusercontent.com/wri/gfw/develop/docs/API_Documentation.md): Documents dataset and layer syntax used by the front end to define appearance and behaviour in the application. _(cited in 1/5 runs: 3)_
- [Climate widget calculations](https://raw.githubusercontent.com/wri/gfw/develop/docs/ClimateWidgets.md): Documents formulas such as belowground biomass `M_bgb = 0.489 x M_agb^0.89` and carbon stock `M_Carbon = 0.5 x M_biomass`. _(cited in 1/5 runs: 5)_

### Stage 3: Open Execution and Reproducibility

Average score 50.4 (range 46–54 across 5 runs).

- [Local development instructions](https://raw.githubusercontent.com/wri/gfw/develop/README.md): Installation instructions specify cloning the repo, running `yarn`, copying `.env.sample` to `.env.local`, and starting the app with `yarn dev`. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [CI workflow](https://raw.githubusercontent.com/wri/gfw/develop/.github/workflows/ci.yml): CI runs on pull requests and pushes to `develop` and `master`, sets up Node `18.15.0`, installs modules with `yarn`, runs ESLint, and runs unit tests via `yarn test:ci`. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [CodeQL workflow](https://raw.githubusercontent.com/wri/gfw/develop/.github/workflows/codeql-analysis.yml): CodeQL analysis is configured for JavaScript on pushes, pull requests, and a weekly schedule. _(cited in 3/5 runs: 1, 3, 5)_

### Stage 4: Open Community and Review

Average score 46.4 (range 43–50 across 5 runs).

- [Repository issue metadata](https://github.com/wri/gfw): Repository metadata reports `open_issues_count: 16`. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Pull-request and review-app workflow](https://raw.githubusercontent.com/wri/gfw/develop/README.md): Development uses Gitflow; pull requests are merged into `develop`; Heroku Review Apps are deployed automatically when a pull request is created and linked to the pull request. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [CI checks for review](https://raw.githubusercontent.com/wri/gfw/develop/.github/workflows/ci.yml): Pull requests to `develop` and `master` trigger linting and unit tests. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [CodeQL review automation](https://raw.githubusercontent.com/wri/gfw/develop/.github/workflows/codeql-analysis.yml): CodeQL runs on pull requests and scheduled weekly for JavaScript. _(cited in 4/5 runs: 1, 2, 3, 4)_

### Stage 5: Open Publications and Communication

Average score 60.8 (range 57–66 across 5 runs).

- [Public GFW description and homepage](https://raw.githubusercontent.com/wri/gfw/develop/README.md): “Global Forest Watch ... is a dynamic online forest monitoring and alert system” and the homepage is given as http://www.globalforestwatch.org/. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Layer and dataset documentation](https://raw.githubusercontent.com/wri/gfw/develop/docs/API_Documentation.md): Documents how GFW layers and datasets should be configured, including metadata, legend behavior, interactions, and external more-info links. _(cited in 4/5 runs: 1, 2, 3, 5)_
- [Widget calculation documentation](https://raw.githubusercontent.com/wri/gfw/develop/docs/Widget_Calculations_Docs.md): Provides explanatory documentation for dashboard widget calculations, including statistical bands for Fires and GLAD widgets. _(cited in 4/5 runs: 1, 3, 4, 5)_
- [Climate widget calculations](https://raw.githubusercontent.com/wri/gfw/develop/docs/ClimateWidgets.md): The document explains formulas for below-ground biomass, total biomass, carbon stock, below-ground carbon, and total carbon, including mathematical notation. _(cited in 4/5 runs: 2, 3, 4, 5)_
- [Repository homepage metadata](https://github.com/wri/gfw): Repository homepage is listed as `https://www.globalforestwatch.org`. _(cited in 2/5 runs: 3, 5)_

### Stage 6: Open Linkage

Average score 38.8 (range 36–42 across 5 runs).

- [App-to-data/API linkage](https://raw.githubusercontent.com/wri/gfw/develop/README.md): The README states that GFW map layers and relevant datasets are stored in RW-API and that `globalforestwatch.org/map` uses `layer-manager` to render them. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Metadata keys connect datasets to UI behavior](https://raw.githubusercontent.com/wri/gfw/develop/docs/API_Documentation.md): Dataset metadata includes `info.metadata`, described as “the metadata key for the dataset,” and application configuration controls layer behavior. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Calculation-to-input linkage example](https://raw.githubusercontent.com/wri/gfw/develop/docs/ClimateWidgets.md): The carbon stock widget calculation references `whrc_aboveground_biomass_stock_2000__Mg` in summary Geotrellis tables, including example table UUID `998dd97a-389f-4a02-988f-17b184f507ac`. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [CI workflow: tests tied to branches, not claims](https://raw.githubusercontent.com/wri/gfw/develop/.github/workflows/ci.yml): CI runs lint and unit tests on pushes and pull requests for `master` and `develop`. _(cited in 1/5 runs: 5)_

## Consolidated limitations across runs

Distinct limitations raised by one or more runs (deduplicated):
- The assessment uses only the supplied evidence bundle and does not inspect the live Resource Watch API, live Global Forest Watch website, GitHub issues, pull requests, releases, or repository files not included in the bundle.
- The project URL is for the GFW web app, not necessarily the full Global Forest Watch scientific data-processing system; upstream APIs, satellite data pipelines, alert-generation models, and backend services may have separate repositories or documentation not included here.
- No actual API responses, dataset records, primary measurement documentation, dataset licenses, uncertainty estimates, or quality-control reports were supplied.
- No specific environmental claim or dashboard output was supplied, so linkage was assessed from general repository documentation rather than from a claim-specific evidence chain.
- The evidence bundle includes workflow configuration but not CI run logs, exact production environment configuration, API snapshots, or reproducible computational runs for environmental results.
- The evidence bundle reports open issue counts and workflows but does not include actual review discussions, governance records, peer-review materials, or correction histories.
- The assessment uses only the supplied evidence bundle and did not inspect the live Global Forest Watch site, API responses, GitHub issues, pull requests, releases, or files not included in the bundle.
- The evidence bundle does not include actual dataset metadata records, primary data sources, dataset licenses, uncertainty estimates, quality-control records, or versioned data snapshots.
- The evidence bundle does not include package manifests, lockfiles, `.env.sample`, build artifacts, containers, or full production infrastructure configuration.
- The repository appears to be the GFW web app rather than the complete backend/data-processing system, so the assessment may understate traceability if backend repositories or data pipelines provide additional evidence.
- No specific environmental claim was supplied, so scoring assesses the repository’s general traceability infrastructure rather than a claim-specific evidence chain.
- The evidence bundle provides workflow definitions and metadata but not actual CI run results, issue discussions, peer-review records, correction notices, or release artifacts.
- The evidence bundle appears focused on the `wri/gfw` front-end repository and does not include the full backend/API code, data pipelines, or hosted API metadata responses.
- No primary satellite or field measurement datasets were provided, so provenance, quality control, uncertainty, and reuse conditions for input data could not be fully assessed.
- No package manifest, lockfile, container definition, `.env.sample`, or full deployment configuration was included in the evidence bundle, limiting reproducibility assessment.
- No specific environmental claim, dashboard value, report, or publication was identified for end-to-end tracing.
- No issue, pull request, peer review, correction notice, governance, or community discussion records were included beyond repository metadata and workflow descriptions.
- The live Global Forest Watch website and Resource Watch API may contain additional documentation or metadata, but only the supplied artifacts were used for scoring.
- The evidence bundle focuses on the `wri/gfw` web app repository and does not include the live Global Forest Watch dashboard pages, formal reports, or methodology publications.
- External Resource Watch API dataset records are referenced but not included, so dataset provenance, licensing, uncertainty, quality controls, and versioning cannot be fully assessed.
- The bundle does not include package manifests, lockfiles, `.env.sample`, backend services, geotrellis processing code, or infrastructure configuration needed to assess complete reproducibility.
- No specific environmental claim was supplied; the assessment therefore evaluates the repository’s traceability infrastructure rather than tracing one claim end to end.
- Issue contents, pull request discussions, governance documents, correction notices, peer-review records, and community feedback processes were not included.
- GitHub releases are mentioned in the README, but actual release artifacts and their relationship to public outputs were not provided.
- The evidence bundle contains selected repository files but not the full repository tree, package manifests, lockfiles, tests, source-code implementations, or environment templates.
- The Resource Watch API endpoint is referenced, but the bundle does not include API responses, dataset metadata records, data licenses, data versions, or primary measurement provenance.
- No live Global Forest Watch dashboard pages, reports, publications, or indicator pages were included, so publication quality and source citation in final outputs could only be inferred from repository documentation.
- No actual GitHub issues, pull requests, review comments, release pages, correction notices, or community discussions were supplied, only metadata and workflow descriptions.
- No archived workflow runs, production run logs, model configuration files, data-processing pipelines, containers, or reproducibility packages were provided.
- Scores assess the supplied evidence only and may understate traceability if relevant artifacts exist outside the bundle.
