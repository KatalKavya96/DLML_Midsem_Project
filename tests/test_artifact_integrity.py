import numpy as np
import pytest

from trafficml.eval.predictions import (
    load_predictions,
    load_targets,
    save_predictions,
    save_targets,
)


def fixture_bundle(tmp_path):
    a, ids = np.array([11, 12]), ["a", "b"]
    y = np.full((2, 3, 2), 50.0, dtype=np.float32)
    save_targets("test", a, ids, y, tmp_path, context={"dataset_sha256": "synthetic"})
    save_predictions("model", "test", a, y + 1, tmp_path, sensor_ids=ids)
    return a, ids, y


def rewrite(path, **changes):
    with np.load(path) as f:
        data = {k: f[k] for k in f.files}
    data.update(changes)
    np.savez_compressed(path, **data)


def test_target_overwrite_rejected_for_data_and_context(tmp_path):
    a, ids, y = fixture_bundle(tmp_path)
    for target, context in [
        (y + 1, {"dataset_sha256": "synthetic"}),
        (y, {"dataset_sha256": "different"}),
    ]:
        with pytest.raises(ValueError, match="overwrite"):
            save_targets("test", a, ids, target, tmp_path, context=context)


@pytest.mark.parametrize("change", ["anchors", "sensor_ids", "fingerprint", "shape", "inf", "nan"])
def test_load_rejects_stale_misaligned_or_invalid_predictions(tmp_path, change):
    a, ids, y = fixture_bundle(tmp_path)
    data = {"anchors": a + 100} if change == "anchors" else {}
    if change == "sensor_ids":
        data["sensor_ids"] = np.array(ids[::-1])
    if change == "fingerprint":
        data["target_fingerprint"] = "stale"
    if change == "shape":
        data["y_pred"] = np.ones((2, 2, 2))
    if change in ("inf", "nan"):
        y[0, 0, 0] = np.inf if change == "inf" else np.nan
        data["y_pred"] = y
    rewrite(tmp_path / "model_test.npz", **data)
    with pytest.raises(ValueError):
        load_predictions("model", "test", tmp_path)


@pytest.mark.parametrize("value", [np.inf, -np.inf, np.nan])
def test_save_rejects_nonfinite_scored_predictions(tmp_path, value):
    a, ids, y = fixture_bundle(tmp_path)
    y[0, 0, 0] = value
    with pytest.raises(ValueError, match="non-finite"):
        save_predictions("bad", "test", a, y, tmp_path, sensor_ids=ids)


def test_save_rejects_sensor_order_and_load_rejects_tampered_targets(tmp_path):
    a, ids, y = fixture_bundle(tmp_path)
    with pytest.raises(ValueError, match="sensor order"):
        save_predictions("bad", "test", a, y, tmp_path, sensor_ids=ids[::-1])
    rewrite(tmp_path / "targets_test.npz", y_true=y + 2)
    with pytest.raises(ValueError, match="fingerprint"):
        load_targets("test", tmp_path)


def test_legacy_prediction_bundle_is_not_silently_accepted(tmp_path):
    a, _, y = fixture_bundle(tmp_path)
    np.savez_compressed(tmp_path / "legacy_test.npz", anchors=a, y_pred=y)
    with pytest.raises(ValueError, match="legacy"):
        load_predictions("legacy", "test", tmp_path)
