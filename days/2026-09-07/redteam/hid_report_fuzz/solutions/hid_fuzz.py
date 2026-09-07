"""HID boot report fuzz triage — magic, bounds, usage strings."""

from __future__ import annotations

import re
from typing import List

HID_BOOT_REPORT_LEN = 8


def validate_hid_boot_length(raw: bytes) -> bool:
    # PEDAGOGY-SOLUTION: RT-HID-MAGIC-01
    return len(raw) == HID_BOOT_REPORT_LEN


def count_nonzero_key_slots(raw: bytes) -> int:
    # PEDAGOGY-SOLUTION: RT-HID-BOUNDS-02
    if len(raw) != HID_BOOT_REPORT_LEN:
        return -1
    return sum(1 for b in raw[2:8] if b != 0)


def extract_hid_usage_hex(raw: bytes) -> List[str]:
    # PEDAGOGY-SOLUTION: RT-HID-STRINGS-03
    if len(raw) != HID_BOOT_REPORT_LEN:
        return []
    return [f"usage:0x{b:02x}" for b in raw[2:8] if b != 0]
