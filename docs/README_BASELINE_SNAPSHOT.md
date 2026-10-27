> Historical baseline-only README, preserved before the Phase 1 extension.

# T072 — Traffic forecasting prototype (Phase 1)

A corrected sandbox copy of the teammate's METR-LA prototype. The implemented models are **M0 persistence** and **M1 historical average**. This is for review and testing, not a completed Phase 1 submission or an approved dataset/methodology decision.

No UI is required to run this prototype. Use the commands below. EDA, feature engineering, Ridge/Random Forest/XGBoost, plots, report, slides and Phase 2 remain future work. A basic CI workflow is included; its remote run status must be checked separately. Signal control is simulated-only future scope.

Read [CORRECTIONS.md](CORRECTIONS.md), [the current proposal](PHASE1_PLAN.md), and [agent instructions](AGENTS.md) before extending it. The faculty allocation title is “Multi-Agent Traffic Flow Control via Graph Attention Networks and LWR Models”; earlier notes use a different forecasting title. This scope discrepancy remains open.

## Setup

Tested on macOS with Python **3.12.14**. Create a fresh virtual environment on your own machine; copied `.venv` directories are not portable. `requirements.txt` pins all packages in the tested environment. It does not guarantee identical binary wheels across operating systems.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install --no-deps --no-build-isolation -e .
python -m pip check
```

Only packages used by the baseline pipeline and its tests are required. `requirements-future.txt` preserves the original dependency proposal; it is not needed for these commands.

## Dataset files

Datasets and generated predictions are excluded from Git. Copy the existing teammate `data/raw/` files locally, or obtain the benchmark from its supplied source after checking permissions/licensing:

- [DCRNN repository](https://github.com/liyaguang/DCRNN)
- [DCRNN dataset folder](https://drive.google.com/drive/folders/10FOTa6HXPqX8Pf5WRoRwcFnW9BrNZEIX)

Expected layout:

```text
data/raw/
  metr-la.h5
  sensor_graph/
    adj_mx.pkl
    distances_la_2012.csv
    graph_sensor_ids.txt
    graph_sensor_locations.csv
```

For convenience, the original `scripts/download_data.sh` is retained. It requires separately installing `gdown==6.4.2`, uses the upstream mutable `master` branch, and downloads PEMS-BAY as well. It was not executed during correction. Prefer verified local files; each new run records their SHA-256 checksums. Dataset distribution/licensing and formal selection remain unresolved.

## Check and test

```bash
pytest -q
ruff check .
ruff format --check .
python scripts/check_data.py
```

Unit tests run without data; the real-data tests explicitly skip if files are absent. Inspect the skipped count before claiming a complete integration check. `check_data.py` requires the graph files and also checks the speed series when present.

## Run the existing baselines

Start with validation. Choose a **new directory for each run**:

```bash
python scripts/run_baselines.py --run-dir results/runs/my-review
python scripts/evaluate.py --run-dir results/runs/my-review --dm M1_ha M0_persistence
```

Both commands default to `val_tune`. Outputs are the manifest, validated target/prediction bundles, metric tables including valid sample counts, and a leaderboard. Relative `--run-dir` paths are relative to your shell's current directory; run these commands from the project root.

To reproduce all previously implemented baseline splits explicitly:

```bash
python scripts/run_baselines.py --run-dir results/runs/all-splits-review --splits val_tune val_stack test
python scripts/evaluate.py --run-dir results/runs/all-splits-review --split test --dm M1_ha M0_persistence
```

The old test results were already inspected. These are exploratory correction checks, not an untouched final holdout. Do not tune models on test results. A formal future evaluation protocol requires owner review.

The runner refuses an existing run directory. Evaluation refuses mismatched source/configuration/data hashes, stale targets, misaligned sensors/anchors, legacy bundles, or non-finite scored predictions. Keep the source revision and run manifest together; changed source should be verified in a new run.

## Protocol and limitations

- Nominal 70/10/20 anchor partitions are retained as a prototype setting. Earlier partitions drop their final `horizon - 1` anchors, including the boundary between the two validation halves. This differs from the original unpurged DCRNN split.
- Inputs contain past observations only; historical averages fit through the last retained training target. Past history can cross partition boundaries.
- Zero/NaN readings are excluded; malformed infinite or negative raw speeds are rejected. Zero-as-missing is the prototype's benchmark policy, not a universal traffic-sensor rule. Targets are never imputed. Persistence uses historical-average fallback when its entire lookback is missing.
- MAE/RMSE aggregate valid target points per horizon. MAPE is a percentage over the same nonzero valid targets, without a low-speed floor; low-speed sensitivity remains a limitation.
- Peak slices use weekday target-clock hours 07:00–10:00 and 16:00–19:00. Timestamp timezone/DST remains unresolved; these slices are provisional.
- Holm correction currently covers one requested model pair across its horizons, not a future family of multiple ablations. Confidence intervals and bootstrap are not implemented.

## Team and repository

Team T072, Section C: Rudraksh Sharma, Anshuman Mehta, Vridhi Chaudhary, Bineet Keshari, and Kavya Katal. The original submission proposed task ownership; approval and individual contribution evidence remain pending. Everyone must understand the full project for viva.

`src/trafficml/` holds the existing data, baseline, and evaluation modules; `scripts/` holds commands; `tests/` contains regression checks; `configs/` contains provisional settings. `docs/PHASE1_PLAN_SUBMITTED_2026-10-25.md` preserves the submitted plan as history. `legacy_results/` in the local correction workspace preserves original outputs and is not published. New generated runs remain local.
