from __future__ import annotations

import struct
from dataclasses import dataclass


@dataclass(frozen=True)
class Elf64Header:
    machine: int
    entry: int
    program_header_offset: int
    section_header_offset: int
    program_header_count: int
    section_header_count: int
    section_name_index: int


def parse_elf64_header(data: bytes) -> Elf64Header:
    if len(data) < 64:
        raise ValueError("ELF64 header is truncated")
    if data[:4] != b"\x7fELF":
        raise ValueError("ELF magic mismatch")
    if data[4] != 2:
        raise ValueError("only ELFCLASS64 is supported")
    if data[5] != 1:
        raise ValueError("only little-endian ELF is supported")
    if data[6] != 1:
        raise ValueError("unsupported ELF identification version")

    machine = struct.unpack_from("<H", data, 18)[0]
    entry = struct.unpack_from("<Q", data, 24)[0]
    phoff = struct.unpack_from("<Q", data, 32)[0]
    shoff = struct.unpack_from("<Q", data, 40)[0]
    phnum = struct.unpack_from("<H", data, 56)[0]
    shnum = struct.unpack_from("<H", data, 60)[0]
    shstrndx = struct.unpack_from("<H", data, 62)[0]
    return Elf64Header(machine, entry, phoff, shoff, phnum, shnum, shstrndx)
