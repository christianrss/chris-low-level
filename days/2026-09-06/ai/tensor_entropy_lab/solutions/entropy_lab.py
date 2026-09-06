# PEDAGOGY-SOLUTION: AI-ENT-01
# PEDAGOGY-SOLUTION: AI-ENT-02
# PEDAGOGY-SOLUTION: AI-ENT-03
"""Tensor entropy lab — Shannon entropy, RLE e comparação com gzip."""

from __future__ import annotations

import gzip
import math
from collections import Counter


def shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    n = len(data)
    entropy = 0.0
    for count in counts.values():
        p = count / n
        entropy -= p * math.log2(p)
    return entropy


def tensor_rle_encode(tensor: list[int]) -> list[tuple[int, int]]:
    if not tensor:
        return []
    pairs: list[tuple[int, int]] = []
    current = tensor[0]
    run = 1
    for value in tensor[1:]:
        if value == current:
            run += 1
        else:
            pairs.append((current, run))
            current = value
            run = 1
    pairs.append((current, run))
    return pairs


def tensor_rle_size_bytes(tensor: list[int]) -> int:
    pairs = tensor_rle_encode(tensor)
    return len(pairs) * 8


def raw_tensor_size_bytes(tensor: list[int]) -> int:
    return len(tensor) * 4


def compression_ratio_rle(tensor: list[int]) -> float:
    raw = raw_tensor_size_bytes(tensor)
    if raw == 0:
        return 1.0
    return tensor_rle_size_bytes(tensor) / raw


def compression_ratio_gzip(data: bytes) -> float:
    if not data:
        return 1.0
    compressed = gzip.compress(data)
    return len(compressed) / len(data)
