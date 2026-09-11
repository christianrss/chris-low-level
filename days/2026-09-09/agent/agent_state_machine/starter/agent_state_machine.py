from dataclasses import dataclass
STATES = ["PERCEIVE", "PLAN", "ACT", "OBSERVE", "VERIFY", "REVISE", "DONE", "FAILED"]

@dataclass(frozen=True)
class ToolResult:
    ok: bool
    evidence: str

def next_state(state, event):
    # TODO [D7-AGENT-TRANSITIONS]
    raise NotImplementedError("D7-AGENT-TRANSITIONS")

def run(task, tool, verify, max_retries=2):
    # TODO [D7-AGENT-RUN]
    # TODO [D7-AGENT-TRACE]
    raise NotImplementedError("D7-AGENT-RUN")
