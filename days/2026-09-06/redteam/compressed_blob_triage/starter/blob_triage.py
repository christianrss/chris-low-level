"""Compressed blob triage — magic bytes, limites e strings."""

from __future__ import annotations

import re
import struct
import zlib
from typing import Literal

CompressionKind = Literal["gzip", "zlib", "unknown"]


def detect_compression_magic(data: bytes) -> CompressionKind:
    """Detecta gzip (1F 8B) ou zlib (78 9C / 78 DA).

    TODO [RT-COMP-01]
    """
    raise NotImplementedError("RT-COMP-01")


def validate_size_limits(
    data: bytes,
    max_compressed: int,
    max_uncompressed: int,
) -> bool:
    """Retorna True se tamanhos estão dentro dos limites seguros.

    TODO [RT-COMP-02]
    """
    raise NotImplementedError("RT-COMP-02")


def extract_ascii_strings(data: bytes, min_len: int = 4) -> list[str]:
    """Extrai strings ASCII imprimíveis do payload.

    TODO [RT-COMP-03]
    """
    raise NotImplementedError("RT-COMP-03")


def safe_inflate_preview(data: bytes, max_out: int = 65536) -> bytes:
    kind = detect_compression_magic(data)
    if kind == "gzip":
        import gzip

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
