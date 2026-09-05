"""Inspector mínimo de cabeçalho ELF64."""

import struct
from typing import Any

# Tabela de offsets do ELF64 header (little-endian)
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
    """Valida ident ELF e retorna metadados básicos.

    TODO [RT-ELF-HDR-01]
    """
    raise NotImplementedError("RT-ELF-HDR-01")


def parse_elf64(data: bytes) -> dict[str, Any]:
    """Extrai campos principais do ELF64 header.

    TODO [RT-ELF-ENTRY-02]
    """
    raise NotImplementedError("RT-ELF-ENTRY-02")
