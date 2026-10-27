# Phase 1 methods and viva guide

## Problem in one sentence

Predict each traffic sensor's future speed from its own recent speed history and recorded calendar time, then compare learned tree models against simple baselines. This is regression, not classification or traffic-signal control.

## The data

The inspected METR-LA file is a timestamp-by-sensor speed matrix with 34,272 rows and 207 sensors at five-minute intervals. Its one measured channel is speed. The benchmark source describes speed in mph. No separate measured flow or occupancy channels are present in this matrix. Speed is distance/time; flow is vehicles/time; density is vehicles/distance; occupancy is the fraction of detector time covered by vehicles. These quantities are related but not interchangeable.

Zeros are masked under the benchmark's missing-reading convention. That is an evaluation policy, not proof that a zero from every real-world traffic sensor must mean an outage. NaN is also missing; malformed infinite/negative raw speeds are rejected. Quality figures are generated from the actual file, not copied from a paper.

## Forecasting formulation

For sensor i and forecast origin t, let x(t,i) contain 12 observations ending at t: t-11 through t (t-55 minutes through t for five-minute sampling). Features use those observations and calendar values already known at t. For h=1,...,12, predict v(t+h,i). Our headline offsets h=3,6,12 mean 15,30,60 minutes ahead. Prediction arrays retain all 12 offsets.

There is one independent model per sensor for Random Forest and one per sensor/horizon for XGBoost. Calendar features repeat deterministically. No neighbouring sensor's speed enters these estimators. A road adjacency matrix has been verified for context and future work; this does not make the current predictors graph-aware.

## Chronology and leakage

The nominal anchor proportions are 70/10/20. Validation retains the prototype's two halves: val_tune for selection and val_stack as a separately reported interval; no stacker is implemented. Remove the final 11 anchors of every earlier partition so its last future target ends no later than the next partition's first forecast origin. Past input readings may cross a boundary because they are already observed at that origin.

All fitted feature medians and historical averages use the retained training interval only. No target is imputed. Tree training anchors are sampled every two steps to bound compute; the full prediction grid is evaluated. Random Forest and XGBoost share those candidate training anchors, but their valid-label rules differ and must be disclosed.

The old test interval was inspected before this extension. Parameters are selected only on val_tune; the existing test is reported as exploratory. An already-inspected dataset cannot be made pristine by renaming its split. Stronger generalization claims need a prospectively agreed additional holdout or validation protocol.

## Features: 38 values per sensor/sample

- 12 speed lags, with lag 0 the latest reading.
- 12 original missing-value flags, one per lag.
- Means over the last 3, 6 and 12 readings; standard deviation, minimum and maximum over the history.
- One-step difference, difference across the history, and missing fraction.
- Sine/cosine of recorded time of day and time of week, plus a weekend flag.

Within a sample, fill missing inputs from earlier observations in that same history, then use the training median for leading gaps. There is no backward fill. Statistics use this explicitly imputed history. Completely empty sensor-training history gives a deterministic feature fallback; prediction fallback is separately documented. Models do not use scalers. Missingness flags tell a model when an input is substituted. The timezone is unresolved, so calendar/peak labels refer to recorded clock values.

## Models

### M0 persistence

Repeat the last valid history reading for every horizon. If the whole window is missing, use the training historical average. It is inexpensive and sets a meaningful short-horizon reference.

### M1 historical average

For each sensor and time-of-week slot, average valid training observations. An unseen slot falls back to a time-of-day average and then the sensor's training mean. It captures recurring patterns but cannot react to an unexpected current incident.

### M3 Random Forest

An ensemble of bootstrap-trained regression trees averages their predictions. Feature subsampling reduces dependence among trees. Each sensor's forest jointly outputs all 12 future speeds. Under squared-error training, averaging tends toward conditional mean predictions. Target vectors with any missing horizon are excluded because the joint-label training rule requires complete vectors. This changes the training distribution, so exclusion counts are saved.

Parameters to explain: number of trees (ensemble size), depth (complexity), minimum leaf size (smoothness), and feature fraction (tree diversity). Bootstrap resampling inside training is not a random train/test split. OOB error is not our final forecasting evaluation.

### M4 XGBoost

Fit an additive sequence of small trees; later trees reduce the current objective. Each sensor/horizon gets its own direct regressor, with that horizon's missing labels excluded. Compare two predeclared configurations on six evenly spaced sensor indices in val_tune; select by pooled valid-point MAE at 15/30/60 minutes. Selected parameters are recorded before full-data comparisons. The candidates include squared-error and absolute-error objectives. The selected objective, not an assumed one, must be described in the report.

An objective can be written as sum of prediction losses plus tree-complexity regularization. Learning rate limits each new tree's contribution; depth and minimum child weight constrain complexity; row/column subsampling controls the training sample used inside a tree. This is a small budgeted search, not proof of globally optimal hyperparameters.

If too few valid labels exist for a sensor/model/horizon, use the predefined historical-average fallback and count it. Never remove difficult held-out targets only for the weaker model.

## Metrics

For valid targets, define e = prediction - actual. MAE = mean(abs(e)); RMSE = sqrt(mean(e squared)); MAPE = 100*mean(abs(e/actual)). MAE and RMSE have speed units. MAPE has percent units, excludes missing/zero targets, and can be unstable near zero. There is no classification accuracy and 100-MAPE is not a classification accuracy score.

Metrics pool valid sensor-time points at each horizon. All methods use the same targets and masks; valid counts are recorded. Peak windows are provisional weekdays 07:00-10:00 and 16:00-19:00 in recorded clock time. A single overall number can hide poor peak-period performance or large errors in RMSE.

The existing Diebold-Mariano utility compares a per-timestamp sensor-average loss differential using a HAC variance estimate. Its weighting differs from point-pooled MAE when valid sensor counts vary. Holm correction covers one declared comparison across horizons, not an unspecified collection of experiments. P-values are exploratory under the exposed test set and serial dependence; large sample size is not proof of practical benefit.

## Traffic theory and limits

The LWR conservation equation is partial rho/partial t + partial q/partial x = 0, with q=rho*v. A shock between two density/flow states has speed (q2-q1)/(rho2-rho1). This provides conceptual motivation for spatial dependence, not a calibrated result from our speed-only dataset. We have not measured density/flow states, estimated an LWR shock speed, implemented a GAT, or shown a graph model beats these baselines.

## Questions everyone should answer

1. What exactly is predicted, and in which units?
2. Why is a five-minute dataset's h=12 forecast one hour ahead?
3. What observations are available at forecast time?
4. Where could a feature or scaler leak future information?
5. Why purge windows if anchors are already chronological?
6. How are missing inputs different from missing targets?
7. Why does RF discard more training labels than a direct model?
8. Why can persistence be strong at short horizons?
9. How does bagging differ from boosting?
10. What settings were actually selected, and on which data?
11. Why can MAE and MAPE rank models differently?
12. Why do high RMSE and peak-period errors matter?
13. What does the verified road graph contribute to current prediction? (It is not used.)
14. Why can speed-only forecasts not demonstrate signal-control improvement?
15. What work was actually performed by each contributor and what assistance was used?

Use generated results.md and the run manifest for numerical answers; do not memorize invented claims.

## Observed output constraint limitation

The complete test tensor contains 24 negative raw XGBoost forecasts among 17,015,400 predictions. They were not silently clipped to improve reported errors. Regression trees do not automatically enforce physical bounds. A future version can predeclare a nonnegative-output rule and revalidate it; the current report preserves the measured raw outputs. RF and the two references had no negative forecasts in this check.
