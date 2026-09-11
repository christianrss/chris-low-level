# PEDAGOGY-TEST: Q-DECO-CHANNEL-01
# PEDAGOGY-TEST: Q-DECO-APPLY-02
# PEDAGOGY-TEST: Q-DECO-TRACE-03
# Caso 1: soma probs 1
# Caso 2: p0 diminui com gamma
# Caso 3: trace len steps+1
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from decoherence import depolarizing_channel, apply_noise_step, trace_decoherence

def main():
    p0, p1 = depolarizing_channel(1.0, 0.0, 0.1)
    assert abs(p0 + p1 - 1.0) < 1e-9
    nxt = apply_noise_step([1.0, 0.0], 0.2)
    assert nxt[0] < 1.0
    tr = trace_decoherence(1.0, 3, 0.1)
    assert len(tr) == 4
    print("OK decoherence")

if __name__ == "__main__":
    main()
