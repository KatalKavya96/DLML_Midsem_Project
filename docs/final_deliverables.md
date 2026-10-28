# Owner-supplied Phase 1 report and presentation

Registered: 2026-10-28, Asia/Kolkata. The owner identified these three files as the final report/presentation and authorized adding and pushing them. “Final” records the owner's selected deliverables; it does not certify faculty acceptance or resolve the numerical discrepancies below.

## Files

- [Report PDF](../report/final/Traffic_Speed_Forecasting_T072.pdf) — 17 A4 pages.
- [PowerPoint presentation](../slides/final/Traffic_Speed_Forecasting_T072.pptx) — 8 slides.
- [Presentation PDF](../slides/final/Traffic_Speed_Forecasting_T072.pdf) — 8 landscape pages, supplied compressed export.

All three files are byte-identical copies of the supplied Downloads originals. Only their repository filenames were normalized. The 17-page PDF is the report; the compressed 8-page PDF is the presentation export, not a second report.

## Content discrepancies to resolve before submission

The supplied PPTX and presentation PDF are preserved unchanged. A limited content check found:

1. **Slide 6: the RMSE columns differ from the frozen experiment.** MAE headline values agree. The saved source of truth is [all_metrics.csv](../verification/full-phase1-20261026/analysis/all_metrics.csv), filtered to `split=test`, `slice=all` and horizons 3/6/12. Use the following RMSE values in mph:

| Method | Correct 15-minute RMSE | Correct 30-minute RMSE | Correct 60-minute RMSE |
| --- | ---: | ---: | ---: |
| Persistence | 6.374 | 7.983 | 10.250 |
| Historical average | 7.852 | 7.852 | 7.852 |
| Random Forest | 5.438 | 6.374 | 7.255 |
| XGBoost | 5.777 | 6.911 | 7.993 |

For example, the supplied slide shows RF 60-minute RMSE 5.487 and XGBoost 5.592, whereas the saved experiment gives 7.255 and 7.993. Do not treat those supplied RMSE columns as verified experiment results. The qualitative claim that RF has the lowest pooled headline RMSE remains supported by the saved values.

2. **Slide 4: pilot-candidate captions are misleading.** Values 3.829 vs 3.881 compare the two RF candidates; values 3.824 vs 3.413 compare the two XGBoost candidates. The supplied slide labels the alternatives “Historical Average,” which is not what [tuning.json](../verification/full-phase1-20261026/tuning.json) records. Relabel them as candidate comparisons.

No scores, model settings, experiment evidence or supplied artifact contents were changed during import. These issues are documented so the owner can correct the presentation in its source and supply replacement PPTX/PDF files together.

## Preservation and checks

Existing report sources, generated report tables/run reference, earlier presentation, package ownership inventory and contribution disclosures remain intact. The separately proposed PR #7 report/slides were not imported by this change.

Checks performed for this upload: both PDFs parse and are unencrypted without document JavaScript; PDF page counts checked; PPTX ZIP integrity and 8-slide structure checked, with no VBA project found; report cover and presentation results page visually inspected; copied-file SHA-256 values compared with their originals. This is a limited import check, not a full scientific/content/layout review or a fresh runtime test run. Native PowerPoint execution was not tested.

## Source filenames and SHA-256

### 17-page report

- Supplied filename: `Traffic_Speed_Forecasting_T072.pdf`
- Repository path: `report/final/Traffic_Speed_Forecasting_T072.pdf`
- Size: 311,490 bytes
- SHA-256: `95530e99dc21e75b911c23173b73b640cbcd02557ae15127f654daec65419315`

### 8-slide editable presentation

- Supplied filename: `Traffic_Speed_Forecasting_T072 (1).pptx`
- Repository path: `slides/final/Traffic_Speed_Forecasting_T072.pptx`
- Size: 20,406,944 bytes
- SHA-256: `6b905a4ea420b4e8db4a81d618d59a66d445c8e0cf16333a4a51219b2f5f78f2`

### 8-page presentation PDF export

- Supplied filename: `Traffic_Speed_Forecasting_T072 (1)_compressed.pdf`
- Repository path: `slides/final/Traffic_Speed_Forecasting_T072.pdf`
- Size: 1,311,559 bytes
- SHA-256: `dc85c3843b1e9b3887fa353483dfe789f8193bdef850100cb68ca0f33aba1bc2`
