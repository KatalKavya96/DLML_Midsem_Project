# Phase 1 traffic speed forecasting — Team T072

> Integration status: member PRs #2–#6 are merged into `main`. The owner-authorized `kavya` branch adds the selected report and presentation for review. No direct-main commit or push is used. See [current state](PROJECT_STATE.md).

Canonical repository: `KatalKavya96/DLML_Midsem_Project`. The implementation lives directly at this repository root (`src/trafficml`, `scripts`, `tests`, `configs`). There is no nested `AML/` project. Delivery ZIPs, old scaffolding and private build files were moved to the separate sibling `DLML_Project_Archive_2026-10-27` folder. Read [current state](PROJECT_STATE.md), [team roster](PROJECT.md) and [handoff instructions](docs/handoffs/HANDOFF.md).

A local, end-to-end forecasting study using **Persistence, Historical Average, Random Forest and XGBoost** on the existing METR-LA files. No neural networks, graph-neighbour features, UI or traffic-signal controller are included. The broader faculty title/LWR scope remains to be reconciled; do not present forecasting results as traffic-control benefits.

Read [the methods/viva guide](docs/METHODS_AND_VIVA.md), [literature synthesis](docs/LITERATURE.md), and [contribution disclosure](docs/CONTRIBUTIONS.md). The integrated implementation was prepared with substantial AI assistance; names/commits are not evidence of individual implementation.

## Report and presentation

- [Report PDF](report/final/Traffic_Speed_Forecasting_T072.pdf)
- [PowerPoint](slides/final/Traffic_Speed_Forecasting_T072.pptx)
- [Presentation PDF](slides/final/Traffic_Speed_Forecasting_T072.pdf)

These are the owner's supplied files, preserved unchanged. **The presentation's RMSE columns and pilot-candidate labels need correction against the saved evidence.** See [import checks, correct values and provenance](docs/final_deliverables.md). Existing sources and generated experiment evidence are preserved.

## Setup

Use a fresh Python **3.12** environment (tested with 3.12.14). On macOS, XGBoost requires the OpenMP runtime:

```bash
brew install libomp
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install --no-deps --no-build-isolation -e .
python -m pip check
```

Homebrew is a macOS-only prerequisite; Linux uses the platform OpenMP runtime, typically libgomp. Do not copy someone else's virtual environment. Direct/transitive Python package versions are pinned. Native dependencies/platform differences still matter; the runtime manifest records the measured environment.

## Data

Place the existing files here (not distributed in the source package):

```text
data/raw/metr-la.h5
data/raw/sensor_graph/adj_mx.pkl
data/raw/sensor_graph/distances_la_2012.csv
data/raw/sensor_graph/graph_sensor_ids.txt
data/raw/sensor_graph/graph_sensor_locations.csv
```

Source: [DCRNN](https://github.com/liyaguang/DCRNN). The original download helper is retained but was not executed during this work; it separately requires gdown and also downloads PEMS-BAY. Prefer verified local files and compare checksums with the run manifest. Upstream code is MIT; separate raw-data redistribution rights remain unresolved, so no datasets are bundled. No additional flow/occupancy channels are invented.

## Check

```bash
pytest -q -ra
ruff check .
ruff format --check .
python scripts/check_data.py
```

Two real-data tests skip if datasets are missing; a skip is not a passed integration check. Other tests cover causal features, masks, split purging, artifacts, model label rules and saved-model reuse.

## Run the full pipeline

```bash
python scripts/run_all.py --run-dir results/runs/my-phase1-run
```

This trains/tunes the models, evaluates tuning/second-validation/test partitions, generates data/error figures and writes report result tables. Use a **fresh directory per run**. The second validation interval is reported separately; no hybrid stacker is trained. The default training stride is 2 to bound compute. Full evaluation includes all sensors/anchors. A development check can use `--max-sensors 2`; it must never be described as a 207-sensor result.

The two learned methods share 38 causal features. A small, predeclared search uses only val_tune and six evenly spaced pilot sensors. Parameters freeze before full comparisons. Test data were inspected in the earlier prototype; test results are exploratory, not an untouched final holdout. Do not tune against the test tables or promise a particular error/accuracy.

Outputs within the run:

- `manifest.json`: source/data/config hashes, environment, exact command, partitions, feature names and selected parameters.
- `tuning.json`: every budgeted candidate and its pilot validation score.
- `models/`, `preprocessing.joblib`: locally fitted estimators/transforms for later prediction; load only trusted local artifacts.
- `preds/`: immutable targets and aligned predictions for all methods/partitions.
- `tables/`, `leaderboard_*.csv`: MAE/RMSE/MAPE, valid counts and exploratory significance results.
- `training_records.json`, `timing.json`: actual valid training counts, fallback horizons and timings.
- `analysis/`: EDA, horizon/period comparisons, sensor errors and a fixed-index forecast example.

Evaluation rejects stale source/config/data or misaligned artifacts. Changing runtime code requires a new run; do not mix an old result file with a new code snapshot. Full twelve-horizon tensors are retained, with 15/30/60 minutes highlighted. A three-column tensor cannot silently replace them.

## Make a forecast without retraining

Choose a sensor ID from the run manifest, for example the first listed ID:

```bash
python scripts/predict.py --run-dir results/runs/my-phase1-run --sensor 773869 --at latest
```

This prints forecasts 15, 30 and 60 minutes after the dataset's last observation. It is a historical-data demonstration, not live traffic service. Use `--at '2012-06-05 08:00:00'` for another observed origin with adequate history. Earlier origins inside the training interval are in-sample demonstrations, not held-out results. For an alternative sensor, use its exact recorded ID.

## Explain and report

`report/phase1/results.md` and `metrics.tex` are generated from actual completed outputs. `report/ieee/main.tex` is the IEEE-style report source. Copy the generated metrics table and selected run images into its project directory before recompiling, as documented in `report/ieee/README.md`. Presentation material is under `slides/`.

Key limitations: prior test exposure; provisional clock timezone/DST and peak windows; missing-target selection bias in multi-output RF; strided training; a small pilot search; a single region/period; low-speed MAPE instability. The graph is verified but not a prediction input. Multi-seed stability, graph learning, calibrated LWR physics and signal simulation remain future work.

## Integrity and ownership

Original teammate code/plan and correction records are retained as history. Report actual contributions and assistance honestly. Team members need to understand the full pipeline for viva; a completed code package cannot certify that understanding. The owner-authorized integration is prepared on branch `kavya`; branch publication and PR review are separate from merging or declaring final acceptance.
