"""Magic bytes format detector — tooling capstone."""
from __future__ import annotations

SIGNATURES = [
    (b"\x89PNG\r\n\x1a\n", "PNG"),
    (b"\x1f\x8b", "GZIP"),
    (b"PK\x03\x04", "ZIP"),
]


def match_signature(data: bytes) -> str | None:
    # PEDAGOGY-SOLUTION: CAP-TOOL-DET-01
    for sig, name in SIGNATURES:
        if data.startswith(sig):
            return name
    return None


def confidence(data: bytes, fmt: str) -> float:
    # PEDAGOGY-SOLUTION: CAP-TOOL-DET-02
    for sig, name in SIGNATURES:
        if name == fmt:
            return 1.0 if data.startswith(sig) else 0.0
    return 0.0


def detect_format(data: bytes) -> dict:
    # PEDAGOGY-SOLUTION: CAP-TOOL-DET-03
    fmt = match_signature(data)
    if fmt is None:
        return {"format": None, "confidence": 0.0}
    return {"format": fmt, "confidence": confidence(data, fmt)}
