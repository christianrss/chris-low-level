import sys,time,statistics
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"solutions"))
from agent_fsm import AgentFSM
xs=[]
for _ in range(30):
 t=time.perf_counter_ns()
 for i in range(10000):
  a=AgentFSM(0)
  for e in ["perceived","planned","acted","observed"]:a.transition(e)
  a.verification(True,{"ok":1})
 xs.append((time.perf_counter_ns()-t)/1e6)
print(f"10000_loops median_ms={statistics.median(xs):.3f} min={min(xs):.3f} max={max(xs):.3f}")
