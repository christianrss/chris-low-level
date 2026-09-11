"""Composite input driver concept — HID + PS/2 → evdev."""
from __future__ import annotations

SYN_REPORT = 0


def register_device(name: str, capabilities: set[str]) -> dict:
    """TODO [CAP-LNX-COMP-01]: return device dict with name and caps."""
    raise NotImplementedError("CAP-LNX-COMP-01")


def hid_boot_to_evdev(report: bytes) -> list[tuple[int, int, int]]:
    """TODO [CAP-LNX-EVDEV-02]: map 8B HID boot to EV_KEY tuples (type=1)."""
    raise NotImplementedError("CAP-LNX-EVDEV-02")


def finalize_frame(events: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    """TODO [CAP-LNX-SYNC-03]: append SYN_REPORT (0,0,0) at end."""
    raise NotImplementedError("CAP-LNX-SYNC-03")
