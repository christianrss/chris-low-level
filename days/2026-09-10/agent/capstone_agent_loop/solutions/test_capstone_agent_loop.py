# PEDAGOGY-TEST: CAP-AGENT-01
# PEDAGOGY-TEST: CAP-AGENT-02
# PEDAGOGY-TEST: CAP-AGENT-03
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from capstone_agent_loop import AgentLoop, replay

def main():
    ag = AgentLoop()
    ag.step("ok")
    ag.verify(True)
    assert ag.state == "DONE"
    assert replay(ag.trace)
    print("OK agent")

if __name__ == "__main__":
    main()
