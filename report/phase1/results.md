# Phase 1 observed results

Generated from: `results/runs/phase1-full-v1`. This is an independent-sensor ML study; no graph model or signal controller is implemented.

## Evaluation status

Settings are selected only using val_tune. The test period was previously inspected; test results are exploratory, not an untouched final holdout. No classification accuracy percentage is claimed.

| Split | Model | Ahead (min) | MAE | RMSE | MAPE (%) | Valid points |
| --- | --- | --- | --- | --- | --- | --- |
| val_tune | M0_persistence | 15 | 3.099 | 5.810 | 7.35 | 344769 |
| val_tune | M0_persistence | 30 | 3.651 | 7.228 | 9.16 | 344764 |
| val_tune | M0_persistence | 60 | 4.471 | 9.074 | 11.76 | 344758 |
| val_tune | M1_ha | 15 | 4.603 | 8.543 | 12.63 | 344769 |
| val_tune | M1_ha | 30 | 4.599 | 8.537 | 12.61 | 344764 |
| val_tune | M1_ha | 60 | 4.584 | 8.516 | 12.53 | 344758 |
| val_tune | M3_rf | 15 | 2.793 | 5.122 | 7.28 | 344769 |
| val_tune | M3_rf | 30 | 3.286 | 6.174 | 9.01 | 344764 |
| val_tune | M3_rf | 60 | 3.849 | 7.235 | 10.86 | 344758 |
| val_tune | M4_xgb | 15 | 2.614 | 5.287 | 6.97 | 344769 |
| val_tune | M4_xgb | 30 | 3.075 | 6.467 | 8.94 | 344764 |
| val_tune | M4_xgb | 60 | 3.608 | 7.637 | 11.25 | 344758 |
| val_stack | M0_persistence | 15 | 3.350 | 6.244 | 8.36 | 310343 |
| val_stack | M0_persistence | 30 | 4.013 | 7.867 | 10.64 | 310342 |
| val_stack | M0_persistence | 60 | 5.140 | 10.184 | 14.48 | 310335 |
| val_stack | M1_ha | 15 | 4.054 | 7.614 | 12.89 | 310343 |
| val_stack | M1_ha | 30 | 4.057 | 7.616 | 12.90 | 310342 |
| val_stack | M1_ha | 60 | 4.061 | 7.619 | 12.90 | 310335 |
| val_stack | M3_rf | 15 | 2.864 | 5.338 | 8.06 | 310343 |
| val_stack | M3_rf | 30 | 3.299 | 6.249 | 9.81 | 310342 |
| val_stack | M3_rf | 60 | 3.746 | 7.089 | 11.72 | 310335 |
| val_stack | M4_xgb | 15 | 2.822 | 5.701 | 8.08 | 310343 |
| val_stack | M4_xgb | 30 | 3.276 | 6.868 | 10.28 | 310342 |
| val_stack | M4_xgb | 60 | 3.765 | 7.960 | 12.88 | 310335 |
| test | M0_persistence | 15 | 3.482 | 6.374 | 8.57 | 1246273 |
| test | M0_persistence | 30 | 4.173 | 7.983 | 10.77 | 1246258 |
| test | M0_persistence | 60 | 5.321 | 10.250 | 14.39 | 1246222 |
| test | M1_ha | 15 | 4.187 | 7.852 | 13.03 | 1246273 |
| test | M1_ha | 30 | 4.187 | 7.852 | 13.03 | 1246258 |
| test | M1_ha | 60 | 4.187 | 7.852 | 13.03 | 1246222 |
| test | M3_rf | 15 | 2.972 | 5.438 | 8.07 | 1246273 |
| test | M3_rf | 30 | 3.423 | 6.374 | 9.81 | 1246258 |
| test | M3_rf | 60 | 3.896 | 7.255 | 11.71 | 1246222 |
| test | M4_xgb | 15 | 2.920 | 5.777 | 8.04 | 1246273 |
| test | M4_xgb | 30 | 3.376 | 6.911 | 10.06 | 1246258 |
| test | M4_xgb | 60 | 3.874 | 7.993 | 12.59 | 1246222 |

## Implemented feature/model contract

207 sensors; 38 causal features; history 12 steps and 12 target horizons. Training anchors sampled every 2 steps to bound compute; full evaluation anchors retained.

RF is multi-output per sensor and drops incomplete training label vectors. XGBoost fits one estimator per sensor/horizon and drops that horizon's invalid training labels. Both use the same evaluation target masks. Missing/sparse training uses the predeclared historical-average fallback.

Selected settings:
```json
{
  "rf": {
    "n_estimators": 48,
    "max_depth": 12,
    "min_samples_leaf": 8,
    "max_features": 0.8
  },
  "xgb": {
    "n_estimators": 140,
    "max_depth": 3,
    "learning_rate": 0.06,
    "min_child_weight": 10,
    "subsample": 0.8,
    "colsample_bytree": 0.9,
    "objective": "reg:absoluteerror"
  }
}
```

## Interpretation

- val_tune, 15 minutes: lowest observed MAE is M4_xgb (2.614); 15.6% below persistence on this interval. This is a descriptive comparison, not a causal claim.
- val_tune, 30 minutes: lowest observed MAE is M4_xgb (3.075); 15.8% below persistence on this interval. This is a descriptive comparison, not a causal claim.
- val_tune, 60 minutes: lowest observed MAE is M4_xgb (3.608); 19.3% below persistence on this interval. This is a descriptive comparison, not a causal claim.
- val_stack, 15 minutes: lowest observed MAE is M4_xgb (2.822); 15.8% below persistence on this interval. This is a descriptive comparison, not a causal claim.
- val_stack, 30 minutes: lowest observed MAE is M4_xgb (3.276); 18.4% below persistence on this interval. This is a descriptive comparison, not a causal claim.
- val_stack, 60 minutes: lowest observed MAE is M3_rf (3.746); 27.1% below persistence on this interval. This is a descriptive comparison, not a causal claim.
- test, 15 minutes: lowest observed MAE is M4_xgb (2.920); 16.1% below persistence on this interval. This is a descriptive comparison, not a causal claim.
- test, 30 minutes: lowest observed MAE is M4_xgb (3.376); 19.1% below persistence on this interval. This is a descriptive comparison, not a causal claim.
- test, 60 minutes: lowest observed MAE is M4_xgb (3.874); 27.2% below persistence on this interval. This is a descriptive comparison, not a causal claim.

## Limitations

- Speed only; no measured flow, density, or occupancy is fabricated.
- Timezone/DST and separate raw-data redistribution rights remain unresolved.
- Six deterministic pilot sensors and two candidates per model form a budgeted search, not exhaustive tuning.
- Strided training and RF complete-label exclusion can affect model comparisons; see training_records.json.
- Calendar/time features do not give the models neighbouring-road information.
- Low-speed MAPE is unstable; headline conclusions should consider MAE/RMSE as well.
- Repeated time points/horizons are dependent; do not infer significance from sample size alone.
- No individual contributions or faculty acceptance are inferred from the presence of names or commits.

## Reproduction

```bash
python scripts/run_all.py --run-dir results/runs/new-experiment
python scripts/build_report.py --run-dir results/runs/new-experiment
```
