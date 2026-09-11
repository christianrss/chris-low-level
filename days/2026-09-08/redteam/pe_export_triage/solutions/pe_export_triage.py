"""PE export table triage — validate MZ/PE and flag suspicious names."""

from __future__ import annotations

SUSPICIOUS = ("VirtualAlloc", "WriteProcessMemory", "CreateRemoteThread")


def validate_mz_pe(data: bytes) -> bool:
    # PEDAGOGY-SOLUTION: RT-PE-EXP-01
    if len(data) < 0x40 or data[0:2] != b"MZ":
        return False
    import struct
    pe_off = struct.unpack_from("<I", data, 0x3C)[0]
    return pe_off + 4 <= len(data) and data[pe_off:pe_off + 2] == b"PE"


def count_export_names(data: bytes, names: list[str]) -> int:
    # PEDAGOGY-SOLUTION: RT-PE-EXP-02
    if not validate_mz_pe(data):
        return -1
    return len(names)


def flag_suspicious_exports(names: list[str]) -> list[str]:
    # PEDAGOGY-SOLUTION: RT-PE-EXP-03
    return [n for n in names if n in SUSPICIOUS]
