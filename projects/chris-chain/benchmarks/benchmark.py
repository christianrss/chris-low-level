from pathlib import Path
import sys, time, statistics
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from toy_chain import Block

for difficulty in (1, 2, 3):
    samples=[]
    nonces=[]
    for i in range(20):
        b=Block(1,"0"*64,[f"tx-{i}"],i)
        start=time.perf_counter(); b.mine(difficulty); samples.append(time.perf_counter()-start); nonces.append(b.nonce)
    print(f"difficulty={difficulty} median_ms={statistics.median(samples)*1000:.3f} median_nonce={statistics.median(nonces)}")
