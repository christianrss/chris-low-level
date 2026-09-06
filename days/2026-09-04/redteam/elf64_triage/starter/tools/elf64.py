from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Sequence

ELF64_PHDR_SIZE = 56
ELF64_SHDR_SIZE = 64
ELF64_SYM_SIZE = 24


@dataclass(frozen=True)
class Elf64Header:
    machine: int
    entry: int
    program_header_offset: int
    section_header_offset: int
    program_header_count: int
    section_header_count: int
    section_name_index: int


@dataclass(frozen=True)
class Elf64Phdr:
    type: int
    offset: int
    vaddr: int
    filesz: int
    memsz: int


@dataclass(frozen=True)
class Elf64Shdr:
    name_index: int
    type: int
    offset: int
    size: int
    name: str


@dataclass(frozen=True)
class Elf64DynSym:
    name: str
    value: int


def parse_elf64_header(data: bytes) -> Elf64Header:
    # TODO [D2-ELF-HEADER]: valide 64 bytes, magic, class, endian e version; depois leia campos com struct.unpack_from.
    raise NotImplementedError("complete parse_elf64_header")


def parse_program_headers(data: bytes, header: Elf64Header) -> list[Elf64Phdr]:
    # TODO [D2-ELF-PHDR]: leia phnum entradas de 56 bytes em phoff (type@0, offset@8, vaddr@16, filesz@32, memsz@40).
    raise NotImplementedError("complete parse_program_headers")


def parse_section_headers(data: bytes, header: Elf64Header) -> list[Elf64Shdr]:
    # TODO [D2-ELF-SHDR]: leia shnum Shdr de 64 bytes; resolva nomes via tabela em shstrndx (name@0, type@4, offset@24, size@32).
    raise NotImplementedError("complete parse_section_headers")


def list_dynamic_symbols(data: bytes, sections: Sequence[Elf64Shdr]) -> list[Elf64DynSym]:
    # TODO [D2-ELF-DYNSYM]: ache .dynsym/.dynstr; para cada Elf64_Sym (24B) leia nome em dynstr e st_value@8.
    raise NotImplementedError("complete list_dynamic_symbols")
