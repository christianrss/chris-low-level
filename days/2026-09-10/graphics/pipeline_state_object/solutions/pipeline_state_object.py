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
    # PEDAGOGY-SOLUTION: CAP-GFX-PSO-01
    return target in VALID_TRANSITIONS.get(current, set())


def apply_transition(current: str, target: str) -> str:
    # PEDAGOGY-SOLUTION: CAP-GFX-PSO-02
    if not can_transition(current, target):
        raise ValueError(f"invalid {current}->{target}")
    return target


def pipeline_trace(states: list[str]) -> bool:
    # PEDAGOGY-SOLUTION: CAP-GFX-PSO-03
    if not states or states[0] != "UNINITIALIZED":
        return False
    for a, b in zip(states, states[1:]):
        if not can_transition(a, b):
            return False
    return True
