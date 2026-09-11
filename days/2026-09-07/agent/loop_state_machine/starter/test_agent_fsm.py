from agent_fsm import *

# Test cases (TESTES_GUIADOS.md):
# Caso 1: happy path PERCEIVE through VERIFY to DONE
# Caso 2: retry path REVISE after failed verify

a = AgentFSM(1)
# PEDAGOGY-TEST: D5-AGENT-TRANSITION
for e in ["perceived", "planned", "acted", "observed"]:
    a.transition(e)
# PEDAGOGY-TEST: D5-AGENT-VERIFY
assert a.verification(False, {"tests": 0}) == "REVISE"
a.transition("revised")
for e in ["planned", "acted", "observed"]:
    a.transition(e)
assert a.verification(True, {"tests": 5}) == "DONE"
# PEDAGOGY-TEST: D5-AGENT-REPLAY
assert replay(a.trace) == "DONE"
print("chris-agent-fsm tests passed")