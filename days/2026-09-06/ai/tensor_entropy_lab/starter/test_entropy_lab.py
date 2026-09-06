// Test cases (TESTES_GUIADOS.md):
// Caso 1: `python starter/test_entropy_lab.py` — entropia uniforme e RLE.
// Caso 2: **Shannon:** 4 símbolos equiprováveis → 2.0 bits/byte.
// Caso 3: **RLE:** tensor repetido comprime < 0.1 da forma raw.
// Caso 4: **gzip stub:** payload repetitivo tem ratio < RLE em alguns casos.
// Caso 5: Valide solutions/ com os mesmos testes.
# PEDAGOGY-TEST: AI-ENT-01: Shannon entropy uniforme 2.0 bits
# PEDAGOGY-TEST: AI-ENT-02: tensor RLE em tensor repetitivo
# PEDAGOGY-TEST: AI-ENT-03: compression_ratio_gzip vs RLE
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from entropy_lab import (
    compression_ratio_gzip,
    compression_ratio_rle,
    shannon_entropy,
    tensor_rle_encode,
)


def test_uniform_entropy() -> None:
    data = bytes([0, 1, 2, 3] * 25)
    h = shannon_entropy(data)
    assert abs(h - 2.0) < 1e-6


def test_rle_repeated_tensor() -> None:
    tensor = [7] * 1000 + [3] * 500
    pairs = tensor_rle_encode(tensor)
    assert pairs == [(7, 1000), (3, 500)]
    ratio = compression_ratio_rle(tensor)
    assert ratio < 0.01


def test_gzip_vs_rle() -> None:
    payload = b"LOWLEVEL" * 500
    gz_ratio = compression_ratio_gzip(payload)
    rle_ratio = compression_ratio_rle(list(payload))
    assert gz_ratio < 0.2
    assert gz_ratio < rle_ratio


if __name__ == "__main__":
    test_uniform_entropy()
    test_rle_repeated_tensor()
    test_gzip_vs_rle()
    print("OK tensor entropy lab")
