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
        # PEDAGOGY-SOLUTION: CAP-AGENT-01
        key = (self.state, event)
        if key not in TRANSITIONS:
            return self.state
        self.state = TRANSITIONS[key]
        self.trace.append(self.state)
        return self.state

    def verify(self, passed: bool) -> str:
        # PEDAGOGY-SOLUTION: CAP-AGENT-02
        self.state = "VERIFY"
        return self.step("pass" if passed else "fail")


def replay(trace: list[str]) -> bool:
    # PEDAGOGY-SOLUTION: CAP-AGENT-03
    return len(trace) >= 1 and trace[-1] == "DONE"
