# PEDAGOGY-TEST: AGT-TOOL-01
# PEDAGOGY-TEST: AGT-TOOL-02
# PEDAGOGY-TEST: AGT-TOOL-03
# Caso 1: IDLE call -> CALLING
# Caso 2: handle_response ok -> DONE
# Caso 3: validate_tool_call
# Caso 4: err path -> ERROR
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from tool_protocol_fsm import ToolProtocolFSM

def main():
    fsm = ToolProtocolFSM()
    assert fsm.transition("call") == "CALLING"
    fsm.transition("sent")
    ev = fsm.handle_response(True, {"result": 1})
    assert ev["state"] == "DONE"
    assert fsm.validate_tool_call("search", {})
    fsm2 = ToolProtocolFSM()
    fsm2.transition("call"); fsm2.transition("sent")
    fsm2.handle_response(False, {})
    assert fsm2.state == "ERROR"
    print("OK tool_protocol_fsm")

if __name__ == "__main__":
    main()
