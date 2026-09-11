import sys,time,statistics,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"solutions"));from online_softmax import *
x=[random.Random(1).uniform(-20,20) for _ in range(10000)]
for _ in range(5):online_softmax(x)
a=[]
for _ in range(30):t=time.perf_counter_ns();online_softmax(x);a.append((time.perf_counter_ns()-t)/1e6)
print(f"median_ms={statistics.median(a):.4f} min_ms={min(a):.4f} max_ms={max(a):.4f}")
