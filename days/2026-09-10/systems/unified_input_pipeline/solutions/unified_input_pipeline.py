"""Unified input: keyboard + mouse → mux → transform."""
from __future__ import annotations

EVENT_SIZE = 24


def parse_keyboard_chunk(buf: bytes) -> list[tuple[int, int, int]]:
    # PEDAGOGY-SOLUTION: CAP-INP-KBD-01
    out = []
    for off in range(0, len(buf) - EVENT_SIZE + 1, EVENT_SIZE):
        t, c, v = int.from_bytes(buf[off+16:off+18], "little"), int.from_bytes(buf[off+18:off+20], "little"), int.from_bytes(buf[off+20:off+24], "little", signed=True)
        if t == 1:
            out.append((t, c, v))
    return out


def mux_streams(kbd: list[tuple[int, int, int]], mouse: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    # PEDAGOGY-SOLUTION: CAP-INP-MUX-02
    return kbd + mouse


def transform_events(events: list[tuple[int, int, int]]) -> list[str]:
    # PEDAGOGY-SOLUTION: CAP-INP-XFM-03
    out = []
    for t, c, v in events:
        if t == 1:
            out.append(f"KEY:{c}")
        elif t == 2:
            out.append(f"REL:{c}={v}")
    return out
