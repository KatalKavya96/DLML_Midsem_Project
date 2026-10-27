"""One command: train, evaluate three partitions, then generate EDA/error figures."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", type=Path, required=True)
    p.add_argument("--max-sensors", type=int, default=None, help="Development subset only")
    args = p.parse_args()
    scripts = Path(__file__).resolve().parent
    command = [sys.executable, str(scripts / "run_phase1.py"), "--run-dir", str(args.run_dir)]
    if args.max_sensors:
        command += ["--max-sensors", str(args.max_sensors)]
    subprocess.run(command, check=True)
    for split in ["val_tune", "val_stack", "test"]:
        subprocess.run(
            [
                sys.executable,
                str(scripts / "evaluate.py"),
                "--run-dir",
                str(args.run_dir),
                "--split",
                split,
                "--dm",
                "M4_xgb",
                "M0_persistence",
            ],
            check=True,
        )
    subprocess.run(
        [sys.executable, str(scripts / "build_analysis.py"), "--run-dir", str(args.run_dir)],
        check=True,
    )
    subprocess.run(
        [sys.executable, str(scripts / "build_report.py"), "--run-dir", str(args.run_dir)],
        check=True,
    )


if __name__ == "__main__":
    main()
