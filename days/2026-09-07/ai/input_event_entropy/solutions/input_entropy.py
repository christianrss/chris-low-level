"""Input event stream entropy — Shannon + RLE + gzip ratio."""

from __future__ import annotations

import gzip
import math
from collections import Counter


def shannon_entropy_events(data: bytes) -> float:
    # PEDAGOGY-SOLUTION: AI-EVT-ENT-01
    if not data:
        return 0.0
    counts = Counter(data)
    n = len(data)
    ent = 0.0
    for c in counts.values():
        p = c / n
        ent -= p * math.log2(p)
    return ent


def event_rle_encode(codes: list[int]) -> list[tuple[int, int]]:
    # PEDAGOGY-SOLUTION: AI-EVT-RLE-02
    if not codes:
        return []
    out: list[tuple[int, int]] = []
    cur, run = codes[0], 1
    for x in codes[1:]:
        if x == cur:
            run += 1
        else:
            out.append((cur, run))
            cur, run = x, 1
    out.append((cur, run))
    return out


def compression_ratio_gzip_events(data: bytes) -> float:
    # PEDAGOGY-SOLUTION: AI-EVT-RATIO-03
    if not data:
        return 1.0
    return len(gzip.compress(data)) / len(data)
