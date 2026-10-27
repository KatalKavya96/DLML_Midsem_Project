import json

import _provenance
import numpy as np
import pandas as pd
import pytest
from _provenance import create_manifest, validate_manifest

from trafficml.data.splits import chronological_split


@pytest.mark.parametrize("mutation", ["data", "config", "source"])
def test_manifest_detects_changed_input_and_refuses_existing_run(tmp_path, monkeypatch, mutation):
    monkeypatch.setattr(_provenance, "ROOT", tmp_path)
    (tmp_path / "pyproject.toml").write_text("# synthetic metadata")
    (tmp_path / "requirements.txt").write_text("# synthetic requirements")
    (tmp_path / "src").mkdir()
    source = tmp_path / "src" / "probe.py"
    source.write_text("# source version one")
    data = tmp_path / "data.csv"
    data.write_text("source version one")
    config = tmp_path / "config.yaml"
    config.write_text("synthetic config")
    cfg = {"paths": {"speed": data}, "windows": {"horizon": 3}}
    series = pd.DataFrame(
        np.ones((200, 1)), index=pd.date_range("2012-01-01", periods=200, freq="5min")
    )
    split = chronological_split(200, history=3, horizon=3)
    run = tmp_path / "run"
    manifest = create_manifest(run, cfg, config, series, split, ["val_tune"])
    assert manifest == validate_manifest(run, cfg, config)
    assert json.loads((run / "manifest.json").read_text())["sample_counts"]["test"] > 0
    with pytest.raises(ValueError, match="already exists"):
        create_manifest(run, cfg, config, series, split, ["val_tune"])
    {"data": data, "config": config, "source": source}[mutation].write_text("changed")
    with pytest.raises(ValueError, match="differs"):
        validate_manifest(run, cfg, config)
