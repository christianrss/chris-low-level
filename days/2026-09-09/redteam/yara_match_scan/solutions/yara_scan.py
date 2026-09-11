"""YARA-style hex pattern scanner."""

from __future__ import annotations


def parse_hex_pattern(pat: str) -> list[int | None]:
    # PEDAGOGY-SOLUTION: RT-YARA-PARSE-01
    body = pat.strip("{} ").replace(" ", "")
    out: list[int | None] = []
    i = 0
    while i < len(body):
        if body[i:i+2] == "??":
            out.append(None); i += 2
        else:
            out.append(int(body[i:i+2], 16)); i += 2
    return out


def match_at(data: bytes, pattern: list[int | None], off: int) -> bool:
    # PEDAGOGY-SOLUTION: RT-YARA-MATCH-02
    if off + len(pattern) > len(data):
        return False
    for i, b in enumerate(pattern):
        if b is not None and data[off + i] != b:
            return False
    return True


def scan_all(data: bytes, pattern: list[int | None]) -> list[int]:
    # PEDAGOGY-SOLUTION: RT-YARA-TRIAGE-03
    return [i for i in range(len(data)) if match_at(data, pattern, i)]
