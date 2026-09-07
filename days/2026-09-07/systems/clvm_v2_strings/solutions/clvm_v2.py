# PEDAGOGY-SOLUTION: CLVM-V2-POOL-01
# PEDAGOGY-SOLUTION: CLVM-V2-PRINTS-01
"""CLVM v2: header version=2 + code + string pool; opcode PRINTS=0x21."""

from __future__ import annotations

import struct
from pathlib import Path

PRINTS = 0x21
HALT = 0x08


def fnv1a32(data: bytes) -> int:
    h = 0x811C9DC5
    for b in data:
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def encode_pool(strings: list[str]) -> bytes:
    out = bytearray(struct.pack("<I", len(strings)))
    for s in strings:
        raw = s.encode("utf-8")
        out += struct.pack("<I", len(raw))
        out += raw
    return bytes(out)


def decode_pool(data: bytes, offset: int) -> tuple[list[str], int]:
    (count,) = struct.unpack_from("<I", data, offset)
    offset += 4
    strings: list[str] = []
    for _ in range(count):
        (n,) = struct.unpack_from("<I", data, offset)
        offset += 4
        raw = data[offset : offset + n]
        offset += n
        strings.append(raw.decode("utf-8"))
    return strings, offset


def build_image(code: bytes, strings: list[str]) -> bytes:
    pool = encode_pool(strings)
    payload = code + pool
    checksum = fnv1a32(payload)
    header = b"CLVM" + bytes([2, 0]) + struct.pack("<HII", 0, len(code), checksum)
    return header + payload


def parse_image(data: bytes) -> tuple[bytes, list[str]]:
    if data[0:4] != b"CLVM" or data[4] != 2:
        raise ValueError("not CLVM v2")
    code_size = struct.unpack_from("<I", data, 8)[0]
    checksum = struct.unpack_from("<I", data, 12)[0]
    body = data[16:]
    if fnv1a32(body) != checksum:
        raise ValueError("checksum mismatch")
    code = body[:code_size]
    strings, _ = decode_pool(body, code_size)
    return code, strings


def assemble_hello() -> bytes:
    # PRINTS 0; HALT
    code = bytes([PRINTS]) + struct.pack("<H", 0) + bytes([HALT])
    return build_image(code, ["hi"])


def run_v2(data: bytes) -> str:
    code, strings = parse_image(data)
    out: list[str] = []
    pc = 0
    while pc < len(code):
        op = code[pc]
        pc += 1
        if op == PRINTS:
            (idx,) = struct.unpack_from("<H", code, pc)
            pc += 2
            if idx >= len(strings):
                raise ValueError("string index OOB")
            out.append(strings[idx])
        elif op == HALT:
            break
        else:
            raise ValueError(f"unsupported op 0x{op:02x} in mini-v2 runner")
    return "\n".join(out) + ("\n" if out else "")


if __name__ == "__main__":
    img = assemble_hello()
    Path("hello_v2.clvm").write_bytes(img)
    print(run_v2(img), end="")
