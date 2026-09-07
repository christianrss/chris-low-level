import sys,time,statistics
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"solutions"))
from query import parse
q="lang:cpp AND (symbol:allocator OR text:\"arena\")"
xs=[]
for _ in range(30):
 t=time.perf_counter_ns()
 for i in range(5000):parse(q)
 xs.append((time.perf_counter_ns()-t)/1e6)
print(f"5000_parses median_ms={statistics.median(xs):.3f} min={min(xs):.3f} max={max(xs):.3f}")
