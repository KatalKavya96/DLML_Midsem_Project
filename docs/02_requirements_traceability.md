# Phase 1 requirements and evidence mapping

Registered: 2026-10-27, Asia/Kolkata; updated 2026-10-27 with the Project 4 brief. This is an evidence map, not faculty approval or a final-submission certificate.

Sources:

- [Faculty instructions](../CSAI_Project_Instructions_Phase_1_and_Phase_2.pdf): team rules, the Phase 1 rubric categories and individual viva.
- Project 4 brief, "Traffic Flow Prediction and Signal Control via Graph Attention Networks and Flow Models", supplied by the team on 2026-10-27. It asks for an AML baseline (lagged speed/flow/occupancy, time-of-day and road-segment features; XGBoost per segment or multi-output Random Forest), identification of the independent-model gap, a GAT/diffusion model over METR-LA's fixed adjacency (Phase 2), chronological splits, MAE/RMSE/MAPE by horizon, equal history windows, peak versus off-peak reporting, training-only scaling, cyclic time features, outage masking, congestion maps, and an optional simulated-only signal experiment. Pre-reads: Veličković et al. (2018) and CityFlow (2019).

## Phase 1 rubric

| Faculty category | Implemented evidence | Verification / remaining gate |
| --- | --- | --- |
| Literature review | [Source register](LITERATURE.md) including the brief's pre-reads; report Section III | Full student reading/understanding not certified |
| Dataset quality and EDA | [Dataset card](DATASET_CARD.md), [training EDA/audit](../verification/full-phase1-20261026/analysis/), congestion map in [report figures](../report/figures/) | Timezone and raw-data rights remain open |
| Feature engineering | 38 causal features ([methods](METHODS_AND_VIVA.md)), causal feature tests, feature-importance figure | No formal feature-selection or ablation benefit claimed |
| Theoretical rigor | [Methods/viva guide](METHODS_AND_VIVA.md), report Sections II and VI | Individual defense pending |
| Model application | Persistence, historical average, multi-output RF, direct XGBoost; validation-only tuning | Test interval previously exposed; test results exploratory |
| GitHub and code quality | Member PRs #2-#6, pinned environment, tests and [CI](../.github/workflows/tests.yml) | Remote CI result to be checked on the PR |
| Presentation | [10-slide deck](../slides/phase1_presentation.pptx), one slide per member's module, with a [speaker guide](../slides/SLIDE_CONTENT.md) | Rehearsal and individual explanations pending |
| Individual viva | Module reviews and viva questions | Every member must understand and demonstrate the full project |
| LaTeX/IEEE report | [Compiled report](../report/phase1_report.pdf) (8 pages) from [IEEE source](../report/main.tex), with [figures and provenance](../report/README.md) | Team review of the text |
| Exactly five same-section members | [Team T072, Section C roster](../PROJECT.md) | Roster from the faculty allocation |

## Project 4 brief, Phase 1 items

| Brief item | Status | Evidence |
| --- | --- | --- |
| Lagged speed and time-of-day features | Done | 12 lags, rolling statistics, sin/cos time of day and week |
| Flow and occupancy features | Not possible with METR-LA | The dataset has speed only; nothing is fabricated. PeMS is the brief's suggested extension |
| Road-segment features | Implicit | One model per sensor learns that sensor's behaviour |
| XGBoost per segment or multi-output RF | Done (both) | `src/trafficml/models/trees.py` |
| Identify the independent-model gap | Done | Report Section VIII; spatially clustered errors in `report/figures/error_maps.png` |
| Chronological splits | Done | Purged 70/10/20 split, `src/trafficml/data/splits.py` |
| Fit scaling only on training timestamps | Done | No scaler is needed for trees; medians and historical averages are fitted on training only |
| Cyclic time features | Done | `src/trafficml/features/temporal.py` |
| Mask outages instead of zero traffic | Done | `src/trafficml/data/masking.py`; identical masks for every model |
| MAE, RMSE, MAPE by horizon | Done | `verification/full-phase1-20261026/analysis/all_metrics.csv` (all 12 horizons) |
| Equal history windows | Done | 12 steps (60 minutes) for every model |
| Peak versus off-peak | Done | Peak/off-peak/weekday/weekend slices; peak hours use recorded clock time |
| Adjacency from the supplied graph | Done | Rebuilt Gaussian-kernel adjacency matches DCRNN `adj_mx.pkl` |
| Congestion maps, horizon-wise metrics | Done | `report/figures/congestion_map.png`, `error_maps.png`, `mae_horizons_test.png` |

## Phase 2 (deferred)

GAT or diffusion graph model in PyTorch/PyTorch Geometric, deep-learning literature, ablations, an optional justified ML-DL hybrid and an optional simulated-only signal policy (SUMO or CityFlow). None of these is implemented in Phase 1. The brief does not require a calibrated LWR model; LWR appears only as theoretical motivation.
