# Integrated Phase 1 verification - 2026-10-27

Branch: kavya. Team base: canonical main f1ca84f6c40a79c88a3c9a689daf7a01bf35b29c, containing PRs #2-#5. This entry records actual integration checks, separate from the historical full experiment. No new training or test-driven model selection was performed.

## Completed checks

- Full real-data local suite: 56 passed, no skips. Invocation: PYTHONPATH=src:scripts /tmp/aml-repair-env/bin/python -m pytest -q -ra -p no:cacheprovider --basetemp=/tmp/dlml-kavya-integrated-tests.
- Ruff lint and format: passed for 37 Python files.
- uv dependency check: all 52 installed packages compatible. The uv-created test environment lacks pip; initial python -m pip commands failed for that reason, then the appropriate dependency/build tools succeeded. README setup uses a standard venv, which normally bootstraps pip.
- Package wheel built offline using setuptools.build_meta.build_wheel. Runtime dependency pins and original training source/data/config fingerprints unchanged.
- Real-data script: 207 sensors, 34,272 five-minute timestamps, 1,515 directed edges, DCRNN adjacency match, 8.11% missing; retained split counts 23,963 / 1,701 / 1,702 / 6,850.
- Saved-model prediction at latest sensor 773869 origin: manifest accepted and both learned estimators loaded. This is historical inference, not live traffic service or a newly measured generalization score.
- Current IEEE source compiled successfully with the desktop compiler. An exported final PDF and full page inspection remain separate gates.

## Documentation reconciliation

Corrected review logs 02-04 without rewriting original check outcomes or claiming student activity: masking policy versus physical zeros; duration-independent within-window fill; no universal future scaler mandate; descriptive versus causal/linear/graph claims; daily-profile minima 49.05 mph at 08:35 and 45.73 mph at 17:25; peak mask 07:00-10:00 and 16:00-19:00 weekdays; peak/off-peak 60-minute XGBoost MAE 6.31 / 3.26. Added the requirements/evidence map and explicit remaining submission gates.

## Scope

The original full-run scores remain exploratory because the test interval was already inspected. Existing 24 negative raw XGBoost forecasts remain disclosed and unchanged. No independently implemented member history, faculty acceptance, pristine holdout, Phase 2 implementation or zero-error guarantee is asserted. Remote CI and final PR acceptance are not claimed by local checks.

## Clean tracked-source verification

Exported only Git-tracked files from `212ebcd4833a4261102863fb0795b23f9ccd893d` into a fresh temporary directory with no raw data, saved runs or model binaries. Using the existing verified Python dependencies, pytest reported **54 passed, 2 skipped** (the two real-data checks correctly skipped because raw sensor files are excluded). This checks source closure, not a fresh installation/download of every dependency.

Ruff lint/format passed for 37 files. All eight CLI --help entrypoints imported successfully. The built pure-Python wheel imported outside either source checkout. Every frozen full-run runtime source/config/requirements hash matched the clean export, so no new model run was needed. Matplotlib emitted host font/cache warnings but returned success; the existing sandbox restricts normal home cache paths.

`checks.json` is a compact receipt. Later changes in this branch only record verification/documentation; runtime source is unchanged. No remote CI result or final-submission approval is inferred.
