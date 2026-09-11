"""Agent loop: perceive → verify → replay."""
from __future__ import annotations

TRANSITIONS = {
    ("PERCEIVE", "ok"): "VERIFY",
    ("VERIFY", "pass"): "DONE",
    ("VERIFY", "fail"): "REVISE",
    ("REVISE", "ok"): "PERCEIVE",
}


class AgentLoop:
    def __init__(self):
        self.state = "PERCEIVE"
        self.trace: list[str] = []

    def step(self, event: str) -> str:
        """TODO [CAP-AGENT-01]: apply TRANSITIONS, append state to trace."""
        raise NotImplementedError("CAP-AGENT-01")

    def verify(self, passed: bool) -> str:
        """TODO [CAP-AGENT-02]: drive VERIFY transitions."""
        raise NotImplementedError("CAP-AGENT-02")


def replay(trace: list[str]) -> bool:
    """TODO [CAP-AGENT-03]: ensure trace starts PERCEIVE and ends DONE."""
    raise NotImplementedError("CAP-AGENT-03")
