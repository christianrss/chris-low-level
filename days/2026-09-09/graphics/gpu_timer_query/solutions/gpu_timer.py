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
        # PEDAGOGY-SOLUTION: GFX-GPU-TIMER-01
        h = self._next
        self._next += 1
        self._starts[h] = (name, self._clock())
        return h

    def end_query(self, handle: int) -> float:
        # PEDAGOGY-SOLUTION: GFX-GPU-LAP-02
        name, t0 = self._starts.pop(handle)
        ms = (self._clock() - t0) * 1000.0
        self._laps[name] = ms
        return ms

    def lap_times(self) -> dict[str, float]:
        # PEDAGOGY-SOLUTION: GFX-GPU-BENCH-03
        return dict(self._laps)
