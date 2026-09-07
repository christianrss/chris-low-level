#!/usr/bin/env python3
"""Structural + conservative stack-effect verifier for .clvm images."""

from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path

# stack delta: (pops, pushes) ignoring control transfers' dual paths
STACK_EFFECT = {
    0x01: (0, 1),  # PUSH
    0x02: (2, 1),
    0x03: (2, 1),
    0x04: (2, 1),
    0x05: (2, 1),
    0x06: (1, 2),
    0x07: (1, 0),
    0x08: (0, 0),
    0x09: (0, 0),  # JMP
    0x0A: (1, 0),  # JZ
    0x0B: (0, 0),  # CALL (args already pushed by caller)
    0x0C: (0, 0),  # RET (return value already on stack)
    0x0D: (1, 1),  # LOAD
    0x0E: (2, 0),  # STORE
    0x0F: (1, 0),
    0x10: (2, 2),
    0x11: (2, 1),
    0x12: (2, 1),
    0x13: (1, 0),  # JNZ
}

BRANCH = {0x09, 0x0A, 0x0B, 0x13}


def fnv1a32(data: bytes) -> int:
    h = 0x811C9DC5
    for b in data:
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def verify(data: bytes) -> list[str]:
    errors: list[str] = []
    if len(data) < 16:
        return ["file too small"]
    if data[0:4] != b"CLVM":
        return ["bad magic"]
    if data[4] != 1:
        errors.append("unsupported version")
    if data[5] != 0:
        errors.append("unsupported flags")
    entry = struct.unpack_from("<H", data, 6)[0]
    code_size = struct.unpack_from("<I", data, 8)[0]
    checksum = struct.unpack_from("<I", data, 12)[0]
    if code_size != len(data) - 16:
        errors.append("size mismatch")
        return errors
    code = data[16:]
    if fnv1a32(code) != checksum:
        errors.append("checksum mismatch")
    if code_size != 0 and entry >= code_size:
        errors.append("entry outside code")

    # linear walk + instruction boundaries
    boundaries = {0}
    pc = 0
    while pc < len(code):
        op = code[pc]
        if op not in STACK_EFFECT:
            errors.append(f"unknown opcode 0x{op:02x} at {pc}")
            break
        start = pc
        pc += 1
        if op == 0x01:
            if pc + 4 > len(code):
                errors.append(f"truncated PUSH at {start}")
                break
            pc += 4
        elif op in BRANCH:
            if pc + 2 > len(code):
                errors.append(f"truncated branch at {start}")
                break
            rel = struct.unpack_from("<h", code, pc)[0]
            target = pc + 2 + rel
            pc += 2
            if not (0 <= target <= len(code)):
                errors.append(f"branch target OOB from {start} -> {target}")
            else:
                boundaries.add(target)
        boundaries.add(pc)

    # conservative stack walk from entry along fall-through only
    # (branches recorded but not fully CFG-merged — flag negative depth)
    depth = 0
    pc = entry
    seen: set[int] = set()
    steps = 0
    while pc < len(code) and steps < 100000:
        if pc in seen:
            break
        seen.add(pc)
        steps += 1
        op = code[pc]
        if op not in STACK_EFFECT:
            break
        pops, pushes = STACK_EFFECT[op]
        if depth < pops:
            errors.append(f"stack underflow at pc={pc} op=0x{op:02x} depth={depth}")
            break
        depth = depth - pops + pushes
        if depth > 1024:
            errors.append(f"stack overflow depth={depth} at pc={pc}")
            break
        pc += 1
        if op == 0x01:
            pc += 4
        elif op in BRANCH:
            rel = struct.unpack_from("<h", code, pc)[0]
            next_pc = pc + 2
            target = next_pc + rel
            if op == 0x09:  # JMP — follow
                pc = target
                continue
            if op == 0x0B:  # CALL — follow target; ignore return path in this pass
                pc = target
                continue
            # JZ/JNZ: follow fall-through (conservative)
            pc = next_pc
            continue
        if op == 0x08:  # HALT
            break
        if op == 0x0C:  # RET — stop this path
            break
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    args = ap.parse_args()
    errs = verify(args.input.read_bytes())
    if errs:
        for e in errs:
            print(f"INVALID: {e}", file=sys.stderr)
        return 1
    print(f"VALID: {args.input}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
