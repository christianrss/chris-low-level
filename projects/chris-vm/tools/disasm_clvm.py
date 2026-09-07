#!/usr/bin/env python3
"""Disassemble a .clvm image to mnemonics."""

from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path

OPS = {
    0x01: ("PUSH", 4),
    0x02: ("ADD", 0),
    0x03: ("SUB", 0),
    0x04: ("MUL", 0),
    0x05: ("DIV", 0),
    0x06: ("DUP", 0),
    0x07: ("PRINT", 0),
    0x08: ("HALT", 0),
    0x09: ("JMP", 2),
    0x0A: ("JZ", 2),
    0x0B: ("CALL", 2),
    0x0C: ("RET", 0),
    0x0D: ("LOAD", 0),
    0x0E: ("STORE", 0),
    0x0F: ("DROP", 0),
    0x10: ("SWAP", 0),
    0x11: ("EQ", 0),
    0x12: ("LT", 0),
    0x13: ("JNZ", 2),
}


def disassemble(code: bytes) -> list[str]:
    lines: list[str] = []
    pc = 0
    while pc < len(code):
        op = code[pc]
        info = OPS.get(op)
        if info is None:
            raise ValueError(f"unknown opcode 0x{op:02x} at pc={pc}")
        name, extra = info
        pc += 1
        if name == "PUSH":
            if pc + 4 > len(code):
                raise ValueError("truncated PUSH")
            (val,) = struct.unpack_from("<i", code, pc)
            lines.append(f"{pc - 1:04x}: PUSH {val}")
            pc += 4
        elif extra == 2:
            if pc + 2 > len(code):
                raise ValueError(f"truncated {name}")
            (rel,) = struct.unpack_from("<h", code, pc)
            target = pc + 2 + rel
            lines.append(f"{pc - 1:04x}: {name} {rel:+d}  -> {target:04x}")
            pc += 2
        else:
            lines.append(f"{pc - 1:04x}: {name}")
    return lines


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    args = ap.parse_args()
    data = args.input.read_bytes()
    if len(data) < 16 or data[0:4] != b"CLVM":
        print("not a CLVM file", file=sys.stderr)
        return 1
    code_size = struct.unpack_from("<I", data, 8)[0]
    code = data[16 : 16 + code_size]
    for line in disassemble(code):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
