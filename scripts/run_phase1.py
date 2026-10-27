"""Train/tune independent-sensor RF/XGBoost, save real forecasts and fitted estimators.

python scripts/run_phase1.py --run-dir results/runs/phase1-v1
The test set has already been inspected: its outputs are exploratory, never tuning inputs.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import joblib
import numpy as np
import yaml
from _common import ROOT, load_config, load_series
from _provenance import create_manifest, sha256
from run_baselines import fit_training_profile

from trafficml.eval.predictions import save_predictions, save_targets
from trafficml.features.temporal import SensorFeatures
from trafficml.models.baselines import persistence
from trafficml.models.trees import fit_predict_sensor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/data.yaml")
    parser.add_argument("--model-config", type=Path, default=ROOT / "configs/phase1.yaml")
    parser.add_argument("--max-sensors", type=int, default=None, help="Development only; disclosed")
    args = parser.parse_args()
    if args.run_dir.exists():
        raise ValueError("run directory already exists; choose a fresh path")
    cfg = load_config(args.config)
    settings = yaml.safe_load(args.model_config.read_text())
    speed, values, ids, splits = load_series(cfg)
    history, horizon = cfg["windows"]["history"], cfg["windows"]["horizon"]
    if args.max_sensors:
        if not 1 <= args.max_sensors <= len(ids):
            raise ValueError("invalid sensor development subset")
        ids, values = ids[: args.max_sensors], values[:, : args.max_sensors]
    start = time.perf_counter()
    ha = fit_training_profile(values, speed.index, splits, horizon)
    eval_parts = [(name, a) for name, a in splits.items() if name != "train"]
    eval_anchors = np.concatenate([a for _, a in eval_parts])
    lengths = np.cumsum([0] + [len(a) for _, a in eval_parts])
    labels = values[eval_anchors[:, None] + np.arange(1, horizon + 1)]
    ha_pred = ha.predict(eval_anchors, speed.index, horizon)
    train = splits.train[:: settings["train_stride"]]
    train_end = int(splits.train[-1] + horizon + 1)
    tuned = {}
    tuning_rows = []
    pilots = np.unique(
        np.linspace(0, len(ids) - 1, min(settings["pilot_sensors"], len(ids)), dtype=int)
    )
    # Only val_tune labels are visible during selection. All models share the same pilot grid.
    tune = splits.val_tune
    for kind in ["rf", "xgb"]:
        scores = []
        for ci, params in enumerate(settings[kind + "_candidates"]):
            total, count = 0.0, 0
            for i in pilots:
                f = SensorFeatures(history).fit(values[:train_end, i])
                x = f.transform(values[:, i], speed.index, train)
                y = values[train[:, None] + np.arange(1, horizon + 1), i]
                xt = f.transform(values[:, i], speed.index, tune)
                fallback = ha.predict(tune, speed.index, horizon)[:, :, i]
                pred, _ = fit_predict_sensor(
                    kind,
                    x,
                    y,
                    xt,
                    fallback,
                    params,
                    settings["seed"],
                    settings["minimum_training_rows"],
                )
                true = values[tune[:, None] + np.array(cfg["windows"]["report_horizons"]), i]
                err = np.abs(pred[:, np.array(cfg["windows"]["report_horizons"]) - 1] - true)
                total += float(np.nansum(err))
                count += int(np.isfinite(err).sum())
            score = total / count
            scores.append(score)
            tuning_rows.append(
                {
                    "model": kind,
                    "candidate": ci,
                    "validation_mae": score,
                    "valid_count": count,
                    "pilot_sensor_ids": [ids[i] for i in pilots],
                    "params": params,
                }
            )
            print(f"TUNE {kind} candidate {ci}: val_tune MAE={score:.4f}", flush=True)
        tuned[kind] = settings[kind + "_candidates"][int(np.argmin(scores))]
    manifest = create_manifest(
        args.run_dir, cfg, args.config, speed, splits, [n for n, _ in eval_parts]
    )
    manifest.update(
        {
            "purpose": "Phase 1 experiment; validation-selected, test exploratory",
            "model_config": settings,
            "model_config_sha256": sha256(args.model_config),
            "selected_parameters": tuned,
            "coverage_sensor_ids": ids,
            "feature_names": SensorFeatures(history).names,
            "train_stride": settings["train_stride"],
            "selection_rule": "headline micro-MAE on fixed pilot sensors; val_tune only",
            "pilot_sensor_ids": [ids[i] for i in pilots],
        }
    )
    (args.run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (args.run_dir / "tuning.json").write_text(json.dumps(tuning_rows, indent=2) + "\n")
    pred_dir = args.run_dir / "preds"
    outputs = {
        "M0_persistence": np.empty_like(labels),
        "M1_ha": ha_pred,
        "M3_rf": np.empty_like(labels),
        "M4_xgb": np.empty_like(labels),
    }
    feature_list = []
    records = []
    for i, sensor in enumerate(ids):
        f = SensorFeatures(history).fit(values[:train_end, i])
        feature_list.append(f)
        x = f.transform(values[:, i], speed.index, train)
        y = values[train[:, None] + np.arange(1, horizon + 1), i]
        xe = f.transform(values[:, i], speed.index, eval_anchors)
        raw = values[eval_anchors[:, None] + np.arange(-history + 1, 1), i][:, :, None]
        outputs["M0_persistence"][:, :, i] = persistence(raw, horizon, ha_pred[:, :, i : i + 1])[
            :, :, 0
        ]
        row = {"sensor": sensor, "candidate_training_rows": len(train)}
        for kind, name in [("rf", "M3_rf"), ("xgb", "M4_xgb")]:
            began = time.perf_counter()
            pred, record = fit_predict_sensor(
                kind,
                x,
                y,
                xe,
                ha_pred[:, :, i],
                tuned[kind],
                settings["seed"],
                settings["minimum_training_rows"],
                True,
                args.run_dir / "models" / kind / f"{i:03d}",
            )
            outputs[name][:, :, i] = pred
            row[kind] = {**record, "seconds": time.perf_counter() - began}
        records.append(row)
        if i % 10 == 0 or i == len(ids) - 1:
            print(
                f"FIT {i + 1}/{len(ids)} sensors; elapsed {time.perf_counter() - start:.1f}s",
                flush=True,
            )
    for j, (split, anchors) in enumerate(eval_parts):
        section = slice(lengths[j], lengths[j + 1])
        save_targets(split, anchors, ids, labels[section], pred_dir, context=manifest)
        for name, pred in outputs.items():
            save_predictions(name, split, anchors, pred[section], pred_dir, sensor_ids=ids)
    joblib.dump(
        {"features": feature_list, "historical_average": ha}, args.run_dir / "preprocessing.joblib"
    )
    (args.run_dir / "training_records.json").write_text(json.dumps(records, indent=2) + "\n")
    (args.run_dir / "timing.json").write_text(
        json.dumps(
            {
                "total_seconds": time.perf_counter() - start,
                "sensors": len(ids),
                "all_horizons": horizon,
            },
            indent=2,
        )
        + "\n"
    )
    print(f"DONE {args.run_dir}; test output is exploratory, not an untouched holdout.", flush=True)


if __name__ == "__main__":
    main()
