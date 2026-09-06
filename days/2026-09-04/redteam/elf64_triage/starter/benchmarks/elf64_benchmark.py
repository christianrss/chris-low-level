from __future__ import annotations

import struct
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from elf64 import (
    list_dynamic_symbols,
    parse_elf64_header,
    parse_program_headers,
    parse_section_headers,
)


def fixture() -> bytes:
    size = 0x200 + 4 * 64
    data = bytearray(size)
    data[0:4] = b"\x7fELF"
    data[4:7] = bytes((2, 1, 1))
    struct.pack_into("<H", data, 16, 3)
    struct.pack_into("<H", data, 18, 62)
    struct.pack_into("<I", data, 20, 1)
    struct.pack_into("<Q", data, 24, 0x401000)
    struct.pack_into("<Q", data, 32, 64)
    struct.pack_into("<Q", data, 40, 0x200)
    struct.pack_into("<H", data, 52, 64)
    struct.pack_into("<H", data, 54, 56)
    struct.pack_into("<H", data, 56, 1)
    struct.pack_into("<H", data, 58, 64)
    struct.pack_into("<H", data, 60, 4)
    struct.pack_into("<H", data, 62, 3)

    ph = 64
    struct.pack_into("<I", data, ph + 0, 1)
    struct.pack_into("<I", data, ph + 4, 5)
    struct.pack_into("<Q", data, ph + 8, 0)
    struct.pack_into("<Q", data, ph + 16, 0x400000)
    struct.pack_into("<Q", data, ph + 24, 0x400000)
    struct.pack_into("<Q", data, ph + 32, size)
    struct.pack_into("<Q", data, ph + 40, size)
    struct.pack_into("<Q", data, ph + 48, 0x1000)

    dynstr = b"\0lab_main\0"
    data[0x120 : 0x120 + len(dynstr)] = dynstr
    sym = 0x100
    struct.pack_into("<I", data, sym + 0, 1)
    data[sym + 4] = 0x12
    struct.pack_into("<H", data, sym + 6, 1)
    struct.pack_into("<Q", data, sym + 8, 0x401100)
    struct.pack_into("<Q", data, sym + 16, 0)

    shstrtab = b"\0.dynsym\0.dynstr\0.shstrtab\0"
    data[0x140 : 0x140 + len(shstrtab)] = shstrtab

    def write_shdr(index: int, name_idx: int, sh_type: int, offset: int, sh_size: int, link: int = 0, entsize: int = 0) -> None:
        base = 0x200 + index * 64
        struct.pack_into("<I", data, base + 0, name_idx)
        struct.pack_into("<I", data, base + 4, sh_type)
        struct.pack_into("<Q", data, base + 24, offset)
        struct.pack_into("<Q", data, base + 32, sh_size)
        struct.pack_into("<I", data, base + 40, link)
        struct.pack_into("<Q", data, base + 56, entsize)

    write_shdr(0, 0, 0, 0, 0)
    write_shdr(1, 1, 11, 0x100, 24, link=2, entsize=24)
    write_shdr(2, 9, 3, 0x120, len(dynstr))
    write_shdr(3, 17, 3, 0x140, len(shstrtab))
    return bytes(data)


def main() -> None:
    data = fixture()
    iterations = 80000
    start = time.perf_counter()
    checksum = 0
    for _ in range(iterations):
        header = parse_elf64_header(data)
        phdrs = parse_program_headers(data, header)
        sections = parse_section_headers(data, header)
        symbols = list_dynamic_symbols(data, sections)
        checksum += header.machine + phdrs[0].type + len(sections) + len(symbols)
    seconds = time.perf_counter() - start
    print(
        f"iterations={iterations} seconds={seconds:.6f} "
        f"triages_per_s={iterations / seconds:.0f} checksum={checksum}"
    )


if __name__ == "__main__":
    main()
