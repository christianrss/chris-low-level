# PEDAGOGY-SOLUTION: BOOT-IMAGE-01

from __future__ import annotations


def build_image() -> bytes:
    # Exact x86 16-bit bytes for:
    # mov ah,0x0e; mov al,'H'; int 0x10; hlt; jmp $-1
    code = bytes.fromhex("b4 0e b0 48 cd 10 f4 eb fd")
    image = bytearray(512)
    image[:len(code)] = code
    image[510:512] = b"\x55\xaa"
    return bytes(image)


if __name__ == "__main__":
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", default="bootsector.bin")
    args = parser.parse_args()
    Path(args.output).write_bytes(build_image())
