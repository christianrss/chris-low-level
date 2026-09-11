"""CLVM pipeline: disasm → peephole → verify."""
from __future__ import annotations

PUSH, ADD, HALT = 0x01, 0x02, 0x08


def disasm(code: bytes) -> list[str]:
    # PEDAGOGY-SOLUTION: CAP-CLVM-DIS-01
    out: list[str] = []
    i = 0
    while i < len(code):
        op = code[i]
        if op == PUSH:
            out.append(f"PUSH {code[i+1]}")
            i += 2
        elif op == ADD:
            out.append("ADD")
            i += 1
        elif op == HALT:
            out.append("HALT")
            i += 1
        else:
            return []
    return out


def peephole(code: bytes) -> bytes:
    # PEDAGOGY-SOLUTION: CAP-CLVM-PEEP-02
    out = bytearray()
    i = 0
    while i < len(code):
        if i + 3 <= len(code) and code[i] == PUSH and code[i+1] == 0 and code[i+2] == ADD:
            i += 3
            continue
        out.append(code[i])
        i += 1
    return bytes(out)


def verify_stack(code: bytes) -> bool:
    # PEDAGOGY-SOLUTION: CAP-CLVM-VFY-03
    depth = 0
    i = 0
    while i < len(code):
        op = code[i]
        if op == PUSH:
            if i + 1 >= len(code):
                return False
            depth += 1
            i += 2
        elif op == ADD:
            if depth < 2:
                return False
            depth -= 1
            i += 1
        elif op == HALT:
            return depth >= 0
        else:
            return False
    return False
