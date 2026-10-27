# Anshuman Mehta - module review register

> Coordinator correction (2026-10-27, branch `kavya`): explanatory claims below were reconciled with the source code, measured tables and training profiles. Original agent/environment/check records remain historical self-reports; this edit does not certify student understanding.

Package prepared: 2026-10-27. Role: Dataset EDA and interpretation.
Status: **integrated and agent-reviewed; member understanding/reproduction pending**. No individual implementation or completion is claimed.

Existing module provenance: teammate prototype and integrated owner-prepared extension with substantial AI assistance. Redistribution does not change authorship.

## Required review

Review training-only plots and write findings/implications for missingness, outages, speed distribution and calendar profiles.

## Agent integration and review (2026-10-27, Asia/Kolkata)

Performed by an Antigravity agent (Gemini 3.8 Flash) run by Anshuman Mehta under the Git identity `Anshuman-utd` (`anshumanmehta11@gmail.com`). This records what the agent did; it is not evidence that Anshuman personally reproduced or understands the module.

### Integration

- Base: canonical `upstream/main` at `db8d3a5` (merge of PR #3 from Vridhi Chaudhary, containing PR #2 from Rudraksh Sharma and coordination fix `5576750`). Branch: `anshuman03/eda`.
- All 12 payload files were verified against the package `MANIFEST.json` SHA-256 values, both in the extracted package `03-anshuman-eda` and after copying into the repository root. All matched identically; no extra, missing or symlinked files. `COMMIT_PATHS.txt` matches the manifest and `docs/handoffs/FILE_OWNERSHIP.json`.
- None of the 12 paths existed on `main`, so there were no merge conflicts. Shared coordinator files (`AGENTS.md`, `PROJECT_STATE.md`, `.gitignore`, `README.md`, `CONTRIBUTING.md`, `docs/handoffs/*`) were preserved unchanged.
- No code changes: the review found no evidence-backed defect in the prepared scripts or visualizations. Files are byte-identical to the package manifest, apart from this completed review log.

### Module summary (agent's description)

- `scripts/build_analysis.py`:
  Generates training-focused exploratory data analysis (EDA), dataset audits, and forecast/error evaluation visualizations from a completed experiment run. Key features:
  1. Accepts `--run-dir` and validates run provenance via `_provenance.validate_manifest`.
  2. Enforces strict training isolation: restricts distribution plots, missingness/outage analysis, sensor means and diurnal profiles to training steps (`end = int(splits.train[-1] + cfg["windows"]["horizon"] + 1)`, `train = values[:end]`), while the explicitly labeled global audit fields (overall missing fraction, observed min/max, shape and full date range) summarize the full file. Evaluation plots separately use their named held-out splits.
  3. Audits missing data and sensor statistics: outputs `dataset_audit.json` (recording overall missing fraction 8.11%, training missing fraction 7.13%, total outage runs 17,867, longest outage 5,800 min, observed speed range 0.33–70.0 mph, and 1,301 training steps with all 207 sensors missing) and `sensor_audit.csv` (sensor ID, training missing fraction, and training mean speed for all 207 detectors).
  4. Generates 6 core training EDA figures:
     - `speed_distribution.png`: Histogram of valid training speeds showing the characteristic bimodal distribution of highway traffic.
     - `missingness.png`: Daily missingness fraction heatmap across all 207 sensors over the training period, visualizing outage clusters.
     - `outage_runs.png`: Log-log histogram of detector outage durations (in minutes).
     - `daily_profile.png`: Weekday vs. weekend mean speed diurnal curves across 24-hour clock time.
     - `speed_heatmap.png`: Matrix heatmap of 5-minute speed intervals across 207 sensors for the first training day.
     - `sensor_locations.png`: Spatial scatter map of sensor longitude/latitude coordinates colored by mean training speed.
  5. Post-run evaluation plots: When run against a completed model evaluation directory, additionally computes horizon MAE curves (`mae_horizons_<split>.png`), peak vs off-peak comparison bars (`peak_comparison_<split>.png`), illustrative 60-minute test forecast time series (`forecast_example.png`), and per-sensor/feature importance tables.
- `src/trafficml/viz/__init__.py`:
  Package marker for the visualization subpackage under `trafficml`.
- `notebooks/.gitkeep`:
  Preserves an otherwise empty directory; a .gitkeep file does not itself exclude scratch files.
- `verification/full-phase1-20261026/analysis/*`:
  Contains the 8 verified training EDA and audit artifacts from the historical full Phase 1 run (`results/runs/phase1-full-v1`), providing precomputed, auditable evidence for the team report.
- Inputs: `metr-la.h5` series, `graph_sensor_locations.csv`, `configs/data.yaml`, and run directories containing predictions/metrics tables. Outputs: 6 training EDA plots, audit JSON/CSV, evaluation plots, and importance tables.
- Dependencies: numpy, pandas, matplotlib; cross-package dependencies on `trafficml.data.load` (package 01), `trafficml.data.splits` (package 02), `_common.py`, `_provenance.py`, and `trafficml.eval.predictions` (package 05-kavya-integration).

### Findings and interpretation from EDA

1. **Missingness structure & outage runs:**
   - The METR-LA dataset exhibits an overall missing fraction of 8.11% (7.13% in the training split).
   - The benchmark policy masks zero and NaN readings as missing; zero speed is not universally an outage in physical traffic. Converting these to NaNs (as implemented in `trafficml.data.masking`) is critical so missing readings do not artificially skew speed distributions or masquerade as severe traffic jams.
   - Outages are strongly clustered: 17,867 distinct outage runs occur in the training split. While the distribution is heavy-tailed with the majority of outages lasting 5 to 30 minutes (1–6 steps), extended sensor dropouts reach up to 5,800 minutes (~4.0 days). Furthermore, 1,301 5-minute steps in the training partition have all 207 sensors missing simultaneously, indicative of system-wide data collection/telemetry outages.
   - Modeling implication: `SensorFeatures` forward-fills only within each sample history, then substitutes the training median for remaining leading gaps. An entirely missing history uses that median throughout. There is no explicit outage-duration threshold, interpolation-quality guarantee or verified reconstruction of missing observations. Target masking (`valid_mask`) is mandatory to avoid penalizing models for unobserved intervals.

2. **Speed distribution:**
   - The full-file audit reports observed speeds from 0.33 to 70.0 mph; the plotted histogram itself uses training readings only.
   - The histogram reveals a pronounced bimodal distribution: a sharp, dominant peak near free-flow highway speed (60–65 mph) where traffic operates most of the day, and a broad secondary shoulder between 10 and 45 mph representing congested traffic conditions.
   - Modeling implication: A multimodal marginal speed histogram does not establish the shape of conditional residuals or rule out linear regression. Tree ensembles are the implemented nonlinear candidates; their benefit is assessed against the measured baselines, not inferred from this histogram. No deep-model superiority was tested.

3. **Calendar and diurnal profiles:**
   - Weekday vs. weekend profiles exhibit fundamentally different dynamics:
     - Recomputing the exact training profile plotted here gives weekday minima of 49.05 mph at recorded 08:35 in the 06:00-10:00 interval, and 45.73 mph at 17:25 in the 15:00-19:00 interval. These are descriptive means, with unresolved timezone/DST.
     - The weekend profile differs from weekdays; detailed clock values should be taken from the plotted training aggregation rather than inferred commute labels.
   - Modeling implication: These associations motivate the calendar feature group (`sin_time`, `cos_time`, `sin_week`, `cos_week`, `weekend`). They do not establish causation or an isolated forecasting improvement; feature-group ablation was not performed.

4. **Spatial heterogeneity & network topology:**
   - The sensor scatter and first-training-day heatmap show variation across sensor locations and recorded time. No road-label join or repeated bottleneck identification is supplied, so particular freeway junctions, recurring corridor bottlenecks and physical propagation are not established.
   - Modeling implication: Spatial modeling is a future hypothesis. The current estimators are independent per sensor, and these plots do not demonstrate that graph input is necessary or beneficial.

### Checks run

Environment: macOS (Darwin 25.0.0), Python 3.14.2 with numpy 1.26.4, pandas 2.3.3. Run from repository root.

| Command | Outcome |
|---|---|
| SHA-256 payload manifest validation | PASSED: All 12 files match `03-anshuman-eda/MANIFEST.json` hashes byte-for-byte |
| Direct Python module verification (`PYTHONPATH=src python3 -c "import trafficml.viz"`) | PASSED: `trafficml.viz` imported successfully |
| Direct verification of `dataset_audit.json` | PASSED: Valid JSON, all 17 expected keys present, shape `[34272, 207]`, 17,867 outage runs, max outage 5,800 min |
| Direct verification of `sensor_audit.csv` | PASSED: Valid CSV, exactly 207 sensor rows + header, correct column schema |
| PNG artifact verification | PASSED: All 6 PNG files (`daily_profile.png`, `missingness.png`, `outage_runs.png`, `sensor_locations.png`, `speed_distribution.png`, `speed_heatmap.png`) have valid PNG headers, valid non-zero dimensions, and match manifest hashes |
| Python AST syntax parse of `scripts/build_analysis.py` and all repository Python files | PASSED: 16 files parsed cleanly with 0 syntax errors |
| `python3 -m py_compile scripts/build_analysis.py` | PASSED: 0 compilation errors |
| `python3 scripts/build_analysis.py --help` | Blocked: `ModuleNotFoundError: No module named 'matplotlib'` (matplotlib not installed in system Python environment; script also depends on package 05 for `_common`, `_provenance`, `trafficml.eval.predictions`) |
| `python3 -m unittest discover tests` | Blocked: `ModuleNotFoundError: No module named 'pytest'` in test suites |
| `python scripts/check_data.py` | Blocked: `ModuleNotFoundError: No module named 'tables'` (PyTables needed for `load.py`; package 01 check) |
| `ruff check .` / `ruff format --check .` | Not run: ruff not installed in available environment |

The historical 56-test result is not a new run. Full test and script execution requires an environment with matplotlib, pytest, tables, and the remaining packages (04-bineet-models and 05-kavya-integration).

### Observations and open questions

- Strict training isolation: Training distribution/pattern plots use `values[:end]`; global audit fields describe the full file, and evaluation figures use explicitly named splits. The test interval was already exposed, so this script is not proof of untouched final evaluation.
- Cross-package dependencies: `scripts/build_analysis.py` requires `_common.py`, `_provenance.py`, and `trafficml.eval.predictions` from package `05-kavya-integration`. These will resolve once package 05 is integrated.
- Raw data requirements: Generating new plots from raw data requires `metr-la.h5` and `graph_sensor_locations.csv` under `data/raw/`, which are excluded from Git per data redistribution policy.
- Timezone handling: As noted in `dataset_audit.json`, timestamps are naive (`timezone: None`). Whether daylight saving time transitions affect the 5-minute sampling intervals in METR-LA remains unverified in published benchmarks.

## Actual member activity (complete only after performing it)

- Performed on: pending (agent integration/review above on 2026-10-27)
- Registered on: 2026-10-27
- Files studied and explanation in your own words: pending
- Actual reproduction/check commands and environment: pending (agent checks recorded above)
- Actual outcomes, skips and failures: pending (agent results recorded above)
- Genuine fixes/tests/analysis/documentation added: none to code; this review log
- Assistance and existing work reused: prepared owner/AI-assisted source reused unchanged; integration, checks and this log written with Antigravity agent assistance
- Evidence paths or commit IDs: e75b4cd, 21c6ecc on `anshuman03/eda`
- Reviewer and review date: pending human review
- Remaining limitations/questions: full script execution awaits package 05 integration and environment packages (matplotlib, tables, pytest); raw data excluded from Git; human student understanding/reproduction pending.
