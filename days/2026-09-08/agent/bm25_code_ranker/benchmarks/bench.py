import sys,time,statistics
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"solutions"));from bm25 import *
docs={f"f{i}.cpp":("allocator free slot " if i%50==0 else "tensor kernel stride ")*5 for i in range(5000)}
m=BM25(docs);a=[]
for _ in range(30):t=time.perf_counter_ns();m.rank("allocator slot");a.append((time.perf_counter_ns()-t)/1e6)
print(f"docs=5000 median_ms={statistics.median(a):.4f} min_ms={min(a):.4f} max_ms={max(a):.4f}")
