"""Full measurement pipeline — Born rule + collapse + sample."""
from __future__ import annotations

import math


def born_probability(amplitude: complex) -> float:
    """TODO [CAP-Q-MEAS-01]: |amp|^2."""
    raise NotImplementedError("CAP-Q-MEAS-01")


def collapse(state: list[complex], index: int) -> list[complex]:
    """TODO [CAP-Q-MEAS-02]: basis state at index."""
    raise NotImplementedError("CAP-Q-MEAS-02")


def measure_sample(probs: list[float], u: float) -> int:
    """TODO [CAP-Q-MEAS-03]: inverse CDF with uniform u in [0,1)."""
    raise NotImplementedError("CAP-Q-MEAS-03")
