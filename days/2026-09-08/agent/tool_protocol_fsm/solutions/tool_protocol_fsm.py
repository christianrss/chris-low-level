"""Tool calling FSM — IDLE→CALLING→WAITING→DONE/ERROR."""

from __future__ import annotations

TRANSITIONS = {
    ("IDLE", "call"): "CALLING",
    ("CALLING", "sent"): "WAITING",
    ("WAITING", "ok"): "DONE",
    ("WAITING", "err"): "ERROR",
}


class ToolProtocolFSM:
    def __init__(self):
        self.state = "IDLE"
        self.trace: list[str] = []

    def transition(self, event: str) -> str:
        # PEDAGOGY-SOLUTION: AGT-TOOL-01
        key = (self.state, event)
        if key not in TRANSITIONS:
            raise ValueError(key)
        self.state = TRANSITIONS[key]
        self.trace.append(f"{event}->{self.state}")
        return self.state

    def handle_response(self, ok: bool, payload: dict) -> dict:
        # PEDAGOGY-SOLUTION: AGT-TOOL-02
        self.transition("ok" if ok else "err")
        return {"state": self.state, "payload_keys": list(payload.keys())}

    def validate_tool_call(self, name: str, args: dict) -> bool:
        # PEDAGOGY-SOLUTION: AGT-TOOL-03
        return bool(name) and isinstance(args, dict)
