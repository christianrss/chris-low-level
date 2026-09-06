"""Tensor entropy lab — Shannon entropy, RLE e comparação com gzip."""

from __future__ import annotations

import gzip
import math
from collections import Counter
from typing import Iterable


def shannon_entropy(data: bytes) -> float:
    """Retorna entropia de Shannon em bits por byte.

    TODO [AI-ENT-01]
    """
    raise NotImplementedError("AI-ENT-01")


def tensor_rle_encode(tensor: list[int]) -> list[tuple[int, int]]:
    """Codifica tensor 1D como lista de pares (valor, contagem).

    TODO [AI-ENT-02]
    """
    raise NotImplementedError("AI-ENT-02")


def tensor_rle_size_bytes(tensor: list[int]) -> int:
    """Tamanho em bytes se cada par RLE usar int32 + int32."""
    pairs = tensor_rle_encode(tensor)
    return len(pairs) * 8


def raw_tensor_size_bytes(tensor: list[int]) -> int:
    return len(tensor) * 4


def compression_ratio_rle(tensor: list[int]) -> float:
    """Razão compressed/raw (< 1 significa ganho).

    TODO [AI-ENT-02]
    """
    raise NotImplementedError("AI-ENT-02")


def compression_ratio_gzip(data: bytes) -> float:
    """Razão len(gzip(data))/len(data). Stub usa gzip padrão.

    TODO [AI-ENT-03]
    """
    raise NotImplementedError("AI-ENT-03")
