# PEDAGOGY-TEST: GFX-GPU-TIMER-01
# PEDAGOGY-TEST: GFX-GPU-LAP-02
# PEDAGOGY-TEST: GFX-GPU-BENCH-03
# Caso 1: handle 0
# Caso 2: ms >= 0
# Caso 3: lap_times não vazio
# VISUAL-01: lap draw > 0 ms no relatório
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from gpu_timer import GpuTimerSim

def main():
    t = GpuTimerSim()
    h = t.begin_query("draw")
    ms = t.end_query(h)
    assert h == 0
    assert ms >= 0.0
    laps = t.lap_times()
    assert "draw" in laps
    print("OK gpu_timer")

if __name__ == "__main__":
    main()
