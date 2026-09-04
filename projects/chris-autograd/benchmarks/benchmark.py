from __future__ import annotations
import statistics, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'python'))
from linear_train import train

RUNS=50
for _ in range(5): train()
values=[]
for _ in range(RUNS):
    t0=time.perf_counter_ns(); train(); values.append((time.perf_counter_ns()-t0)/1e6)
print(f'implementation=python runs={RUNS} median_ms={statistics.median(values):.4f} min_ms={min(values):.4f} max_ms={max(values):.4f}')
