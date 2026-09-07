"""HID boot report fuzz triage — magic, bounds, usage strings."""

from __future__ import annotations

import re
from typing import List

HID_BOOT_REPORT_LEN = 8


def validate_hid_boot_length(raw: bytes) -> bool:
    """TODO [RT-HID-MAGIC-01]: boot keyboard report must be exactly 8 bytes."""
    raise NotImplementedError("RT-HID-MAGIC-01")


def count_nonzero_key_slots(raw: bytes) -> int:
    """TODO [RT-HID-BOUNDS-02]: count usages in bytes 2..7 (ignore reserved byte 1)."""
    raise NotImplementedError("RT-HID-BOUNDS-02")


def extract_hid_usage_hex(raw: bytes) -> List[str]:
    """TODO [RT-HID-STRINGS-03]: format each nonzero usage as 'usage:0xNN'."""
    raise NotImplementedError("RT-HID-STRINGS-03")
