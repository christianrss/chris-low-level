# PEDAGOGY-TEST: CAP-GFX-PSO-01
# PEDAGOGY-TEST: CAP-GFX-PSO-02
# PEDAGOGY-TEST: CAP-GFX-PSO-03
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from pipeline_state_object import can_transition, apply_transition, pipeline_trace

def main():
    assert can_transition("UNINITIALIZED", "VERTEX_SHADER")
    assert apply_transition("READY", "RECORDING") == "RECORDING"
    seq = ["UNINITIALIZED", "VERTEX_SHADER", "FRAGMENT_SHADER", "READY", "RECORDING", "READY"]
    assert pipeline_trace(seq)
    print("OK pso")

if __name__ == "__main__":
    main()
