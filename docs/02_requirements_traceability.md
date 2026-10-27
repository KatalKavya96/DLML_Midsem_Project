# Phase 1 requirements and evidence mapping

Registered: 2026-10-27, Asia/Kolkata. This replaces the archived placeholder with an evidence map, not faculty approval or a final-submission certificate.

Source: [supplied faculty instructions](../CSAI_Project_Instructions_Phase_1_and_Phase_2.pdf). The broader allocated project title is recorded in [PROJECT.md](../PROJECT.md). The separate project-ideas technical brief is not available here; do not invent its detailed requirements. Generic evaluation categories below are requirements; particular model choices, feature counts and artifact formats beyond that source are project implementation choices.

| Faculty category | Implemented evidence | Verification / remaining gate |
| --- | --- | --- |
| Literature review | [Six-source synthesis](LITERATURE.md), report bibliography | Source-scope disclosure retained; full student reading/understanding not certified |
| Dataset quality and EDA | [Dataset card](DATASET_CARD.md), [training EDA/audit](../verification/full-phase1-20261026/analysis/) | Loader/graph and audit checks; speed-only suitability versus broader title, timezone and raw-data rights remain open |
| Feature engineering | [38-feature explanation](METHODS_AND_VIVA.md), causal feature tests | Creation is implemented; no formal feature selection or group-ablation benefit claimed |
| Theoretical rigor | [Methods/viva guide](METHODS_AND_VIVA.md), IEEE sections | Explain assumptions, bagging/boosting, masking, chronology, metrics and limits; individual defense pending |
| Model application | Two references plus RF/XGB, bounded validation tuning, saved predictions | Common-target MAE/RMSE/MAPE and valid counts; old test interval exposed, exploratory results only |
| GitHub and code quality | Member PRs and prepared Kavya integration, pinned environment, tests and [CI](../.github/workflows/tests.yml) | Actual author/assistance history retained; integration PR/remote CI review remains before locking |
| Presentation | [Editable 11-slide deck](../slides/output/phase1-study.pptx) | Previously rendered/inspected; native presentation rehearsal and individual explanations pending |
| Individual viva | Module reviews and viva questions | Every member must understand and demonstrate the full project; agent activity does not certify that |
| LaTeX/IEEE report | [IEEE source](../report/ieee/main.tex), generated measured tables and figures | Source previously compiled; final PDF export and page-layout review still pending |
| Exactly five same-section members | [Team T072, Section C roster](../PROJECT.md) | Roster recorded from supplied faculty allocation; no invented role completion |

## Phase distinction and unresolved traffic scope

Phase 1 is traditional ML evaluation. Phase 2 evaluates deep-learning architecture, DL literature, regularization, ablation studies, technical validation and shared submission components; a meaningful justified ML-DL hybrid can earn additional marks. None of this establishes that a GAT, calibrated LWR or simulated controller has already been implemented or is a Phase 1 requirement. Resolve the project-specific brief with faculty. Any signal control is simulated only.

The available generic instructions do not specify a universal minimum accuracy, number of models, papers, report pages or slide count. The deliverables above are evidence of our chosen study, not invented rubric thresholds.
