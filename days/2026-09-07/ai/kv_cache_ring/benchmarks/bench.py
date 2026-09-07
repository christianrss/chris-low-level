import sys,time,statistics
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"solutions"))
from kv_cache import KVCacheRing
c=KVCacheRing(8192)
for i in range(8192):c.append(i,i,i)
xs=[]
for _ in range(30):
 t=time.perf_counter_ns()
 for i in range(1000):c.window(8192-128,8192)
 xs.append((time.perf_counter_ns()-t)/1e6)
print(f"1000_windows median_ms={statistics.median(xs):.3f} min={min(xs):.3f} max={max(xs):.3f}")
