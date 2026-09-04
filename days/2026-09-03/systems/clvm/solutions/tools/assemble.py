#!/usr/bin/env python3
"""Assembler educacional em duas passagens para o formato CLVM."""

from __future__ import annotations

import argparse
import struct
from pathlib import Path


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
    """Calcula FNV-1a 32-bit exatamente como o loader C."""
    hash_value = 0x811C9DC5

    for byte in data:
        hash_value ^= byte
        hash_value = (hash_value * 0x01000193) & 0xFFFFFFFF

    return hash_value


def parse_lines(text: str) -> list[str]:
    """Remove comentários iniciados por # e ignora linhas vazias."""
    lines: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if line:
            lines.append(line)

    return lines


def instruction_size(line: str) -> int:
    """Retorna quantos bytes a instrução ocupará no bytecode."""
    if line.endswith(":"):
        return 0

    opcode_name = line.split()[0].upper()

    if opcode_name == "PUSH":
        return 5  # opcode + i32
    if opcode_name in ("JMP", "JZ"):
        return 3  # opcode + i16 relativo

    return 1


def assemble(text: str) -> bytes:
    """Resolve labels na primeira passagem e emite bytes na segunda."""
    lines = parse_lines(text)
    labels: dict[str, int] = {}
    pc = 0

    # Primeira passagem: descobrir o endereço em bytes de cada label.
    for line in lines:
        if line.endswith(":"):
            label = line[:-1].strip()
            if not label or label in labels:
                raise ValueError(f"label inválido ou duplicado: {label}")
            labels[label] = pc
        else:
            pc += instruction_size(line)

    output = bytearray()
    pc = 0

    # Segunda passagem: emitir bytes agora que todos os labels são conhecidos.
    for line in lines:
        if line.endswith(":"):
            continue

        parts = line.split()
        opcode_name = parts[0].upper()

        if opcode_name == "PUSH":
            if len(parts) != 2:
                raise ValueError("PUSH precisa de um inteiro i32")
            output.append(0x01)
            output += struct.pack("<i", int(parts[1], 0))

        elif opcode_name in OPS:
            if len(parts) != 1:
                raise ValueError(f"{opcode_name} não recebe operando")
            output.append(OPS[opcode_name])

        elif opcode_name in ("JMP", "JZ"):
            if len(parts) != 2 or parts[1] not in labels:
                raise ValueError(f"{opcode_name} precisa de um label conhecido")

            opcode = 0x09 if opcode_name == "JMP" else 0x0A
            next_pc = pc + 3
            displacement = labels[parts[1]] - next_pc

            if not -32768 <= displacement <= 32767:
                raise ValueError("salto excede o alcance de i16")

            output.append(opcode)
            output += struct.pack("<h", displacement)

        else:
            raise ValueError(f"instrução desconhecida: {opcode_name}")

        pc += instruction_size(line)

    return bytes(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()

    source = Path(args.input).read_text(encoding="utf-8")
    code = assemble(source)
    checksum = fnv1a32(code)

    header = b"CLVM" + bytes([1, 0]) + struct.pack(
        "<HII",
        0,
        len(code),
        checksum,
    )

    Path(args.output).write_bytes(header + code)
    print(
        f"wrote {args.output}: code={len(code)} bytes "
        f"checksum=0x{checksum:08X}"
    )


if __name__ == "__main__":
    main()
