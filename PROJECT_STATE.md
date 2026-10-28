# Project state

Updated: 2026-10-28, Asia/Kolkata. Team T072, Section C.

## Current branch and integration

PRs #2–#6 are merged in canonical `main` at `b717675973aa32f966d7d38f177d08087013177c`. The owner authorized uploading the selected final report and presentation on 2026-10-28. Branch `kavya` was fast-forwarded to that main base before adding the three supplied binary artifacts and their documentation. New commits use Kavya Katal's configured identity without a co-author trailer. Publication is to the personal branch for review; no direct-main commit, direct-main push or merge is performed.

The supplied report has 17 pages, and the supplied presentation/PDF export have 8 slides/pages. Their original bytes are preserved under `report/final/` and `slides/final/`. The presentation's RMSE table and pilot-candidate labels disagree with the frozen evidence; see [correct values and import checks](docs/final_deliverables.md). Do not mark these numerical issues or final-submission acceptance resolved. Existing sources, generated results/provenance and contribution history are preserved.

The canonical project is this repository ROOT: src/trafficml/, scripts/, tests/, configs/, report/, slides/ and verification/. There is no nested AML/. Original Downloads/AML is unchanged. Delivery ZIPs/extractions, historical placeholders, unused data and private build files remain in the separate sibling DLML_Project_Archive_2026-10-27 archive; they are not submitted.

## Integrated implementation

Package 05 supplies the remaining pinned environment, model config, training/evaluation/prediction/report runners, CI, integrity/metric tests, small experiment evidence, literature/methods/contribution notes, IEEE source and 11-slide deck. At intake, every remaining Git-visible local file belonged to that package; newer shared docs were preserved. Added [requirements mapping](docs/02_requirements_traceability.md), truthful [Kavya review](docs/handoffs/05-kavya-integration/REVIEW_LOG.md) and [integration evidence](verification/integration-20261027/README.md). Corrected the deferred interpretations in member review logs without altering runtime code, scores or their historical check reports.

The study compares persistence, historical average, independent-sensor multi-output RF and direct-horizon XGBoost with 38 causal features, bounded validation-only tuning, training stride 2, purged chronology, common masked targets, EDA/error analysis and saved-model inference. No GAT, calibrated LWR, UI, stacking or traffic-signal simulation is implemented. Phase 2 remains deferred; any future control is simulated only.

## Recorded implementation verification — 2026-10-27

Full real-data suite: 56 passed without skips. Ruff lint/format passed for 37 Python files; uv checked 52 compatible installed packages. A wheel built offline with setuptools. The existing uv-created verification environment has no pip module, so the initial pip check/build attempts failed; alternative actual checks succeeded.

Real-data loading confirms 207 sensors, 34,272 five-minute timestamps, graph ordering/reference adjacency, 1,515 directed edges, 8.11% missing and split counts 23963/1701/1702/6850. Saved-model prediction loads and reproduces the working historical demo after validating unchanged source/config/data identity. The IEEE source compiled at its canonical root location. Previous rendered-slide inspection is preserved as historical evidence; no native PowerPoint test is claimed. A clean Git-tracked export passed 54 tests with two real-data skips, lint/format and all eight CLI import checks using the existing verified dependencies. The wheel imported outside the checkout; frozen runtime source hashes matched. The source snapshot is recorded in verification/integration-20261027/checks.json. No remote CI result is claimed before publication.

## Existing results and limits

The frozen full run remains local at results/runs/phase1-full-v1 with measured small evidence under verification/full-phase1-20261026/. XGBoost exploratory test MAE at 15/30/60 minutes is 2.9205 / 3.3764 / 3.8737, 16.1% / 19.1% / 27.2% below persistence. RF has lower headline RMSE. These are regression errors, not classification accuracy. The raw XGBoost tensor retains 24 negative predictions out of 17,015,400; no silent clipping or retuning occurred.

Original implementation and substantial owner/AI assistance remain disclosed. Member PR imports and agent reviews do not prove independent student authorship or understanding. See docs/CONTRIBUTIONS.md.

## Gates before final locking/submission

Review the integration PR and actual CI, export/inspect the final PDF, rehearse slides/viva, verify allowed assistance and genuine member contributions, and clarify project-specific flow/LWR scope versus speed-only Phase 1. Raw-data redistribution/timezone remain unresolved; the exposed test remains exploratory. Do not certify these gates from passing code checks alone. Data/models/predictions/environments/bundles remain excluded from Git.
