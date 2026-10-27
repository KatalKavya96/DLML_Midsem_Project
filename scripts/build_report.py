# ruff: noqa: E501
"""Regenerate factual Markdown and LaTeX result tables from a verified experiment."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from _common import ROOT, load_config
from _provenance import validate_manifest


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", type=Path, required=True)
    args = p.parse_args()
    manifest = validate_manifest(args.run_dir, load_config(), ROOT / "configs/data.yaml")
    out = ROOT / "report/phase1"
    out.mkdir(parents=True, exist_ok=True)
    metrics = pd.read_csv(args.run_dir / "analysis/all_metrics.csv")
    chosen = metrics[(metrics["slice"] == "all") & metrics.h.isin([3, 6, 12])]
    lines = [
        "# Phase 1 observed results",
        "",
        "Generated from: `"
        + str(args.run_dir)
        + "`. This is an independent-sensor ML study; no graph model or signal controller is implemented.",
        "",
        "## Evaluation status",
        "",
        "Settings are selected only using val_tune. The test period was previously inspected; test results are exploratory, not an untouched final holdout. No classification accuracy percentage is claimed.",
        "",
        "| Split | Model | Ahead (min) | MAE | RMSE | MAPE (%) | Valid points |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in chosen.itertuples():
        lines.append(
            f"| {r.split} | {r.model} | {r.minutes} | {r.MAE:.3f} | {r.RMSE:.3f} | {r.MAPE:.2f} | {r.n_valid} |"
        )
    lines += [
        "",
        "## Implemented feature/model contract",
        "",
        f"{len(manifest['coverage_sensor_ids'])} sensors; {len(manifest['feature_names'])} causal features; history 12 steps and 12 target horizons. Training anchors sampled every {manifest['train_stride']} steps to bound compute; full evaluation anchors retained.",
        "",
        "RF is multi-output per sensor and drops incomplete training label vectors. XGBoost fits one estimator per sensor/horizon and drops that horizon's invalid training labels. Both use the same evaluation target masks. Missing/sparse training uses the predeclared historical-average fallback.",
        "",
        "Selected settings:",
        "```json",
        json.dumps(manifest["selected_parameters"], indent=2),
        "```",
        "",
        "## Interpretation",
        "",
    ]
    for split in ["val_tune", "val_stack", "test"]:
        part = chosen[chosen.split == split]
        for h in [3, 6, 12]:
            row = part[part.h == h].sort_values("MAE").iloc[0]
            baseline = part[(part.h == h) & (part.model == "M0_persistence")].iloc[0]
            change = 100 * (baseline.MAE - row.MAE) / baseline.MAE
            lines.append(
                f"- {split}, {h * 5} minutes: lowest observed MAE is {row.model} ({row.MAE:.3f}); {change:.1f}% below persistence on this interval. This is a descriptive comparison, not a causal claim."
            )
    lines += [
        "",
        "## Limitations",
        "",
        "- Speed only; no measured flow, density, or occupancy is fabricated.",
        "- Timezone/DST and separate raw-data redistribution rights remain unresolved.",
        "- Six deterministic pilot sensors and two candidates per model form a budgeted search, not exhaustive tuning.",
        "- Strided training and RF complete-label exclusion can affect model comparisons; see training_records.json.",
        "- Calendar/time features do not give the models neighbouring-road information.",
        "- Low-speed MAPE is unstable; headline conclusions should consider MAE/RMSE as well.",
        "- Repeated time points/horizons are dependent; do not infer significance from sample size alone.",
        "- No individual contributions or faculty acceptance are inferred from the presence of names or commits.",
        "",
        "## Reproduction",
        "",
        "```bash",
        "python scripts/run_all.py --run-dir results/runs/new-experiment",
        "python scripts/build_report.py --run-dir results/runs/new-experiment",
        "```",
        "",
    ]
    (out / "results.md").write_text("\n".join(lines))
    tex = [
        "\\begin{tabular}{llrrr}",
        "\\hline",
        "Method & min & MAE & RMSE & MAPE (\\%) \\\\",
        "\\hline",
    ]
    for r in chosen[chosen.split == "test"].itertuples():
        tex.append(
            f"{r.model.replace('_', ' ')} & {r.minutes} & {r.MAE:.2f} & {r.RMSE:.2f} & {r.MAPE:.2f} \\\\"
        )
    tex += ["\\hline", "\\end{tabular}"]
    (out / "metrics.tex").write_text("\n".join(tex) + "\n")
    (out / "run_reference.json").write_text(
        json.dumps({"run": str(args.run_dir), "identity": manifest["identity"]}, indent=2) + "\n"
    )
    print(out / "results.md")


if __name__ == "__main__":
    main()
