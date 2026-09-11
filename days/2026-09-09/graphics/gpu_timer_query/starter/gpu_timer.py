"""GPU timer query simulation (headless)."""

from __future__ import annotations

import time


class GpuTimerSim:
    def __init__(self) -> None:
        self._next = 0
        self._starts: dict[int, tuple[str, float]] = {}
        self._laps: dict[str, float] = {}

    def _clock(self) -> float:
        return time.perf_counter()

    def begin_query(self, name: str) -> int:
        """TODO [GFX-GPU-TIMER-01]: return query handle."""
        raise NotImplementedError("GFX-GPU-TIMER-01")

    def end_query(self, handle: int) -> float:
        """TODO [GFX-GPU-LAP-02]: end query, return ms."""
        raise NotImplementedError("GFX-GPU-LAP-02")

    def lap_times(self) -> dict[str, float]:
        """TODO [GFX-GPU-BENCH-03]: all completed laps."""
        raise NotImplementedError("GFX-GPU-BENCH-03")
