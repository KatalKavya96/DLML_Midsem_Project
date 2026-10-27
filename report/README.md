# Phase 1 project report (IEEE format)

`main.tex` is the Phase 1 report in IEEE conference format; the compiled report is [phase1_report.pdf](phase1_report.pdf) (8 pages). All figures it uses are in `figures/`.

## Compile

`phase1_report.pdf` was built with Tectonic 0.17 (`brew install tectonic`):

```bash
cd report
tectonic main.tex && mv main.pdf phase1_report.pdf
```

Overleaf or any TeX distribution with IEEEtran also works (`pdflatex main.tex` twice). Under XeTeX/Tectonic the preamble selects TeX Gyre Termes, a Times clone; pdfLaTeX uses IEEEtran's default Times.

## Where the numbers and figures come from

Every number in the report is taken from the full 207-sensor run recorded in [verification/full-phase1-20261026](../verification/full-phase1-20261026/):

- metric tables: `leaderboard_test.csv` and `analysis/all_metrics.csv` (test, val-tune, val-2; all/peak/off-peak/weekday/weekend)
- dataset statistics: `analysis/dataset_audit.json`, partitions and settings: `manifest.json`, tuning: `tuning.json`
- `missingness.png`, `daily_profile.png`, `speed_heatmap.png`, `mae_horizons_test.png`, `peak_comparison_test.png`, `forecast_example.png`: copied unchanged from `analysis/`

`congestion_map.png`, `error_maps.png` and `feature_importance.png` are drawn by `figures/make_figures.py` from the saved per-sensor errors, sensor audit and feature importances of that run, plus the DCRNN sensor-graph files in `data/raw/sensor_graph/`. Nothing is retrained or re-scored:

```bash
PYTHONPATH=src python report/figures/make_figures.py   # from the repository root
```

The script lives here rather than in `scripts/` on purpose: the run manifest hashes every file under `src/`, `scripts/` and `configs/`, so adding a file there would invalidate the frozen run.

If you make a new run, regenerate its analysis with `scripts/run_all.py`, point `make_figures.py --analysis-dir` at the new `analysis/` folder, and update the numbers in `main.tex` to match.
