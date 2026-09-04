from __future__ import annotations

from pathlib import Path
import sys


def extract_ascii_strings(data: bytes, minimum: int = 5) -> list[tuple[int, str]]:
    """Return (offset, text) for printable ASCII runs."""

    results: list[tuple[int, str]] = []

    # TODO: walk byte-by-byte, remember the start of a printable run,
    # close the run when a non-printable byte is found and keep only runs
    # whose length is at least `minimum`.
    _ = (data, minimum)
    return results


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: ascii_strings.py <binary>")

    for offset, text in extract_ascii_strings(Path(sys.argv[1]).read_bytes()):
        print(f"0x{offset:08X}  {text}")
