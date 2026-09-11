"""PE export table triage — validate MZ/PE and flag suspicious names."""

from __future__ import annotations

SUSPICIOUS = ("VirtualAlloc", "WriteProcessMemory", "CreateRemoteThread")


def validate_mz_pe(data: bytes) -> bool:
    """TODO [RT-PE-EXP-01]: MZ + PE signature via e_lfanew."""
    raise NotImplementedError("RT-PE-EXP-01")


def count_export_names(data: bytes, names: list[str]) -> int:
    """TODO [RT-PE-EXP-02]: return len(names) if PE valid else -1."""
    raise NotImplementedError("RT-PE-EXP-02")


def flag_suspicious_exports(names: list[str]) -> list[str]:
    """TODO [RT-PE-EXP-03]: return suspicious export names present."""
    raise NotImplementedError("RT-PE-EXP-03")
