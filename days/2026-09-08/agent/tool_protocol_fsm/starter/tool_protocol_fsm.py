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
        """TODO [AGT-TOOL-01]: apply TRANSITIONS and append to trace."""
        raise NotImplementedError("AGT-TOOL-01")

    def handle_response(self, ok: bool, payload: dict) -> dict:
        """TODO [AGT-TOOL-02]: transition on ok/err; return evidence."""
        raise NotImplementedError("AGT-TOOL-02")

    def validate_tool_call(self, name: str, args: dict) -> bool:
        """TODO [AGT-TOOL-03]: name non-empty and args is dict."""
        raise NotImplementedError("AGT-TOOL-03")
