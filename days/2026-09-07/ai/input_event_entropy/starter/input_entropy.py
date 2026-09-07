"""Input event stream entropy — Shannon + RLE + gzip ratio."""

from __future__ import annotations

import gzip
import math
from collections import Counter


def shannon_entropy_events(data: bytes) -> float:
    """TODO [AI-EVT-ENT-01]: entropy over 24-byte aligned records."""
    raise NotImplementedError("AI-EVT-ENT-01")


def event_rle_encode(codes: list[int]) -> list[tuple[int, int]]:
    """TODO [AI-EVT-RLE-02]: RLE on event.code sequence."""
    raise NotImplementedError("AI-EVT-RLE-02")


def compression_ratio_gzip_events(data: bytes) -> float:
    """TODO [AI-EVT-RATIO-03]: len(gzip(data))/len(data)."""
    raise NotImplementedError("AI-EVT-RATIO-03")
