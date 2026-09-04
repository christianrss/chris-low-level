from __future__ import annotations

import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from elf64 import parse_elf64_header


def make_fixture() -> bytes:
    data = bytearray(64)
    data[:4] = b"\x7fELF"
    data[4] = 2
    data[5] = 1
    data[6] = 1
    struct.pack_into("<H", data, 16, 2)
    struct.pack_into("<H", data, 18, 62)
    struct.pack_into("<I", data, 20, 1)
    struct.pack_into("<Q", data, 24, 0x401000)
    struct.pack_into("<Q", data, 32, 64)
    struct.pack_into("<Q", data, 40, 4096)
    struct.pack_into("<H", data, 52, 64)
    struct.pack_into("<H", data, 54, 56)
    struct.pack_into("<H", data, 56, 3)
    struct.pack_into("<H", data, 58, 64)
    struct.pack_into("<H", data, 60, 12)
    struct.pack_into("<H", data, 62, 11)
    return bytes(data)


def main() -> int:
    header = parse_elf64_header(make_fixture())
    assert header.machine == 62
    assert header.entry == 0x401000
    assert header.program_header_count == 3
    assert header.section_header_count == 12
    assert header.section_name_index == 11

    for bad in (b"", b"not elf" + bytes(100)):
        try:
            parse_elf64_header(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid input should fail")

    print("ELF64 parser tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
