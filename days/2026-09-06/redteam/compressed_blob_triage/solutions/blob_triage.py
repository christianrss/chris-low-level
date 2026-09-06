# PEDAGOGY-SOLUTION: RT-COMP-01
# PEDAGOGY-SOLUTION: RT-COMP-02
# PEDAGOGY-SOLUTION: RT-COMP-03
"""Compressed blob triage — magic bytes, limites e strings."""

from __future__ import annotations

import gzip
import re
import zlib
from typing import Literal

CompressionKind = Literal["gzip", "zlib", "unknown"]


def detect_compression_magic(data: bytes) -> CompressionKind:
    if len(data) < 2:
        return "unknown"
    if data[0] == 0x1F and data[1] == 0x8B:
        return "gzip"
    if data[0] == 0x78 and data[1] in (0x01, 0x5E, 0x9C, 0xDA):
        return "zlib"
    return "unknown"


def validate_size_limits(
    data: bytes,
    max_compressed: int,
    max_uncompressed: int,
) -> bool:
    if len(data) > max_compressed:
        return False
    kind = detect_compression_magic(data)
    if kind == "unknown":
        return len(data) <= max_uncompressed
    try:
        preview = safe_inflate_preview(data, max_out=max_uncompressed + 1)
    except Exception:
        return False
    return len(preview) <= max_uncompressed


def extract_ascii_strings(data: bytes, min_len: int = 4) -> list[str]:
    pattern = rb"[\x20-\x7e]{%d,}" % min_len
    return [m.decode("ascii") for m in re.findall(pattern, data)]


def safe_inflate_preview(data: bytes, max_out: int = 65536) -> bytes:
    kind = detect_compression_magic(data)
    if kind == "gzip":
        out = gzip.decompress(data)
        if len(out) > max_out:
            raise ValueError("output too large")
        return out
    if kind == "zlib":
        out = zlib.decompress(data)
        if len(out) > max_out:
            raise ValueError("output too large")
        return out
    raise ValueError("unknown compression")
