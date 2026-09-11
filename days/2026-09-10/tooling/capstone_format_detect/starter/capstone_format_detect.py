"""Magic bytes format detector — tooling capstone."""
from __future__ import annotations

SIGNATURES = [
    (b"\x89PNG\r\n\x1a\n", "PNG"),
    (b"\x1f\x8b", "GZIP"),
    (b"PK\x03\x04", "ZIP"),
]


def match_signature(data: bytes) -> str | None:
    """TODO [CAP-TOOL-DET-01]: first matching signature name."""
    raise NotImplementedError("CAP-TOOL-DET-01")


def confidence(data: bytes, fmt: str) -> float:
    """TODO [CAP-TOOL-DET-02]: 1.0 if prefix matches else 0.0."""
    raise NotImplementedError("CAP-TOOL-DET-02")


def detect_format(data: bytes) -> dict:
    """TODO [CAP-TOOL-DET-03]: {format, confidence}."""
    raise NotImplementedError("CAP-TOOL-DET-03")
