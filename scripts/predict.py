"""Forecast from saved local models at an observed origin, including the latest timestamp.

Only load trusted, locally generated joblib model artifacts.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from _common import load_config, load_series
from _provenance import validate_manifest
from xgboost import XGBRegressor

from trafficml.models.baselines import persistence


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", type=Path, required=True)
    p.add_argument("--sensor", required=True, help="Exact sensor ID from the manifest")
    p.add_argument("--at", default="latest", help="Observed forecast origin, or latest")
    args = p.parse_args()
    cfg = load_config()
    speed, values, all_ids, _ = load_series(cfg)
    manifest = validate_manifest(
        args.run_dir, cfg, Path(__file__).resolve().parents[1] / "configs/data.yaml"
    )
    ids = manifest["coverage_sensor_ids"]
    i = ids.index(args.sensor)
    original_i = all_ids.index(args.sensor)
    anchor = len(speed) - 1 if args.at == "latest" else speed.index.get_loc(pd.Timestamp(args.at))
    history, horizon = cfg["windows"]["history"], cfg["windows"]["horizon"]
    if not isinstance(anchor, (int, np.integer)) or anchor < history - 1:
        raise ValueError("forecast origin lacks a full input history")
    index = speed.index.append(
        pd.date_range(speed.index[-1] + pd.Timedelta(minutes=5), periods=horizon, freq="5min")
    )
    artifacts = joblib.load(args.run_dir / "preprocessing.joblib")
    fallback = artifacts["historical_average"].predict(np.array([anchor]), index, horizon)[0, :, i]
    raw = values[anchor - history + 1 : anchor + 1, original_i][None, :, None]
    preds = {
        "M0_persistence": persistence(raw, horizon, fallback[None, :, None])[0, :, 0],
        "M1_ha": fallback,
        "M3_rf": fallback.copy(),
        "M4_xgb": fallback.copy(),
    }
    features = artifacts["features"][i].transform(values[:, original_i], index, np.array([anchor]))
    forest = args.run_dir / "models/rf" / f"{i:03d}" / "forest.joblib"
    if forest.exists():
        preds["M3_rf"] = joblib.load(forest).predict(features)[0]
    for h in range(horizon):
        path = args.run_dir / "models/xgb" / f"{i:03d}" / f"h{h + 1:02d}.ubj"
        if path.exists():
            model = XGBRegressor()
            model.load_model(path)
            preds["M4_xgb"][h] = model.predict(features)[0]
    rows = [
        {
            "sensor": args.sensor,
            "origin": str(index[anchor]),
            "target": str(index[anchor + h]),
            "minutes": h * 5,
            **{m: float(v[h - 1]) for m, v in preds.items()},
        }
        for h in cfg["windows"]["report_horizons"]
    ]
    print(pd.DataFrame(rows).to_string(index=False, float_format=lambda x: f"{x:.2f}"))
    print("Speed forecasts only; no live traffic control. Units/timezone caveats: see report.")


if __name__ == "__main__":
    main()
