"""Composite input driver concept — HID + PS/2 → evdev."""
from __future__ import annotations

SYN_REPORT = 0


def register_device(name: str, capabilities: set[str]) -> dict:
    # PEDAGOGY-SOLUTION: CAP-LNX-COMP-01
    return {"name": name, "capabilities": sorted(capabilities)}


def hid_boot_to_evdev(report: bytes) -> list[tuple[int, int, int]]:
    # PEDAGOGY-SOLUTION: CAP-LNX-EVDEV-02
    if len(report) != 8:
        return []
    return [(1, b, 1) for b in report[2:8] if b]


def finalize_frame(events: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    # PEDAGOGY-SOLUTION: CAP-LNX-SYNC-03
    return events + [(0, 0, 0)]
