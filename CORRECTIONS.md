# Prototype correction record — 2026-10-25

## Scope and preservation

The owner requested correction of the review findings and publication to `KatalKavya96/DLML-sandbox` for review/testing. The original `/Users/kavyakatal/Downloads/AML` was left untouched. The working copy is `AML/` within the main project workspace. Original result files were copied unchanged to `legacy_results/` and are excluded from publication; the submitted plan is preserved in `docs/` with a historical-status banner.

## Corrections

1. **Boundary leakage:** retain nominal anchor partitions but purge each earlier partition by `horizon - 1`. Tests verify disjoint target timestamps and that mutating future validation data cannot change the fitted training profile.
2. **Stale/misaligned predictions:** immutable versioned targets include a fingerprint over anchors, sensor order, target values and run context. Prediction writers and readers validate alignment, schema and identity. Legacy bundles fail explicitly.
3. **Invalid values:** scored predictions must be finite. Target contracts reject infinities/nonpositive speeds; missing target entries use NaN. Metrics and significance utilities validate inputs and missingness consistently.
4. **Reproducibility:** use a fresh Python 3.12 environment, pinned direct/transitive package versions, and a package that declares actual runtime dependencies. Every run records the exact command, Python/packages/platform, source/config/data SHA-256 hashes, Git base revision/dirty status, split boundaries, metric policy and caveats. New runs never overwrite existing run directories.
5. **Unapproved decisions:** the active plan and README identify dataset/settings/roles as proposals and distinguish implemented components from future deliverables. The original plan is preserved. No UI, Phase 2, or new model implementation is added.

A run fingerprint guards against accidental artifact mixing, not malicious modification of every file together. Exact packages and checksums support reproduction; cross-platform numerical identity is not promised.

## Verification

Observed results in a clean Python 3.12.14 environment:

- **51 tests passed**, including real-data graph and speed-loader checks; no skipped tests in the local full-data run.
- Ruff lint and format checks passed for all 29 Python files. Dependency compatibility check passed.
- Data check: 34,272 timestamps and 207 sensors, 8.11% zero/NaN readings, and 1,515 directed edges excluding self-loops; constructed adjacency matched the supplied DCRNN reference.
- Retained sample counts: train 23,963; validation-tuning 1,701; reserved validation 1,702; test 6,850. Three sets of 11 crossing anchors were purged.
- Existing M0/M1 baselines were regenerated for all three evaluation partitions in a new run. Validation and test metric/DM commands completed successfully. No new ML models were trained.
- Small manifests and metric tables from this run are preserved under `verification/correction-20261025/`; generated prediction arrays remain local. Test outputs are exploratory because the original test results were already inspected.
- A basic GitHub Actions workflow was added. Its remote status is separate from these local verification results.

Commands actually run (the temporary environment's Python executable was used):

```bash
python -m pytest -q -p no:cacheprovider --basetemp=/tmp/aml-sandbox-final-tests
ruff check .
ruff format --check .
python scripts/check_data.py
python scripts/run_baselines.py --run-dir results/runs/correction-20261025 --splits val_tune val_stack test
python scripts/evaluate.py --run-dir results/runs/correction-20261025 --split val_tune --dm M1_ha M0_persistence
python scripts/evaluate.py --run-dir results/runs/correction-20261025 --split test --dm M1_ha M0_persistence
```

The supplied virtual environment could not start on this machine; attempts to reuse its native packages failed. It was not repaired or republished. A new isolated environment was built instead; `requirements.txt` captures its exact package versions. Initial sandbox network access failed, then the authorized dependency installation succeeded with network access.

## Remaining research questions

Formal dataset acceptance and licensing, project title/LWR scope, timezone/DST, peak definitions, member assignments, feature design, model/tuning choices, and future holdout protocol remain open. These are not bugs that an agent can approve on the team's behalf. Report low-speed MAPE sensitivity and the already-inspected test set explicitly. The correction does not complete the missing ML/EDA/report deliverables.
