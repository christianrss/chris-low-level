# PEDAGOGY-SOLUTION: RT-ELF-HDR-01
# PEDAGOGY-SOLUTION: RT-ELF-ENTRY-02
"""Inspector mínimo de cabeçalho ELF64."""

import struct
from typing import Any

ELF64_OFFSETS: dict[str, int] = {
    "e_ident": 0,
    "e_type": 16,
    "e_machine": 18,
    "e_version": 20,
    "e_entry": 24,
    "e_phoff": 32,
    "e_shoff": 40,
    "e_flags": 48,
    "e_ehsize": 52,
    "e_phentsize": 54,
    "e_phnum": 56,
    "e_shentsize": 58,
    "e_shnum": 60,
    "e_shstrndx": 62,
}


def parse_ident(data: bytes) -> dict[str, Any]:
    if len(data) < 16:
        raise ValueError("truncated ident")
    if data[:4] != b"\x7fELF":
        raise ValueError("bad magic")
    if data[4] != 2:
        raise ValueError("not ELF64")
    if data[5] != 1:
        raise ValueError("not little-endian")
    return {"class": 64, "little_endian": True}


def parse_elf64(data: bytes) -> dict[str, Any]:
    if len(data) < 64:
        raise ValueError("truncated ELF64 header")
    parse_ident(data)
    e_type, e_machine, e_version, e_entry = struct.unpack_from(
        "<HHIQ", data, ELF64_OFFSETS["e_type"]
    )
    return {
        "e_type": e_type,
        "e_machine": e_machine,
        "e_version": e_version,
        "e_entry": e_entry,
    }
