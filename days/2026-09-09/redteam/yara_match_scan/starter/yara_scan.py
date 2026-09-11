"""YARA-style hex pattern scanner."""

from __future__ import annotations


def parse_hex_pattern(pat: str) -> list[int | None]:
    """TODO [RT-YARA-PARSE-01]: parse { AA BB ?? }."""
    raise NotImplementedError("RT-YARA-PARSE-01")


def match_at(data: bytes, pattern: list[int | None], off: int) -> bool:
    """TODO [RT-YARA-MATCH-02]: match at offset."""
    raise NotImplementedError("RT-YARA-MATCH-02")


def scan_all(data: bytes, pattern: list[int | None]) -> list[int]:
    """TODO [RT-YARA-TRIAGE-03]: all match offsets."""
    raise NotImplementedError("RT-YARA-TRIAGE-03")
