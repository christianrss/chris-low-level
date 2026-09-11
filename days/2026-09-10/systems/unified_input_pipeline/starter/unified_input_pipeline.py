"""Unified input: keyboard + mouse → mux → transform."""
from __future__ import annotations

EVENT_SIZE = 24


def parse_keyboard_chunk(buf: bytes) -> list[tuple[int, int, int]]:
    """TODO [CAP-INP-KBD-01]: yield (type,code,value) for EV_KEY events in 24B records."""
    raise NotImplementedError("CAP-INP-KBD-01")


def mux_streams(kbd: list[tuple[int, int, int]], mouse: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    """TODO [CAP-INP-MUX-02]: interleave by timestamp order (type,code,value) tuples."""
    raise NotImplementedError("CAP-INP-MUX-02")


def transform_events(events: list[tuple[int, int, int]]) -> list[str]:
    """TODO [CAP-INP-XFM-03]: map to 'KEY:code' or 'REL:code=value' strings."""
    raise NotImplementedError("CAP-INP-XFM-03")
