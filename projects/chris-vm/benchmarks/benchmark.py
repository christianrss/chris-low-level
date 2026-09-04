from __future__ import annotations

import argparse
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("exe", type=Path)
    parser.add_argument("--runs", type=int, default=30)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]

    with tempfile.TemporaryDirectory() as tmp:
        image = Path(tmp) / "arithmetic.clvm"
        subprocess.run(
            [
                sys.executable,
                str(root / "tools/assemble.py"),
                str(root / "programs/arithmetic.asm"),
                str(image),
            ],
            check=True,
        )
        command = [str(args.exe.resolve()), str(image)]

        for _ in range(5):
            subprocess.run(command, stdout=subprocess.DEVNULL, check=True)

        values: list[float] = []
        for _ in range(args.runs):
            start = time.perf_counter_ns()
            subprocess.run(command, stdout=subprocess.DEVNULL, check=True)
            elapsed_ms = (time.perf_counter_ns() - start) / 1e6
            values.append(elapsed_ms)

        print(
            f"runs={len(values)} "
            f"median_ms={statistics.median(values):.4f} "
            f"min_ms={min(values):.4f} "
            f"max_ms={max(values):.4f}"
        )
        print("note=process startup and I/O are included in this Day 01 baseline")


if __name__ == "__main__":
    main()
