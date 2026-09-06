#!/usr/bin/env python3
"""Gera normal map a partir de heightmap PNG (uso opcional pós-dia 1)."""

from __future__ import annotations

import math
import struct
import sys
import zlib
from pathlib import Path


def load_png_grayscale(path: Path) -> tuple[list[list[float]], int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")

    offset = 8
    width = height = 0
    raw = b""

    while offset < len(data):
        length = int.from_bytes(data[offset : offset + 4], "big")
        chunk_type = data[offset + 4 : offset + 8]
        chunk = data[offset + 8 : offset + 8 + length]
        offset += 12 + length

        if chunk_type == b"IHDR":
            width = int.from_bytes(chunk[0:4], "big")
            height = int.from_bytes(chunk[4:8], "big")
        elif chunk_type == b"IDAT":
            raw += chunk

    decompressed = zlib.decompress(raw)
    pixels: list[list[float]] = []
    stride = width * 3 + 1
    for y in range(height):
        row_start = y * stride + 1
        row = []
        for x in range(width):
            r = decompressed[row_start + x * 3] / 255.0
            row.append(r)
        pixels.append(row)
    return pixels, width, height


def save_normal_png(path: Path, normals: list[list[tuple[int, int, int]]]) -> None:
    h = len(normals)
    w = len(normals[0])
    raw = bytearray()
    for row in normals:
        raw.append(0)
        for rgb in row:
            raw.extend(rgb)

    def chunk(tag: bytes, payload: bytes) -> bytes:
        return struct.pack(">I", len(payload)) + tag + payload + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b"")
    path.write_bytes(png)


def normals_from_height(height: list[list[float]], strength: float = 2.5) -> list[list[tuple[int, int, int]]]:
    h = len(height)
    w = len(height[0])
    out: list[list[tuple[int, int, int]]] = []
    for y in range(h):
        row: list[tuple[int, int, int]] = []
        for x in range(w):
            left = height[y][(x - 1) % w]
            right = height[y][(x + 1) % w]
            up = height[(y - 1) % h][x]
            down = height[(y + 1) % h][x]
            dx = (left - right) * strength
            dy = (up - down) * strength
            dz = 1.0
            length = math.sqrt(dx * dx + dy * dy + dz * dz)
            row.append(
                (
                    int(((dx / length) * 0.5 + 0.5) * 255),
                    int(((dy / length) * 0.5 + 0.5) * 255),
                    int(((dz / length) * 0.5 + 0.5) * 255),
                )
            )
        out.append(row)
    return out


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: gen_normal_from_height.py input_albedo.png output_nrm.png")
        sys.exit(1)

    height, _, _ = load_png_grayscale(Path(sys.argv[1]))
    save_normal_png(Path(sys.argv[2]), normals_from_height(height))
    print(f"Wrote {sys.argv[2]}")


if __name__ == "__main__":
    main()
