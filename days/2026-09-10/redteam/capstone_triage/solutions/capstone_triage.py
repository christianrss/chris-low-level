"""Combined format triage: ELF + PE + WASM magic."""
from __future__ import annotations

MAGICS = {
    "ELF": b"\x7fELF",
    "PE": b"MZ",
    "WASM": b"\x00asm",
}


def detect_magic(data: bytes) -> str | None:
    # PEDAGOGY-SOLUTION: CAP-RT-FMT-01
    for name, magic in MAGICS.items():
        if data.startswith(magic):
            return name
    return None


def min_size_for(fmt: str) -> int:
    # PEDAGOGY-SOLUTION: CAP-RT-FMT-02
    return {"ELF": 4, "PE": 2, "WASM": 4}.get(fmt, 0)


def triage_report(data: bytes) -> dict:
    # PEDAGOGY-SOLUTION: CAP-RT-FMT-03
    fmt = detect_magic(data)
    if fmt is None:
        return {"format": None, "ok": False, "reason": "unknown magic"}
    need = min_size_for(fmt)
    if len(data) < need:
        return {"format": fmt, "ok": False, "reason": "truncated"}
    return {"format": fmt, "ok": True, "reason": "ok"}
