from __future__ import annotations

import struct
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from elf64 import parse_elf64_header


def fixture() -> bytes:
    data = bytearray(64)
    data[:4] = b"\x7fELF"
    data[4:7] = bytes((2, 1, 1))
    struct.pack_into("<H", data, 18, 62)
    struct.pack_into("<Q", data, 24, 0x401000)
    struct.pack_into("<H", data, 56, 3)
    struct.pack_into("<H", data, 60, 12)
    struct.pack_into("<H", data, 62, 11)
    return bytes(data)


def main() -> None:
    data = fixture()
    iterations = 300000
    start = time.perf_counter()
    checksum = 0
    for _ in range(iterations):
        checksum += parse_elf64_header(data).machine
    seconds = time.perf_counter() - start
    print(f"iterations={iterations} seconds={seconds:.6f} headers_per_s={iterations / seconds:.0f} checksum={checksum}")


if __name__ == "__main__":
    main()
