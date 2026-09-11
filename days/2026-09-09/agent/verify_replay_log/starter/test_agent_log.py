# PEDAGOGY-TEST: AG-VERIFY-LOG-01
# PEDAGOGY-TEST: AG-REPLAY-FSM-02
# PEDAGOGY-TEST: AG-TRACE-HASH-03
# Caso 1: log len 1
# Caso 2: replay DONE
# Caso 3: hash 16 chars
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from agent_log import append_log, replay_fsm, trace_hash

def main():
    log: list[dict] = []
    append_log(log, "start", {})
    assert len(log) == 1
    append_log(log, "verify", {"ok": True})
    assert replay_fsm(log) == "DONE"
    h = trace_hash(log)
    assert len(h) == 16
    print("OK agent_log")

if __name__ == "__main__":
    main()
