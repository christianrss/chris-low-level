from __future__ import annotations

from pathlib import Path
import sys


def extract_ascii_strings(data: bytes, minimum: int = 5) -> list[tuple[int, str]]:
    """Return (offset, text) for printable ASCII runs."""

    results: list[tuple[int, str]] = []

    # TODO [RE-STRINGS-01]: walk byte-by-byte, remember the start of a printable run,
    # close the run when a non-printable byte is found and keep only runs
    # whose length is at least `minimum`.
    start: int | None = None
    for index, byte in enumerate(data + b"\x00"):
        printable = 0x20 <= byte <= 0x7e
        if printable and start is None:
            start = index
        elif not printable and start is not None:
            if index - start >= minimum:
                text = data[start:index].decode("ascii")
                results.append((start, text))
            start = None
    return results


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: ascii_strings.py <binary>")

    for offset, text in extract_ascii_strings(Path(sys.argv[1]).read_bytes()):
        print(f"0x{offset:08X}  {text}")
