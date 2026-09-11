"""Combined format triage: ELF + PE + WASM magic."""
from __future__ import annotations

MAGICS = {
    "ELF": b"\x7fELF",
    "PE": b"MZ",
    "WASM": b"\x00asm",
}


def detect_magic(data: bytes) -> str | None:
    """TODO [CAP-RT-FMT-01]: return ELF/PE/WASM or None."""
    raise NotImplementedError("CAP-RT-FMT-01")


def min_size_for(fmt: str) -> int:
    """TODO [CAP-RT-FMT-02]: ELF=4, PE=2, WASM=4."""
    raise NotImplementedError("CAP-RT-FMT-02")


def triage_report(data: bytes) -> dict:
    """TODO [CAP-RT-FMT-03]: {format, ok, reason}."""
    raise NotImplementedError("CAP-RT-FMT-03")
