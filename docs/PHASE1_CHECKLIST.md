# Phase 1 completion evidence

This is an implementation/evidence checklist, not a guarantee of faculty acceptance or individual viva readiness.

| Area | Implemented evidence / status |
| --- | --- |
| Data integrity | Actual METR-LA loader, sensor-order/frequency checks, adjacency match, masks and checksums. |
| Dataset suitability | The Project 4 brief recommends starting with METR-LA, so speed-only Phase 1 matches it; flow/occupancy would need PeMS. The brief does not require calibrated LWR. Raw-data rights and timezone remain unresolved. |
| Literature | Eleven-source register in LITERATURE.md, including the brief's GAT and CityFlow pre-reads; no claim every student has read the papers. |
| Features | 38 causal features, training-only median fallback and synthetic leakage/alignment tests. |
| Models | Existing M0/M1 plus RF and XGBoost code; completed full 207-sensor run; see verification/full-phase1-20261026/. |
| Validation | Predeclared two-candidate search on six deterministic pilot sensors; no test-driven selection. |
| Evaluation | Common twelve-horizon target grid, MAE/RMSE/MAPE with valid counts and traffic-period slices. |
| EDA and errors | Reproducible plot script; full-run figures generated and inspected; accompanying tables retained. |
| Reproducibility | Pinned Python dependencies, macOS OpenMP prerequisite, run hashes/configs/commands, saved models, tests and CI configuration. |
| Report | New IEEE report at report/main.tex (2026-10-27) covering every rubric and brief item, with congestion/error maps; numbers taken from the full run. Compiled to report/phase1_report.pdf (8 pages). |
| Presentation | Earlier 11-slide PPTX removed at the team's request (2026-10-27); new 10-slide simple-language deck at slides/phase1_presentation.pptx (one slide per module), speaker guide in slides/SLIDE_CONTENT.md. |
| Individual contribution | Actual work/AI assistance disclosed. Names or redistributed file commits do not certify participation. |
| Viva | Full methods/question guide supplied. Each person must learn, demonstrate and defend the work themselves. |

The prior test interval was inspected; all later test comparisons remain exploratory. No result is a classification accuracy percentage. No GAT, LWR simulator, live traffic control, independent member authorship or fresh holdout is claimed.

## Final submission gates still requiring review

- The Project 4 brief is now mapped item by item in the [requirement mapping](02_requirements_traceability.md); confirm with faculty only if the speed-only (no flow/occupancy) baseline is questioned.
- Team review of report/phase1_report.pdf and slides/phase1_presentation.pptx; rehearse the presentation.
- Review the report, slides, literature-source scope and allowed-assistance policy with the team. Each member must demonstrate understanding and accurately record actual activity.
- Keep raw-data rights/timezone and exposed-test qualifications visible. Do not turn MAPE into an accuracy score or silently clip predictions.
- Review the integration PR and its CI result before freezing a final submission revision. A local pass is not a remote-CI pass.
