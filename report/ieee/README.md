# IEEE report source

The report describes the actual independent-sensor experiment and its limitations. Generated table/image inputs must come from the same completed run. From the canonical repository root:

```bash
python scripts/build_report.py --run-dir results/runs/phase1-full-v1
mkdir -p report/ieee/images
cp report/phase1/metrics.tex report/ieee/metrics.tex
cp results/runs/phase1-full-v1/analysis/daily_profile.png report/ieee/images/
cp results/runs/phase1-full-v1/analysis/mae_horizons_test.png report/ieee/images/
cp results/runs/phase1-full-v1/analysis/forecast_example.png report/ieee/images/
```

Compile main.tex with an IEEEtran-capable LaTeX installation (run twice for references), or open this folder in Codex's LaTeX editor. The sources and supporting files remain together. Confirm all numbers/figures match the selected run before submitting. The team must review the text, source completeness, title/scope and actual contribution statement; this is not certification of individual understanding or faculty acceptance.

The IEEE narrative describes the complete 207-sensor run. Do not substitute a two-sensor development table or figures into that report. Regenerate results.md/metrics.tex from the selected full-coverage run immediately before copying its inputs.

The source has previously compiled successfully; an exported final PDF and its page-by-page layout review are separate final-submission tasks. Do not represent source compilation as a finished PDF export.
