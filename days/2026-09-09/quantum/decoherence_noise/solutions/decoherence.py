"""Simple decoherence noise channel."""

from __future__ import annotations


def depolarizing_channel(p0: float, p1: float, gamma: float) -> tuple[float, float]:
    # PEDAGOGY-SOLUTION: Q-DECO-CHANNEL-01
    mix = gamma / 2
    return (1 - gamma) * p0 + mix, (1 - gamma) * p1 + mix


def apply_noise_step(probs: list[float], gamma: float) -> list[float]:
    # PEDAGOGY-SOLUTION: Q-DECO-APPLY-02
    if len(probs) != 2:
        raise ValueError("2-level only")
    p0, p1 = depolarizing_channel(probs[0], probs[1], gamma)
    return [p0, p1]


def trace_decoherence(p0: float, steps: int, gamma: float) -> list[float]:
    # PEDAGOGY-SOLUTION: Q-DECO-TRACE-03
    cur = [p0, 1.0 - p0]
    trace = [cur[0]]
    for _ in range(steps):
        cur = apply_noise_step(cur, gamma)
        trace.append(cur[0])
    return trace
