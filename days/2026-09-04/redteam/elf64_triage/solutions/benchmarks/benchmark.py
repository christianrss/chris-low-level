from __future__ import annotations

import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from ascii_strings import extract_ascii_strings

for mib in (1, 4, 8):
    block = b"\x00" * 101 + b"PORTFOLIO_STRING_12345\x00"
    repeats = mib * 1024 * 1024 // len(block) + 1
    data = (block * repeats)[: mib * 1024 * 1024]

    for _ in range(2):
        extract_ascii_strings(data, 5)

    values: list[float] = []
    result = []
    for _ in range(5):
        start = time.perf_counter_ns()
        result = extract_ascii_strings(data, 5)
        values.append((time.perf_counter_ns() - start) / 1e9)

    median_seconds = statistics.median(values)
    print(
        f"size_mib={mib} strings={len(result)} "
        f"median_s={median_seconds:.6f} "
        f"throughput_mib_s={mib / median_seconds:.2f}"
    )
