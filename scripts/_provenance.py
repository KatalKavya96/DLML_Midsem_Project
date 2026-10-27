"""Run identity and evidence capture for the existing baseline pipeline."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

from _common import ROOT

from trafficml.data.splits import split_time_ranges


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def input_identity(cfg: dict, config_path: Path) -> dict:
    sources = sorted(
        [
            *ROOT.glob("src/**/*.py"),
            *ROOT.glob("scripts/*.py"),
            *ROOT.glob("configs/**/*.yaml"),
            ROOT / "pyproject.toml",
            ROOT / "requirements.txt",
        ]
    )
    return {
        "config_sha256": sha256(config_path),
        "data_sha256": {str(p.relative_to(ROOT)): sha256(p) for p in cfg["paths"].values()},
        "source_sha256": {str(p.relative_to(ROOT)): sha256(p) for p in sources},
    }


def create_manifest(run_dir, cfg, config_path, speed, splits, requested_splits) -> dict:
    run_dir = Path(run_dir)
    if run_dir.exists():
        raise ValueError("run directory already exists; choose a fresh --run-dir")
    identity = input_identity(cfg, config_path)
    git = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True, check=False
    )
    status = subprocess.run(
        ["git", "-C", str(ROOT), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=False,
    )
    manifest = {
        "schema": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "prototype correction verification; not final research results",
        "identity": identity,
        "config": config_path.read_text(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": {d.metadata["Name"]: d.version for d in metadata.distributions()},
        "git_base_commit": git.stdout.strip() if git.returncode == 0 else None,
        "git_worktree_dirty": bool(status.stdout.strip()) if status.returncode == 0 else None,
        "source_identity_note": "source_sha256 identifies working files, including local fixes",
        "command": [sys.executable, *sys.argv],
        "requested_splits": requested_splits,
        "partition_policy": "nominal anchor fractions; earlier partitions purged by horizon-1",
        "partitions": split_time_ranges(speed.index, splits, cfg["windows"]["horizon"])
        .astype(str)
        .to_dict(orient="records"),
        "sample_counts": {name: len(a) for name, a in splits.items()},
        "target_policy": "zero and non-finite sensor readings excluded; targets never imputed",
        "metric_policy": "micro-average valid target points per horizon; MAPE percent, no floor",
        "peak_policy": "weekday target hours [07,10),[16,19); provisional naive clock labels",
        "caveats": [
            "Dataset choice, roles and methodology are not accepted decisions.",
            "Timezone/DST is unresolved; peak/off-peak is a provisional clock-time slice.",
            "Original test results were already inspected; test is not a fresh holdout.",
        ],
    }
    run_dir.mkdir(parents=True)
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


def validate_manifest(run_dir, cfg, config_path) -> dict:
    manifest = json.loads((Path(run_dir) / "manifest.json").read_text())
    if manifest.get("schema") != 1 or manifest.get("identity") != input_identity(cfg, config_path):
        raise ValueError("dataset/config/source differs from the run manifest; create a new run")
    return manifest
