# Open Traceability Assessment Report

- Project/report URL: https://github.com/wri/gfw
- Assessment definition URL: https://raw.githubusercontent.com/protontypes/open-traceability/refs/heads/main/docs/definition.md
- Model: gpt-5.5
- Number of runs: 5

## Final single-paragraph summary

Across 5 independent assessment runs, the project appears strongest on Open-Source Models, Methods, and Software with an average score of 75.6, and weakest on Open Linkage with an average score of 39.8. The average total score across runs is 53.4. The scores should be interpreted as evidence-bundle-based traceability estimates rather than scientific validation: high scores indicate externally inspectable artifacts and linkages, while lower scores indicate missing, implicit, or insufficiently versioned evidence in the collected material.

## Score table across runs

| Stage | Stage name | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Average | Std dev |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Open Input Data and Measurement Evidence | 45 | 43 | 45 | 42 | 42 | 43.4 | 1.4 |
| 2 | Open-Source Models, Methods, and Software | 72 | 76 | 78 | 76 | 76 | 75.6 | 2.0 |
| 3 | Open Execution and Reproducibility | 50 | 54 | 55 | 54 | 51 | 52.8 | 1.9 |
| 4 | Open Community and Review | 50 | 50 | 48 | 53 | 48 | 49.8 | 1.8 |
| 5 | Open Publications and Communication | 58 | 62 | 54 | 59 | 61 | 58.8 | 2.8 |
| 6 | Open Linkage | 40 | 38 | 42 | 39 | 40 | 39.8 | 1.3 |

## Total score

| Run | Total score |
| --- | ---: |
| 1 | 52 |
| 2 | 54 |
| 3 | 54 |
| 4 | 54 |
| 5 | 53 |

Average total score: **53.4**; population standard deviation: **0.8**.

## Consolidated references by stage

References cited across all runs, deduplicated by URL. The runs that cited each reference are noted in parentheses; references cited by more runs appear first. References marked ⚠️ point to a URL that was not part of the collected evidence bundle and could not be verified (the model may have introduced them).

### Stage 1: Open Input Data and Measurement Evidence

Average score 43.4 (range 42–45 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 5, high 0).

- [README data/API reference](https://raw.githubusercontent.com/wri/gfw/develop/README.md): Map layers and relevant datasets are stored in the RW-API, and the README gives the endpoint `https://api.resourcewatch.org/v1/dataset?app=gfw&includes=layer,vocabulary,metadata&page[size]=200`. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [GFW API documentation](https://raw.githubusercontent.com/wri/gfw/develop/docs/API_Documentation.md): Documents GFW dataset syntax, vocabulary tags, metadata fields, layer configuration, ISO applicability, legend configuration, and external `moreInfo` links. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Climate widget calculations](https://raw.githubusercontent.com/wri/gfw/develop/docs/ClimateWidgets.md): Identifies above-ground biomass as coming from the `whrc_aboveground_biomass_stock_2000__Mg` column within summary Geotrellis tables, including table `998dd97a-389f-4a02-988f-17b184f507ac`. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Repository metadata](https://github.com/wri/gfw): Repository description: “Global Forest Watch: An online, global, near-real time forest monitoring tool”; topics include deforestation, forest-monitoring, and satellite-imagery. _(cited in 1/5 runs: 2)_

### Stage 2: Open-Source Models, Methods, and Software

Average score 75.6 (range 72–78 across 5 runs). Reported uncertainty: mostly low (low 3, medium 2, high 0).

- [Repository metadata](https://github.com/wri/gfw): Repository description: “Global Forest Watch: An online, global, near-real time forest monitoring tool”; licence listed as MIT; default branch `develop`; topics include deforestation, forest-monitoring, satellite-imagery, Next.js, React, Redux. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [MIT licence](https://raw.githubusercontent.com/wri/gfw/develop/LICENSE): The licence grants permission to use, copy, modify, merge, publish, distribute, sublicense, and sell copies of the software, subject to MIT terms. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [README installation and architecture](https://raw.githubusercontent.com/wri/gfw/develop/README.md): The app is built with Next.js, React, and Redux; installation steps include cloning the repo, running `yarn`, copying `.env.sample` to `.env.local`, and starting with `yarn dev`. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Widget calculation documentation](https://raw.githubusercontent.com/wri/gfw/develop/docs/Widget_Calculations_Docs.md): Documents mathematical/statistical calculations for dashboard widgets, including mean, standard deviation, zero-filling, ISO week grouping, and temporal smoothing. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [CI workflow](https://raw.githubusercontent.com/wri/gfw/develop/.github/workflows/ci.yml): GitHub Actions installs modules with `yarn`, runs ESLint, and runs unit tests on pull requests and pushes to `develop` and `master` using Node 18.15.0. _(cited in 1/5 runs: 2)_

### Stage 3: Open Execution and Reproducibility

Average score 52.8 (range 50–55 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 5, high 0).

- [README local execution](https://raw.githubusercontent.com/wri/gfw/develop/README.md): Getting-started instructions: clone the repository, install dependencies with `yarn`, copy `.env.sample` to `.env.local`, and run `yarn dev` to access the app on port 3000. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [CI workflow](https://raw.githubusercontent.com/wri/gfw/develop/.github/workflows/ci.yml): CI runs on pull requests to develop/master and pushes to master/develop; jobs use Ubuntu, Node 18.15.0, `yarn`, `yarn lint`, and `yarn test:ci`. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [CodeQL workflow](https://raw.githubusercontent.com/wri/gfw/develop/.github/workflows/codeql-analysis.yml): CodeQL analysis runs for JavaScript on pushes to `develop` and `master`, pull requests to `develop`, and on a weekly schedule. _(cited in 3/5 runs: 2, 4, 5)_
- [Widget calculation documentation](https://raw.githubusercontent.com/wri/gfw/develop/docs/Widget_Calculations_Docs.md): Explains processing steps for alert-count widgets, including parsing dates, zero-filling data, grouping by isoweek/year, reducing to means and standard deviations, and smoothing. _(cited in 2/5 runs: 2, 3)_

### Stage 4: Open Community and Review

Average score 49.8 (range 48–53 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 5, high 0).

- [Repository metadata issues](https://github.com/wri/gfw): Repository metadata reports `open_issues_count: 16`. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [README Gitflow and review apps](https://raw.githubusercontent.com/wri/gfw/develop/README.md): The project follows a Gitflow workflow, merges pull requests into `develop`, and creates Heroku review apps for pull requests with links added to the respective pull request. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [CI workflow for pull requests](https://raw.githubusercontent.com/wri/gfw/develop/.github/workflows/ci.yml): Lint and unit-test jobs run on pull requests targeting `develop` and `master`. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [CodeQL workflow](https://raw.githubusercontent.com/wri/gfw/develop/.github/workflows/codeql-analysis.yml): CodeQL analysis runs on pushes, pull requests, and a weekly schedule for JavaScript. _(cited in 4/5 runs: 1, 2, 3, 4)_

### Stage 5: Open Publications and Communication

Average score 58.8 (range 54–62 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 5, high 0).

- [README project description](https://raw.githubusercontent.com/wri/gfw/develop/README.md): Defines GFW as “a dynamic online forest monitoring and alert system that empowers people everywhere to better manage forests” and links to the public site `globalforestwatch.org`. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [API documentation](https://raw.githubusercontent.com/wri/gfw/develop/docs/API_Documentation.md): Documents how GFW layers and datasets should be configured for display, legend behavior, searchability, metadata, and external links. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Climate widget documentation](https://raw.githubusercontent.com/wri/gfw/develop/docs/ClimateWidgets.md): Explains formulas for below-ground biomass, total biomass, and carbon stocks used in climate widgets. _(cited in 4/5 runs: 1, 2, 3, 5)_
- [Repository homepage metadata](https://github.com/wri/gfw): Repository metadata lists homepage `https://www.globalforestwatch.org` and describes GFW as an online, global, near-real-time forest monitoring tool. _(cited in 3/5 runs: 2, 3, 4)_
- [Widget calculation documentation](https://raw.githubusercontent.com/wri/gfw/develop/docs/Widget_Calculations_Docs.md): Documents statistical bands for fires and GLAD widgets, including mean, standard deviation, and smoothing approaches. _(cited in 3/5 runs: 2, 4, 5)_

### Stage 6: Open Linkage

Average score 39.8 (range 38–42 across 5 runs). Reported uncertainty: mostly medium (low 0, medium 4, high 1).

- [README API and layer linkage](https://raw.githubusercontent.com/wri/gfw/develop/README.md): States that GFW map layers and datasets are stored in RW-API and that `globalforestwatch.org/map` uses `layer-manager` to render them; gives a GFW dataset endpoint. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [API metadata linkage](https://raw.githubusercontent.com/wri/gfw/develop/docs/API_Documentation.md): The `info.metadata` field is described as “the metadata key for the dataset (populates metadata modal)”; `applicationConfig.moreInfo` defines external links in the legend. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Climate calculation linkage](https://raw.githubusercontent.com/wri/gfw/develop/docs/ClimateWidgets.md): The `carbonStock` widget uses functions such as `agBiomass2bgBiomass`, with input from the `whrc_aboveground_biomass_stock_2000__Mg` column in specified summary Geotrellis tables. _(cited in 5/5 runs: 1, 2, 3, 4, 5)_
- [Widget calculation methods](https://raw.githubusercontent.com/wri/gfw/develop/docs/Widget_Calculations_Docs.md): Documents how raw weekly alert data are transformed into means, standard deviations, and smoothed statistical bands. _(cited in 1/5 runs: 2)_

## Consolidated limitations across runs

Distinct limitations raised by one or more runs (deduplicated):
- The evidence bundle contains repository metadata and selected files only; it does not include the actual Resource Watch API dataset records returned by the documented endpoint.
- No specific environmental claim, dashboard indicator page, report, or output snapshot was supplied, so claim-level traceability could not be assessed directly.
- The repository appears to be primarily the GFW web app; backend services, data-processing pipelines, remote-sensing workflows, and dataset production systems may exist elsewhere but are not evidenced here.
- Dependency manifests, `.env.sample`, test results, release pages, pull request discussions, issue contents, and GitHub Actions run logs were not included in the evidence bundle.
- No primary measurement evidence, uncertainty estimates, quality-control documentation, dataset version history, or data-use licences were supplied for the environmental datasets.
- No peer-review records, correction notices, public methodological discussions, governance records, or replication attempts were included.
- The assessment uses only the supplied evidence bundle and does not inspect the live Global Forest Watch website, Resource Watch API responses, GitHub issues, pull requests, releases, or source files not included in the bundle.
- The bundle primarily documents the web app, not the upstream data pipelines, primary satellite/field measurements, backend APIs, Geotrellis tables, or data-processing infrastructure that produce many environmental outputs.
- No specific environmental claim or dashboard value was supplied, so claim-level traceability could not be tested directly.
- Dataset licences, primary data provenance, measurement methods, uncertainty/error estimates, quality-control procedures, and dataset version histories were not included for the underlying forest-monitoring inputs.
- The evidence includes review infrastructure but not actual review discussions, peer-review reports, correction notices, governance records, or affected-community feedback.
- The evidence does not include immutable workflow run IDs, output artifacts, exact API snapshots, environment variable examples, dependency lockfiles, or deployment logs needed for stronger reproducibility and linkage scoring.
- The evidence bundle covers the `wri/gfw` web-app repository, not necessarily the full Global Forest Watch data-production, analysis, and publication ecosystem.
- External Resource Watch API records are referenced but their actual metadata contents, licenses, versions, provenance, uncertainty, and primary measurement sources are not included in the bundle.
- No specific environmental claim or dashboard output was supplied for tracing from claim back to exact data, code, execution run, review, and publication artifacts.
- The bundle does not include dependency manifests, lockfiles, `.env.sample`, package scripts, test results, build artifacts, or archived workflow-run outputs.
- Public issue and pull-request mechanisms are evidenced, but the contents of reviews, corrections, methodological discussions, or community feedback are not included.
- The public Global Forest Watch website is identified, but the evidence bundle does not include dashboard pages, update-cycle documentation, indicator version histories, publication licenses, or cited reports.
- The evidence bundle does not include actual RW-API dataset records, source datasets, metadata pages, or archived API responses, so input-data provenance and licensing cannot be fully assessed.
- The bundle focuses on the GFW web app repository and does not include backend/API source code, data-processing pipelines, Geotrellis table generation workflows, or infrastructure definitions.
- No specific environmental claim or dashboard output was supplied, so scoring had to assess general project traceability rather than a claim-specific evidence chain.
- No public issue, pull request, review, correction, or governance discussion contents were provided, only evidence that the mechanisms exist.
- No dependency manifest, lockfile, `.env.sample` content, container image, or public CI run artifacts were included in the evidence bundle.
- No publication-level artifacts such as reports, indicator metadata pages, content licenses, update histories, or citations to all supporting datasets were provided.
- No end-to-end provenance manifest links exact dataset versions, code commits, parameters, workflow runs, review records, and public outputs.
- The assessment uses only the supplied evidence bundle and does not inspect live API responses, GitHub issues, pull requests, releases, package manifests, or the production website beyond the provided excerpts.
- The repository appears to be primarily the GFW web app; many datasets, APIs, backend processing systems, satellite products, and model pipelines underlying GFW claims are external to the supplied evidence.
- No primary data files, data licences, measurement protocols, quantified uncertainty records, or quality-control documentation were included in the bundle.
- No exact dashboard claim, timestamped output, data snapshot, code commit, workflow run, and review/publication record were supplied as a complete traceable chain.
- Evidence of community and review processes is limited to repository metadata, CI, pull-request/review-app descriptions, and release practices; substantive review discussions or correction records were not provided.
- Publication and communication evidence is limited to the README and documentation files; no formal reports, papers, dashboard version histories, update-cycle documentation, or Creative Commons publication licences were included.
