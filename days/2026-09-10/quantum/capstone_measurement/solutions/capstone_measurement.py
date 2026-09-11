"""Full measurement pipeline — Born rule + collapse + sample."""
from __future__ import annotations

import math


def born_probability(amplitude: complex) -> float:
    # PEDAGOGY-SOLUTION: CAP-Q-MEAS-01
    return abs(amplitude) ** 2


def collapse(state: list[complex], index: int) -> list[complex]:
    # PEDAGOGY-SOLUTION: CAP-Q-MEAS-02
    n = len(state)
    out = [0j] * n
    out[index] = 1 + 0j
    return out


def measure_sample(probs: list[float], u: float) -> int:
    # PEDAGOGY-SOLUTION: CAP-Q-MEAS-03
    acc = 0.0
    for i, p in enumerate(probs):
        acc += p
        if u < acc:
            return i
    return len(probs) - 1 if probs else 0
