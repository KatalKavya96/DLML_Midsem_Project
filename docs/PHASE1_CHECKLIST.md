# Phase 1 completion evidence

This is an implementation/evidence checklist, not a guarantee of faculty acceptance or individual viva readiness.

| Area | Implemented evidence / status |
| --- | --- |
| Data integrity | Actual METR-LA loader, sensor-order/frequency checks, adjacency match, masks and checksums. |
| Dataset suitability | Speed-only scope documented. Raw-data rights, timezone and the broader title/LWR requirements remain unresolved. |
| Literature | Six-source synthesis and source-scope disclosures in LITERATURE.md; no claim every student has read the papers. |
| Features | 38 causal features, training-only median fallback and synthetic leakage/alignment tests. |
| Models | Existing M0/M1 plus RF and XGBoost code; completed full 207-sensor run; see verification/full-phase1-20261026/. |
| Validation | Predeclared two-candidate search on six deterministic pilot sensors; no test-driven selection. |
| Evaluation | Common twelve-horizon target grid, MAE/RMSE/MAPE with valid counts and traffic-period slices. |
| EDA and errors | Reproducible plot script; full-run figures generated and inspected; accompanying tables retained. |
| Reproducibility | Pinned Python dependencies, macOS OpenMP prerequisite, run hashes/configs/commands, saved models, tests and CI configuration. |
| Report | IEEE LaTeX source plus generated tables and methods/limitations; compiled successfully with the desktop editor compiler. |
| Presentation | 11-slide editable PPTX uses measured full-run data; rendered slides inspected and checks passed. |
| Individual contribution | Actual work/AI assistance disclosed. Names or redistributed file commits do not certify participation. |
| Viva | Full methods/question guide supplied. Each person must learn, demonstrate and defend the work themselves. |

The prior test interval was inspected; all later test comparisons remain exploratory. No result is a classification accuracy percentage. No GAT, LWR simulator, live traffic control, independent member authorship or fresh holdout is claimed.

## Final submission gates still requiring review

- Reconcile the full project-specific brief/faculty expectations with speed-only Phase 1. [Requirement mapping](02_requirements_traceability.md) records current evidence without approving unresolved scope.
- Review/export the final IEEE PDF and inspect its pages; compiling TeX alone is not an exported submission PDF.
- Review the report, slides, literature-source scope and allowed-assistance policy with the team. Each member must demonstrate understanding and accurately record actual activity.
- Keep raw-data rights/timezone and exposed-test qualifications visible. Do not turn MAPE into an accuracy score or silently clip predictions.
- Review the integration PR and its CI result before freezing a final submission revision. A local pass is not a remote-CI pass.
