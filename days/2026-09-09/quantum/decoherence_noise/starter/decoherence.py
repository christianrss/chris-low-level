"""Simple decoherence noise channel."""

from __future__ import annotations


def depolarizing_channel(p0: float, p1: float, gamma: float) -> tuple[float, float]:
    """TODO [Q-DECO-CHANNEL-01]: return (p0', p1')."""
    raise NotImplementedError("Q-DECO-CHANNEL-01")


def apply_noise_step(probs: list[float], gamma: float) -> list[float]:
    """TODO [Q-DECO-APPLY-02]: one noise step."""
    raise NotImplementedError("Q-DECO-APPLY-02")


def trace_decoherence(p0: float, steps: int, gamma: float) -> list[float]:
    """TODO [Q-DECO-TRACE-03]: p0 trace over steps."""
    raise NotImplementedError("Q-DECO-TRACE-03")
