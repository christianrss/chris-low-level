from pathlib import Path
import sys, time
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from gossip import GossipNetwork, Message

N = 2000
net = GossipNetwork()
for i in range(N):
    net.connect(str(i), str((i + 1) % N))
    net.connect(str(i), str((i + 7) % N))
start = time.perf_counter()
reached = net.broadcast("0", Message("bench", "payload", ttl=N))
elapsed = time.perf_counter() - start
print(f"peers={N} reached={len(reached)} deliveries={len(net.deliveries)} seconds={elapsed:.6f}")
