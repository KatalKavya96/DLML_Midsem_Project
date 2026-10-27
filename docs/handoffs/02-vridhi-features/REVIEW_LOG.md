# Vridhi Chaudhary - module review register

> Coordinator correction (2026-10-27, branch `kavya`): explanatory claims below were reconciled with the source code, measured tables and training profiles. Original agent/environment/check records remain historical self-reports; this edit does not certify student understanding.

Package prepared: 2026-10-27. Role: Missing-data handling, chronological splits and features.
Status: **integrated and agent-reviewed; member understanding/reproduction pending**. No individual implementation or completion is claimed.

Existing module provenance: teammate prototype and integrated owner-prepared extension with substantial AI assistance. Redistribution does not change authorship.

## Required review

Explain and verify causal filling, target masks, purge boundaries and all 38 features; record actual tests and useful changes.

## Agent integration and review (2026-10-27, Asia/Kolkata)

Performed by an Antigravity agent (Gemini 3.8 Flash) run by Vridhi Chaudhary under the Git identity `vridhichaudhary` (`vridhichaudhary05@gmail.com`). This records what the agent did; it is not evidence that Vridhi personally reproduced or understands the module.

### Integration

- Base: canonical `upstream/main` at `8bc3920` (merge of PR #2 from Rudraksh, containing coordination fix `5576750`). Branch: `vridhi02/vridhi-features`.
- All 7 payload files were verified against the package `MANIFEST.json` SHA-256 values, both in the extracted package `02-vridhi-features` and after copying into the repository root. All matched; no extra, missing or symlinked files. `COMMIT_PATHS.txt` matches the manifest and `docs/handoffs/FILE_OWNERSHIP.json`.
- None of the 7 paths existed on `main`, so there were no conflicts. Shared coordinator files (`AGENTS.md`, `PROJECT_STATE.md`, `.gitignore`, `README.md`, `CONTRIBUTING.md`, `docs/handoffs/*`) were preserved unchanged.
- No code changes: the review found no evidence-backed defect. Files are byte-identical to the package manifest, apart from this completed review log.

### Module summary (agent's description)

- `src/trafficml/data/masking.py`:
  Defines `NULL_VALUE = 0.0`. Under this benchmark policy, 0.0 mph is masked as a missing reading; this is not a universal physical rule about stopped traffic. Provides `valid_mask(x, null_value=0.0)` returning a boolean mask where readings are finite and non-zero, and `to_nan(x, null_value=0.0)` converting missing readings to `np.nan` (as float32) so missing observations cannot silently masquerade as valid zero-speed traffic in downstream calculations.
- `src/trafficml/data/splits.py`:
  Implements `anchor_indices(num_steps, history=12, horizon=12)` returning valid anchor indices where both full past history and future horizon windows lie strictly within series bounds. Implements `chronological_split(num_steps, history=12, horizon=12, train_frac=0.7, test_frac=0.2)` producing a `Splits` dataclass (`train`, `val_tune`, `val_stack`, `test`). Crucially enforces chronological target purging: discards the last `horizon - 1` (11 steps = 55 minutes) anchors of train, val_tune, and val_stack (`gap = horizon - 1`). This ensures that the forecast targets of an earlier partition $k$ (which reach up to anchor + horizon) terminate on or before the first anchor of the subsequent partition $k+1$ ($t_{k,\text{last}} + \text{horizon} \le t_{k+1,\text{first}}$), eliminating future target leakage across splits. Also provides `make_windows` to slice 2D data `(T, N)` into causal 3D windows `(S, history, N)` and targets `(S, horizon, N)`, and `split_time_ranges` for split audit verification.
- `src/trafficml/features/__init__.py`:
  Empty package marker file.
- `src/trafficml/features/temporal.py`:
  Implements `SensorFeatures(history=12, engineered=True)`. Computes a fallback median `self.median_` strictly on training observations. Slices causal historical windows `[anchor - history + 1 .. anchor]`. Handles missing observations causally: forward-fills left-to-right within each sample (`pd.DataFrame(raw).ffill(axis=1)`), with any remaining leading NaNs filled using the training median `self.median_`; no backward fill and no future readings are ever used. Generates exactly 38 causal features per sensor when `history=12` and `engineered=True`:
  1. 12 lag features (`lag_0` to `lag_11`, where `lag_0` is the most recent observation at anchor $t$)
  2. 12 missingness indicators (`missing_lag_0` to `missing_lag_11`)
  3. 9 summary statistics computed on causal imputed history: `mean_3`, `mean_6`, `mean_history`, `std_history`, `min_history`, `max_history`, 1-step difference (`difference_1`), full history difference (`difference_history`), and `missing_fraction`
  4. 5 cyclical clock and calendar features: `sin_time`, `cos_time` (normalized day fraction / 1440), `sin_week`, `cos_week` (normalized week fraction / 7), and boolean `weekend` indicator.
  No graph adjacency or future target-derived profiles are used.
- Inputs: 1D sensor arrays, 2D speed matrices `(T, N)`, pandas `DatetimeIndex`, integer anchor indices. Outputs: feature matrices `(num_anchors, 38)`, target matrices `(num_anchors, horizon)`, split index arrays.
- Dependencies: numpy, pandas; tests have cross-package dependencies on `trafficml.models.trees` and `scripts/run_baselines.py` (owned by package `04-bineet-models`).

### Checks run

Environment: macOS (Darwin 25.0.0), Anaconda Python 3.11.7 with numpy 1.26.4, pandas 2.1.4, tables 3.9.2, pytest 7.4.0, pyflakes 3.0.1. Run from repository root.

| Command | Outcome |
|---|---|
| Direct Python module verification (`valid_mask`, `to_nan`, `SensorFeatures`, `chronological_split`, partition sizes `[23963, 1701, 1702, 6850]`) | PASSED: 38 feature names generated, causal transform verified, partition sizes match exactly |
| `python -m pyflakes src/trafficml/data/masking.py src/trafficml/data/splits.py src/trafficml/features/ tests/test_features.py tests/test_splits.py` | PASSED: 0 findings |
| `PYTHONPATH=src pytest -q -ra tests/test_splits.py` | 13 passed, 1 failed (`test_future_validation_changes_cannot_change_fitted_profile`: `ModuleNotFoundError: No module named 'run_baselines'` from package 04) |
| `PYTHONPATH=src pytest -q -ra tests/test_features.py` | Blocked during collection: `ModuleNotFoundError: No module named 'trafficml.models'` (owned by package 04-bineet-models) |
| `PYTHONPATH=src pytest -q -ra tests/test_load.py tests/test_graph.py` | 5 passed, 2 skipped (data/raw not downloaded; package 01 tests) |
| `PYTHONPATH=src python scripts/check_data.py` | Successfully imported `trafficml.data.masking` and `trafficml.data.splits` (resolving package 01's ModuleNotFoundError); stopped on `FileNotFoundError` for raw sensor IDs (raw data excluded from Git) |
| `ruff check .` / `ruff format --check .` | Not run: ruff not installed in available environments |

The historical 56-test result is not a new run. Full test execution of `test_features.py` and `test_splits.py` requires package 04 (`trafficml.models.trees` and `scripts/run_baselines.py`).

### Observations and open questions

- Chronological boundary policy: our `chronological_split` purges `horizon - 1` anchors (11 five-minute steps for the configured horizon) at each boundary. Published benchmark scores must not be treated as equivalent-protocol comparisons without independently auditing their splits and masks.
- Validation partition allocation: The validation set is partitioned 50/50 into `val_tune` (for hyperparameter tuning) and `val_stack` (provisional future stacking partition). As noted in code docstrings, this remains a prototype setting pending coordinator confirmation.
- Cross-package coupling: `test_features.py` directly tests tree estimators (`trafficml.models.trees`) alongside features, and `test_splits.py` tests `fit_training_profile` from `run_baselines.py`. These tests verify end-to-end causal isolation and will execute cleanly once `04-bineet-models` is integrated.
- Feature scaling: current tree models use raw unscaled features. Scaling for any future model is a model-specific decision; if fitted, scaler statistics must use training data only. No future z-score requirement or exact invariance of approximate histogram implementations is asserted.

## Actual member activity (complete only after performing it)

- Performed on: pending (agent integration/review above on 2026-10-27)
- Registered on: 2026-10-27
- Files studied and explanation in your own words: pending
- Actual reproduction/check commands and environment: pending (agent checks recorded above)
- Actual outcomes, skips and failures: pending (agent results recorded above)
- Genuine fixes/tests/analysis/documentation added: none to code; this review log
- Assistance and existing work reused: prepared owner/AI-assisted source reused unchanged; integration, checks and this log written with Antigravity agent assistance
- Evidence paths or commit IDs: 6604d04, 3288405 on `vridhi02/vridhi-features`
- Reviewer and review date: pending human review
- Remaining limitations/questions: full test pass awaits package 04 integration; real-data checks await raw data download; human student understanding/reproduction pending.
