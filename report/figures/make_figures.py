"""Draw the congestion/error maps and feature-importance chart used in the report.

Uses only saved evidence from the full run (per-sensor test MAE and training audit) plus the
DCRNN sensor-graph files; nothing is retrained or re-scored.

Usage, from the repository root:
    PYTHONPATH=src python report/figures/make_figures.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from trafficml.data.graph import without_self_loops
from trafficml.data.load import load_dcrnn_adj, load_locations

ROOT = Path(__file__).resolve().parents[2]
GRAPH_DIR = ROOT / "data/raw/sensor_graph"


def draw_network(ax, xy: np.ndarray, adj: np.ndarray) -> None:
    """Light grey lines for every directed edge with nonzero kernel weight."""
    src, dst = np.nonzero(without_self_loops(adj))
    for i, j in zip(src, dst, strict=True):
        ax.plot(xy[[i, j], 0], xy[[i, j], 1], color="0.85", linewidth=0.6, zorder=1)


def sensor_map(ax, xy, adj, values, title, cmap, vmin, vmax, label):
    draw_network(ax, xy, adj)
    points = ax.scatter(
        xy[:, 0], xy[:, 1], c=values, cmap=cmap, vmin=vmin, vmax=vmax, s=16, zorder=2
    )
    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.xaxis.set_major_locator(plt.MaxNLocator(4))
    plt.colorbar(points, ax=ax, label=label, shrink=0.85)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--analysis-dir",
        type=Path,
        default=ROOT / "verification/full-phase1-20261026/analysis",
    )
    p.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    args = p.parse_args()

    ids, _, adj = load_dcrnn_adj(GRAPH_DIR / "adj_mx.pkl")
    locations = load_locations(GRAPH_DIR / "graph_sensor_locations.csv").set_index("sensor_id")
    xy = locations.loc[ids, ["longitude", "latitude"]].to_numpy()
    audit = pd.read_csv(args.analysis_dir / "sensor_audit.csv", dtype={"sensor_id": str})
    mae = pd.read_csv(args.analysis_dir / "per_sensor_mae_60.csv", dtype={"sensor_id": str})
    mae = mae.pivot(index="sensor_id", columns="model", values="mae_60").loc[ids]
    speed = audit.set_index("sensor_id").loc[ids, "train_mean_speed"].to_numpy()

    plt.rcParams.update(
        {
            "font.size": 9,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.dpi": 150,
            "savefig.bbox": "tight",
        }
    )

    fig, ax = plt.subplots(figsize=(6.5, 4))
    sensor_map(
        ax,
        xy,
        adj,
        speed,
        "Average training speed (low = congested)",
        "RdYlGn",
        30,
        70,
        "Mean speed (mph)",
    )
    fig.savefig(args.out / "congestion_map.png")
    plt.close(fig)

    persistence, xgb = mae["M0_persistence"].to_numpy(), mae["M4_xgb"].to_numpy()
    top = float(np.ceil(max(persistence.max(), xgb.max())))
    fig, axes = plt.subplots(1, 3, figsize=(16, 4), layout="constrained")
    sensor_map(
        axes[0],
        xy,
        adj,
        persistence,
        "Persistence: 60-min test MAE",
        "magma_r",
        0,
        top,
        "MAE (mph)",
    )
    sensor_map(axes[1], xy, adj, xgb, "XGBoost: 60-min test MAE", "magma_r", 0, top, "MAE (mph)")
    gain = persistence - xgb
    sensor_map(
        axes[2],
        xy,
        adj,
        gain,
        "MAE reduction (persistence - XGBoost)",
        "Greens",
        0,
        float(np.ceil(gain.max())),
        "mph",
    )
    fig.savefig(args.out / "error_maps.png")
    plt.close(fig)

    importance = pd.read_csv(args.analysis_dir / "feature_importance.csv")
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), layout="constrained")
    for ax, (model, name) in zip(axes, [("rf", "Random Forest"), ("xgb", "XGBoost")], strict=True):
        top = importance[importance.model == model].nlargest(10, "importance")[::-1]
        ax.barh(top.feature, top.importance, color="tab:blue" if model == "rf" else "tab:orange")
        ax.set_title(f"{name}: top 10 features")
        ax.set_xlabel("Mean importance over 207 sensors")
    fig.savefig(args.out / "feature_importance.png")
    plt.close(fig)
    print(f"figures written to {args.out}")


if __name__ == "__main__":
    main()
