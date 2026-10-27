# Full Phase 1 experiment evidence

Actual 207-sensor experiment, completed locally on 2026-10-26. Runtime source identity is recorded in manifest.json. Training and prediction-artifact generation took 922.34 seconds; evaluation and figure/report generation ran afterward. Random Forest and XGBoost were selected on tuning data only. Test results are exploratory because the earlier prototype's test outputs were inspected.

56 local tests passed, including model reload equality and causal-feature checks. Lint, formatting and dependency checks passed. The IEEE source compiled successfully after an initial compiler dependency-download timeout. The 11-slide PPTX passed package/font/layout/chart-workbook checks; its rendered slides were inspected. It has not been opened in native PowerPoint.

No sparse-label model fallbacks were needed. Mean valid training-label fraction was 89.65% for RF and 92.87% for direct XGBoost. There were 24 negative raw XGBoost predictions among 17,015,400 test forecasts, retained in the measured scores rather than silently clipped. The model limitation is disclosed in the report and methods guide.

Raw datasets, virtual environments, serialized models and prediction arrays are excluded from this evidence folder. The local complete run retains them for prediction/reproduction. Model training uses a stride of two and a small pilot parameter search; this is not exhaustive optimization or prospective external validation.
