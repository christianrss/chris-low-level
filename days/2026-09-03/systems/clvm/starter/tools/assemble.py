#!/usr/bin/env python3
"""Assembler inicial da CLVM.

A versão starter compila/roda até os pontos marcados com TODO. A ideia é
preencher os TODOs seguindo RESOLUCAO_GUIADA_PASSO_A_PASSO.md.
"""

from __future__ import annotations

import argparse
import struct
from pathlib import Path


# Tabela opcode: mnemonic textual -> byte emitido no arquivo CLVM.
OPS = {
    "ADD": 0x02,
    "SUB": 0x03,
    "MUL": 0x04,
    "DIV": 0x05,
    "DUP": 0x06,
    "PRINT": 0x07,
    "HALT": 0x08,
}


def fnv1a32(data: bytes) -> int:
    """TODO [CLVM-PY-FNV-01]: implemente FNV-1a 32-bit."""
    return 0


def parse_lines(text: str) -> list[str]:
    """Remove comentários e linhas vazias do assembly."""
    lines: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if line:
            lines.append(line)

    return lines


def assemble(text: str) -> bytes:
    """Monta PUSH e opcodes simples; labels ficam para o exercício difícil."""
    output = bytearray()

    for line in parse_lines(text):
        parts = line.split()
        opcode_name = parts[0].upper()

        if opcode_name == "PUSH":
            output.append(0x01)
            output += struct.pack("<i", int(parts[1], 0))
        elif opcode_name in OPS:
            output.append(OPS[opcode_name])
        elif line.endswith(":") or opcode_name in ("JMP", "JZ"):
            raise NotImplementedError(
                "TODO [CLVM-ASM-LABELS-01]: implemente labels em duas passagens + JMP/JZ"
            )
        else:
            raise ValueError(f"instrução desconhecida: {opcode_name}")

    return bytes(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()

    source = Path(args.input).read_text(encoding="utf-8")
    code = assemble(source)

    header = (
        b"CLVM"
        + bytes([1, 0])
        + struct.pack("<HII", 0, len(code), fnv1a32(code))
    )

    Path(args.output).write_bytes(header + code)
    print(f"wrote {args.output}: {len(code)} code bytes")


if __name__ == "__main__":
    main()
