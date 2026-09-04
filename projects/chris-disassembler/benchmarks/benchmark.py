from __future__ import annotations

import argparse
import statistics
import subprocess
import time
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("tool", type=Path)
parser.add_argument("target", type=Path)
parser.add_argument("--runs", type=int, default=30)
args = parser.parse_args()

command = [str(args.tool.resolve()), str(args.target.resolve())]
for _ in range(5):
    subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )

values: list[float] = []
for _ in range(args.runs):
    start = time.perf_counter_ns()
    subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )
    values.append((time.perf_counter_ns() - start) / 1e6)

size = args.target.stat().st_size
print(
    f"bytes={size} runs={len(values)} "
    f"median_ms={statistics.median(values):.4f} "
    f"min_ms={min(values):.4f} "
    f"max_ms={max(values):.4f}"
)
print("note=process startup and textual rendering are included")
