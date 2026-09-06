from __future__ import annotations

import struct
from dataclasses import dataclass
from collections.abc import Sequence

ELF64_PHDR_SIZE = 56
ELF64_SHDR_SIZE = 64
ELF64_SYM_SIZE = 24

SHT_DYNSYM = 11
SHT_STRTAB = 3


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


def _read_c_string(data: bytes, start: int, end_limit: int) -> str:
    if start < 0 or start >= end_limit:
        return ""
    nul = data.find(b"\x00", start, end_limit)
    if nul < 0:
        nul = end_limit
    return data[start:nul].decode("ascii", errors="replace")


# PEDAGOGY-SOLUTION: D2-ELF-HEADER
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


# PEDAGOGY-SOLUTION: D2-ELF-PHDR
def parse_program_headers(data: bytes, header: Elf64Header) -> list[Elf64Phdr]:
    phoff = header.program_header_offset
    phnum = header.program_header_count
    end = phoff + phnum * ELF64_PHDR_SIZE
    if phoff < 0 or end > len(data):
        raise ValueError("program header table is truncated")

    result: list[Elf64Phdr] = []
    for index in range(phnum):
        base = phoff + index * ELF64_PHDR_SIZE
        p_type = struct.unpack_from("<I", data, base + 0)[0]
        p_offset = struct.unpack_from("<Q", data, base + 8)[0]
        p_vaddr = struct.unpack_from("<Q", data, base + 16)[0]
        p_filesz = struct.unpack_from("<Q", data, base + 32)[0]
        p_memsz = struct.unpack_from("<Q", data, base + 40)[0]
        result.append(Elf64Phdr(p_type, p_offset, p_vaddr, p_filesz, p_memsz))
    return result


# PEDAGOGY-SOLUTION: D2-ELF-SHDR
def parse_section_headers(data: bytes, header: Elf64Header) -> list[Elf64Shdr]:
    shoff = header.section_header_offset
    shnum = header.section_header_count
    end = shoff + shnum * ELF64_SHDR_SIZE
    if shoff < 0 or end > len(data):
        raise ValueError("section header table is truncated")

    raw: list[tuple[int, int, int, int]] = []
    for index in range(shnum):
        base = shoff + index * ELF64_SHDR_SIZE
        name_index = struct.unpack_from("<I", data, base + 0)[0]
        sh_type = struct.unpack_from("<I", data, base + 4)[0]
        sh_offset = struct.unpack_from("<Q", data, base + 24)[0]
        sh_size = struct.unpack_from("<Q", data, base + 32)[0]
        raw.append((name_index, sh_type, sh_offset, sh_size))

    shstrndx = header.section_name_index
    if shstrndx >= shnum:
        raise ValueError("e_shstrndx out of range")
    str_off, str_size = raw[shstrndx][2], raw[shstrndx][3]
    str_end = str_off + str_size
    if str_off < 0 or str_end > len(data):
        raise ValueError("section string table is truncated")

    sections: list[Elf64Shdr] = []
    for name_index, sh_type, sh_offset, sh_size in raw:
        name = _read_c_string(data, str_off + name_index, str_end) if name_index else ""
        sections.append(Elf64Shdr(name_index, sh_type, sh_offset, sh_size, name))
    return sections


def _find_section(sections: Sequence[Elf64Shdr], name: str, sh_type: int | None = None) -> Elf64Shdr | None:
    for section in sections:
        if section.name == name and (sh_type is None or section.type == sh_type):
            return section
    if sh_type is not None:
        for section in sections:
            if section.type == sh_type and section.name in ("", name):
                return section
    return None


# PEDAGOGY-SOLUTION: D2-ELF-DYNSYM
def list_dynamic_symbols(data: bytes, sections: Sequence[Elf64Shdr]) -> list[Elf64DynSym]:
    dynsym = _find_section(sections, ".dynsym", SHT_DYNSYM)
    dynstr = _find_section(sections, ".dynstr", SHT_STRTAB)
    if dynsym is None or dynstr is None:
        return []

    sym_end = dynsym.offset + dynsym.size
    str_end = dynstr.offset + dynstr.size
    if dynsym.offset < 0 or sym_end > len(data) or dynstr.offset < 0 or str_end > len(data):
        raise ValueError("dynamic symbol tables are truncated")
    if dynsym.size % ELF64_SYM_SIZE != 0:
        raise ValueError("dynsym size is not a multiple of Elf64_Sym")

    symbols: list[Elf64DynSym] = []
    for base in range(dynsym.offset, sym_end, ELF64_SYM_SIZE):
        st_name = struct.unpack_from("<I", data, base + 0)[0]
        st_value = struct.unpack_from("<Q", data, base + 8)[0]
        name = _read_c_string(data, dynstr.offset + st_name, str_end) if st_name else ""
        if not name:
            continue
        symbols.append(Elf64DynSym(name, st_value))
    return symbols
