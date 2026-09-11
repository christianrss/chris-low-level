"""perf_event_open subset simulation in Python."""

from __future__ import annotations


def perf_event_open(event_type: int, config: int) -> int:
    """TODO [LX-PERF-OPEN-01]: return synthetic fd or -1."""
    raise NotImplementedError("LX-PERF-OPEN-01")


def perf_event_read(fd: int, counters: dict[int, int]) -> int:
    """TODO [LX-PERF-READ-02]: read counter value."""
    raise NotImplementedError("LX-PERF-READ-02")


def perf_event_close(fd: int, counters: dict[int, int]) -> bool:
    """TODO [LX-PERF-CLOSE-03]: remove fd from counters."""
    raise NotImplementedError("LX-PERF-CLOSE-03")
