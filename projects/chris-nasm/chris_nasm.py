from __future__ import annotations
import re
import struct

REG_MOV_OPCODE = {
    "rax": 0,
    "rcx": 1,
    "rdx": 2,
    "rbx": 3,
    "rsp": 4,
    "rbp": 5,
    "rsi": 6,
    "rdi": 7,
}


def parse_int(text: str) -> int:
    return int(text.strip(), 0)


def assemble_line(line: str) -> bytes:
    line = line.split(';', 1)[0].strip().lower()
    if not line:
        return b""
    if line == "nop":
        return b"\x90"
    if line == "ret":
        return b"\xc3"
    if line == "int3":
        return b"\xcc"
    if line == "syscall":
        return b"\x0f\x05"
    if line.startswith("db "):
        values = [parse_int(x) for x in line[3:].split(',')]
        if any(v < 0 or v > 255 for v in values):
            raise ValueError("db values must fit in one byte")
        return bytes(values)

    match = re.fullmatch(r"mov\s+([a-z0-9]+)\s*,\s*(.+)", line)
    if match:
        reg, imm_text = match.groups()
        if reg not in REG_MOV_OPCODE:
            raise ValueError(f"unsupported register: {reg}")
        imm = parse_int(imm_text)
        if imm < 0 or imm > 0xFFFFFFFFFFFFFFFF:
            raise ValueError("immediate does not fit in 64 bits")
        opcode = 0xB8 + REG_MOV_OPCODE[reg]
        return bytes([0x48, opcode]) + struct.pack("<Q", imm)

    raise ValueError(f"unsupported instruction: {line}")


def assemble(source: str) -> bytes:
    output = bytearray()
    for number, line in enumerate(source.splitlines(), start=1):
        try:
            output.extend(assemble_line(line))
        except ValueError as exc:
            raise ValueError(f"line {number}: {exc}") from exc
    return bytes(output)


if __name__ == "__main__":
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()
    data = assemble(Path(args.source).read_text(encoding="utf-8"))
    Path(args.output).write_bytes(data)
