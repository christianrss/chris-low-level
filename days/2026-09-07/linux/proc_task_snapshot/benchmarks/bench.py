import sys,time,statistics
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"solutions"))
from proc_snapshot import parse_stat
line="42 (worker pool) "+" ".join(["S","1"]+["0"]*9+["10","5"]+["0"]*4+["2","0","100"])
xs=[]
for _ in range(30):
 t=time.perf_counter_ns()
 for i in range(10000):parse_stat(line)
 xs.append((time.perf_counter_ns()-t)/1e6)
print(f"10000_parses median_ms={statistics.median(xs):.3f} min={min(xs):.3f} max={max(xs):.3f}")
