"""Pipeline State Object FSM — headless Python model."""
from __future__ import annotations

VALID_TRANSITIONS = {
    "UNINITIALIZED": {"VERTEX_SHADER"},
    "VERTEX_SHADER": {"FRAGMENT_SHADER"},
    "FRAGMENT_SHADER": {"READY"},
    "READY": {"RECORDING"},
    "RECORDING": {"READY"},
}


def can_transition(current: str, target: str) -> bool:
    """TODO [CAP-GFX-PSO-01]: check VALID_TRANSITIONS."""
    raise NotImplementedError("CAP-GFX-PSO-01")


def apply_transition(current: str, target: str) -> str:
    """TODO [CAP-GFX-PSO-02]: return target or raise ValueError."""
    raise NotImplementedError("CAP-GFX-PSO-02")


def pipeline_trace(states: list[str]) -> bool:
    """TODO [CAP-GFX-PSO-03]: validate full state sequence from UNINITIALIZED."""
    raise NotImplementedError("CAP-GFX-PSO-03")
