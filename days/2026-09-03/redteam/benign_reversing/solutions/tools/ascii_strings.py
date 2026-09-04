# PEDAGOGY-SOLUTION: RE-STRINGS-01

# Educational ASCII string extractor for binaries created in this lab.
from __future__ import annotations

import argparse
from pathlib import Path


def extract_ascii_strings(data: bytes, minimum: int = 5) -> list[tuple[int, str]]:
    results: list[tuple[int, str]] = []
    start: int | None = None

    for index, byte in enumerate(data + b"\x00"):
        printable = 0x20 <= byte <= 0x7E

        if printable and start is None:
            start = index
        elif not printable and start is not None:
            if index - start >= minimum:
                text = data[start:index].decode("ascii")
                results.append((start, text))
            start = None

    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("binary", type=Path)
    parser.add_argument("--minimum", type=int, default=5)
    args = parser.parse_args()

    data = args.binary.read_bytes()
    for offset, text in extract_ascii_strings(data, args.minimum):
        print(f"0x{offset:08X}  {text}")


if __name__ == "__main__":
    main()
