#!/usr/bin/env python3
"""Gera texturas tileable, normal maps e WAVs CC0 para Lantern Hunt."""

from __future__ import annotations

import math
import struct
import wave
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None  # type: ignore


ROOT = Path(__file__).resolve().parents[1]
TEX_DIR = ROOT / "assets" / "textures"
AUDIO_DIR = ROOT / "assets" / "audio"


def noise(x: int, y: int, seed: int) -> float:
    value = (x * 374761393 + y * 668265263 + seed * 1442695040888963407) & 0xFFFFFFFF
    value = (value ^ (value >> 13)) * 1274126177
    value = (value ^ (value >> 16)) & 0xFFFFFFFF
    return value / 0xFFFFFFFF


def make_tileable_albedo(size: int, seed: int, base: tuple[int, int, int], contrast: float) -> list[list[tuple[int, int, int]]]:
    pixels: list[list[tuple[int, int, int]]] = []
    for y in range(size):
        row: list[tuple[int, int, int]] = []
        for x in range(size):
            n = noise(x, y, seed)
            n2 = noise(x * 2, y * 2, seed + 17)
            shade = contrast * (0.55 * n + 0.45 * n2)
            row.append(
                tuple(max(0, min(255, int(channel * (0.65 + shade)))) for channel in base)
            )
        pixels.append(row)
    return pixels


def height_from_albedo(pixels: list[list[tuple[int, int, int]]]) -> list[list[float]]:
    height: list[list[float]] = []
    for row in pixels:
        height.append([sum(px) / (3.0 * 255.0) for px in row])
    return height


def normal_from_height(height: list[list[float]], strength: float = 2.5) -> list[list[tuple[int, int, int]]]:
    h = len(height)
    w = len(height[0])
    normals: list[list[tuple[int, int, int]]] = []
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
            nx = int(((dx / length) * 0.5 + 0.5) * 255)
            ny = int(((dy / length) * 0.5 + 0.5) * 255)
            nz = int(((dz / length) * 0.5 + 0.5) * 255)
            row.append((nx, ny, nz))
        normals.append(row)
    return normals


def save_png(path: Path, pixels: list[list[tuple[int, int, int]]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if Image is not None:
        img = Image.new("RGB", (len(pixels[0]), len(pixels)))
        img.putdata([px for row in pixels for px in row])
        img.save(path)
        return

    # PNG mínimo sem Pillow: grava PPM e renomeia não serve — escreve PNG raw simples via struct.
    width = len(pixels[0])
    height = len(pixels)
    raw = bytearray()
    for row in pixels:
        raw.append(0)
        for r, g, b in row:
            raw.extend((r, g, b))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    import zlib

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    idat = zlib.compress(bytes(raw), 9)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")
    path.write_bytes(png)


def write_wav(path: Path, samples: list[float], sample_rate: int = 44100) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pcm = bytearray()
    for sample in samples:
        clipped = max(-1.0, min(1.0, sample))
        pcm.extend(struct.pack("<h", int(clipped * 32767)))

    with wave.open(str(path), "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm)


def gen_textures() -> None:
    size = 256
    floor = make_tileable_albedo(size, 11, (48, 44, 38), 0.55)
    wall = make_tileable_albedo(size, 23, (62, 58, 52), 0.75)
    bug = make_tileable_albedo(size, 37, (90, 28, 24), 0.45)

    save_png(TEX_DIR / "floor_albedo.png", floor)
    save_png(TEX_DIR / "wall_albedo.png", wall)
    save_png(TEX_DIR / "bug_albedo.png", bug)

    save_png(TEX_DIR / "floor_nrm.png", normal_from_height(height_from_albedo(floor)))
    save_png(TEX_DIR / "wall_nrm.png", normal_from_height(height_from_albedo(wall)))
    save_png(TEX_DIR / "bug_nrm.png", normal_from_height(height_from_albedo(bug)))

    water = make_tileable_albedo(size, 51, (24, 58, 92), 0.35)
    save_png(TEX_DIR / "water_albedo.png", water)
    save_png(TEX_DIR / "water_nrm.png", normal_from_height(height_from_albedo(water), strength=1.8))


def gen_audio() -> None:
    sample_rate = 44100

    ambient: list[float] = []
    duration = 30.0
    total = int(sample_rate * duration)
    for i in range(total):
        t = i / sample_rate
        rumble = 0.18 * math.sin(2 * math.pi * 42.0 * t)
        rumble += 0.08 * math.sin(2 * math.pi * 67.0 * t + 0.4)
        noise_val = (noise(i % 997, i // 997, 99) - 0.5) * 0.04
        ambient.append(rumble + noise_val)

    footstep: list[float] = []
    foot_len = int(0.2 * sample_rate)
    for i in range(foot_len):
        t = i / sample_rate
        env = math.exp(-t * 28.0)
        footstep.append(env * math.sin(2 * math.pi * 180.0 * t) * 0.55)

    shoot: list[float] = []
    shoot_len = int(0.12 * sample_rate)
    for i in range(shoot_len):
        t = i / sample_rate
        env = math.exp(-t * 40.0)
        shoot.append(env * math.sin(2 * math.pi * 920.0 * t) * 0.35)

    write_wav(AUDIO_DIR / "ambient_dark.wav", ambient, sample_rate)
    write_wav(AUDIO_DIR / "footstep.wav", footstep, sample_rate)
    write_wav(AUDIO_DIR / "shoot_marble.wav", shoot, sample_rate)

    slime: list[float] = []
    slime_len = int(0.35 * sample_rate)
    for i in range(slime_len):
        t = i / sample_rate
        env = math.exp(-t * 12.0)
        slime.append(env * (math.sin(2 * math.pi * 140.0 * t) * 0.4 + (noise(i, 0, 77) - 0.5) * 0.2))
    write_wav(AUDIO_DIR / "slime_hit.wav", slime, sample_rate)


def main() -> None:
    gen_textures()
    gen_audio()
    print(f"Assets generated under {ROOT / 'assets'}")


if __name__ == "__main__":
    main()
