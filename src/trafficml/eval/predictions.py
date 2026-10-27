"""Validated, versioned target/prediction bundles. Legacy bundles must be regenerated."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

PRED_DIR = Path(__file__).resolve().parents[3] / "results" / "preds"
SCHEMA = 2


def _path(pred_dir: Path, name: str, split: str) -> Path:
    if any(
        not s
        or any(
            c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in s
        )
        for s in (name, split)
    ):
        raise ValueError("model/split identifiers must use letters, digits, '_' or '-'")
    return Path(pred_dir) / f"{name}_{split}.npz"


def _fingerprint(anchors, sensor_ids, y_true, metadata: str) -> str:
    digest = hashlib.sha256(metadata.encode())
    for arr in (anchors, sensor_ids, y_true):
        digest.update(str((arr.dtype.str, arr.shape)).encode())
        # Canonicalize missing-value bytes before hashing.
        arr = np.where(np.isnan(arr), np.float32(np.nan), arr) if arr.dtype.kind == "f" else arr
        digest.update(np.ascontiguousarray(arr).tobytes())
    return digest.hexdigest()


def _validate_targets(anchors, sensor_ids, y_true) -> None:
    if anchors.ndim != 1 or not np.issubdtype(anchors.dtype, np.integer):
        raise ValueError("anchors must be 1D integers")
    if len(anchors) == 0 or np.any(anchors < 0) or np.any(np.diff(anchors) <= 0):
        raise ValueError("anchors must be nonempty, nonnegative and strictly increasing")
    if sensor_ids.ndim != 1 or len(sensor_ids) == 0 or len(set(sensor_ids)) != len(sensor_ids):
        raise ValueError("sensor_ids must be a nonempty unique sequence")
    if y_true.ndim != 3 or y_true.shape[0] != len(anchors) or y_true.shape[2] != len(sensor_ids):
        raise ValueError("target shape must be (anchors, horizon, sensors)")
    if y_true.shape[1] < 1 or np.isinf(y_true).any() or np.any(y_true[~np.isnan(y_true)] <= 0):
        raise ValueError("targets must be positive finite speeds or NaN for missing readings")


def save_targets(split, anchors, sensor_ids, y_true, pred_dir=PRED_DIR, *, context=None) -> Path:
    """Create immutable targets; identical repeated writes are allowed.

    ``context`` records dataset/configuration identity, normally the run manifest.
    Synthetic unit tests may use an empty context.
    """
    anchors = (
        np.asarray(anchors, dtype=np.int64)
        if np.asarray(anchors).dtype.kind in "iu"
        else np.asarray(anchors)
    )
    sensor_ids, y_true = np.asarray(sensor_ids, dtype=str), np.asarray(y_true, dtype=np.float32)
    _validate_targets(anchors, sensor_ids, y_true)
    metadata = json.dumps(
        {"schema": SCHEMA, "split": split, "context": context or {}},
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    identity = _fingerprint(anchors, sensor_ids, y_true, metadata)
    path = _path(pred_dir, "targets", split)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        old = load_targets(split, pred_dir)
        if old["fingerprint"].item() != identity:
            raise ValueError(
                "refusing to overwrite different targets/context; use a new run directory"
            )
        return path
    np.savez_compressed(
        path,
        anchors=anchors,
        sensor_ids=sensor_ids,
        y_true=y_true,
        metadata=metadata,
        fingerprint=identity,
    )
    return path


def load_targets(split, pred_dir=PRED_DIR) -> dict[str, np.ndarray]:
    path = _path(pred_dir, "targets", split)
    with np.load(path, allow_pickle=False) as f:
        required = {"anchors", "sensor_ids", "y_true", "metadata", "fingerprint"}
        if not required.issubset(f.files):
            raise ValueError("legacy/incomplete targets: regenerate in a new run directory")
        out = {k: f[k] for k in required}
    _validate_targets(out["anchors"], out["sensor_ids"], out["y_true"])
    meta = json.loads(out["metadata"].item())
    if meta.get("schema") != SCHEMA or meta.get("split") != split:
        raise ValueError("target schema/split mismatch")
    expected = _fingerprint(
        out["anchors"], out["sensor_ids"], out["y_true"], out["metadata"].item()
    )
    if out["fingerprint"].item() != expected:
        raise ValueError("target fingerprint mismatch")
    return out


def _validate_predictions(targets, anchors, sensor_ids, y_pred) -> None:
    if not np.array_equal(targets["anchors"], anchors) or y_pred.shape != targets["y_true"].shape:
        raise ValueError("prediction anchors or shape differ from targets")
    if not np.array_equal(targets["sensor_ids"], sensor_ids):
        raise ValueError("prediction sensor order differs from targets")
    scored = np.isfinite(targets["y_true"])
    if not np.isfinite(y_pred[scored]).all():
        raise ValueError("non-finite predictions (NaN/inf) on scored points")


def save_predictions(model, split, anchors, y_pred, pred_dir=PRED_DIR, *, sensor_ids) -> Path:
    if model.startswith("targets"):
        raise ValueError("model name uses reserved targets prefix")
    y_pred = np.asarray(y_pred, dtype=np.float32)
    targets = load_targets(split, pred_dir)
    _validate_predictions(targets, anchors, sensor_ids, y_pred)
    path = _path(pred_dir, model, split)
    np.savez_compressed(
        path,
        anchors=np.asarray(anchors),
        sensor_ids=np.asarray(sensor_ids, dtype=str),
        y_pred=y_pred,
        target_fingerprint=targets["fingerprint"],
        schema=SCHEMA,
    )
    return path


def load_predictions(model, split, pred_dir=PRED_DIR) -> np.ndarray:
    targets = load_targets(split, pred_dir)
    with np.load(_path(pred_dir, model, split), allow_pickle=False) as f:
        required = {"anchors", "sensor_ids", "y_pred", "target_fingerprint", "schema"}
        if not required.issubset(f.files):
            raise ValueError("legacy/incomplete predictions: regenerate in a new run directory")
        if (
            f["schema"].item() != SCHEMA
            or f["target_fingerprint"].item() != targets["fingerprint"].item()
        ):
            raise ValueError("prediction target fingerprint/schema mismatch")
        y_pred = f["y_pred"]
        _validate_predictions(targets, f["anchors"], f["sensor_ids"], y_pred)
    return y_pred


def available_models(split, pred_dir=PRED_DIR) -> list[str]:
    suffix = f"_{split}.npz"
    return sorted(
        p.name[: -len(suffix)]
        for p in Path(pred_dir).glob(f"*{suffix}")
        if not p.name.startswith("targets_")
    )
