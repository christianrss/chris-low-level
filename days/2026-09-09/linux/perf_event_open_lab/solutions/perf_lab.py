"""perf_event_open subset simulation in Python."""

from __future__ import annotations


def perf_event_open(event_type: int, config: int) -> int:
    # PEDAGOGY-SOLUTION: LX-PERF-OPEN-01
    if event_type < 0:
        return -1
    return (event_type << 16) | (config & 0xFFFF)


def perf_event_read(fd: int, counters: dict[int, int]) -> int:
    # PEDAGOGY-SOLUTION: LX-PERF-READ-02
    return counters.get(fd, 0)


def perf_event_close(fd: int, counters: dict[int, int]) -> bool:
    # PEDAGOGY-SOLUTION: LX-PERF-CLOSE-03
    return counters.pop(fd, None) is not None
