from __future__ import annotations
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
    # TODO [D2-ELF-HEADER]: valide 64 bytes, magic, class, endian e version; depois leia campos com struct.unpack_from.
    raise NotImplementedError("complete parse_elf64_header")
