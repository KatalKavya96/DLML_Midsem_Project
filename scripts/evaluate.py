"""Score saved predictions: horizon-wise metrics per slice, leaderboard, optional DM tests.

Usage:
  python scripts/evaluate.py                          # all models with saved validation predictions
  python scripts/evaluate.py --split val_tune
  python scripts/evaluate.py --dm M0_persistence M1_ha
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from _common import ROOT, load_config
from _provenance import validate_manifest

from trafficml.data.load import load_sensor_ids, load_speed
from trafficml.eval.metrics import horizon_metrics
from trafficml.eval.predictions import available_models, load_predictions, load_targets
from trafficml.eval.significance import diebold_mariano, holm, loss_differential
from trafficml.eval.slices import time_slices


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=["val_tune", "val_stack", "test"], default="val_tune")
    parser.add_argument("--config", type=Path, default=ROOT / "configs/data.yaml")
    parser.add_argument("--run-dir", type=Path, default=ROOT / "results/runs/correction-v1")
    parser.add_argument("--models", nargs="*")
    parser.add_argument("--dm", nargs=2, metavar=("MODEL_A", "MODEL_B"))
    args = parser.parse_args()

    cfg = load_config(args.config)
    manifest = validate_manifest(args.run_dir, cfg, args.config)
    pred_dir = args.run_dir / "preds"
    tables = args.run_dir / "tables"
    index = load_speed(cfg["paths"]["speed_h5"], load_sensor_ids(cfg["paths"]["sensor_ids"])).index
    targets = load_targets(args.split, pred_dir)
    y_true, anchors = targets["y_true"], targets["anchors"]
    if json.loads(targets["metadata"].item())["context"] != manifest:
        raise ValueError("target context differs from run manifest")
    horizon = y_true.shape[1]
    slices = time_slices(index, anchors, horizon)
    models = args.models or available_models(args.split, pred_dir)

    if not models:
        raise ValueError("no predictions available for requested split")
    frames = []
    for model in models:
        y_pred = load_predictions(model, args.split, pred_dir)
        for name, mask in slices.items():
            m = horizon_metrics(np.where(mask, y_true, np.nan), y_pred, cfg["series"]["null_value"])
            frames.append(m.assign(model=model, slice=name))
    metrics = pd.concat(frames)[
        ["model", "slice", "h", "minutes", "n_valid", "MAE", "RMSE", "MAPE"]
    ]
    tables.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(tables / f"metrics_{args.split}.csv", index=False)

    report_h = cfg["windows"]["report_horizons"]
    board = metrics[metrics.h.isin(report_h)].pivot_table(
        index=["model", "slice"], columns="minutes", values=["MAE", "RMSE", "MAPE"]
    )
    board = board.reindex(columns=["MAE", "RMSE", "MAPE"], level=0)
    board.to_csv(args.run_dir / f"leaderboard_{args.split}.csv")
    with pd.option_context("display.float_format", "{:.2f}".format, "display.width", 140):
        for name in ("all", "peak", "off_peak"):
            print(f"\n== {args.split} / {name} ==")
            print(board.xs(name, level="slice"))

    if args.split == "test":
        print("Exploratory verification only: test results have already been inspected.")
    if args.dm:
        a, b = args.dm
        pred_a, pred_b = (
            load_predictions(a, args.split, pred_dir),
            load_predictions(b, args.split, pred_dir),
        )
        rows = []
        for h in range(1, horizon + 1):
            d = loss_differential(y_true[:, h - 1], pred_a[:, h - 1], pred_b[:, h - 1])
            rows.append({"h": h, **diebold_mariano(d, h)})
        dm = pd.DataFrame(rows)
        # This correction covers this model pair and these horizons only.
        # A future multi-ablation family needs joint adjustment across all tests.
        dm["p_holm"] = holm(dm["p_value"])
        dm.to_csv(tables / f"dm_{a}_vs_{b}_{args.split}.csv", index=False)
        print(f"\n== Diebold-Mariano {a} vs {b} (positive: {b} better) ==")
        print(dm[dm.h.isin(report_h)].to_string(index=False, float_format="{:.4g}".format))


if __name__ == "__main__":
    main()
