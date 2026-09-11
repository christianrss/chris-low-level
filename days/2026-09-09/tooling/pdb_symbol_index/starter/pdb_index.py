"""PDB symbol index basics (text fixture format)."""

from __future__ import annotations


def parse_symbol_line(line: str) -> tuple[int, str]:
    """TODO [TL-PDB-PARSE-01]: parse '1000 main'."""
    raise NotImplementedError("TL-PDB-PARSE-01")


def build_index(lines: list[str]) -> dict[int, str]:
    """TODO [TL-PDB-INDEX-02]: addr->name index."""
    raise NotImplementedError("TL-PDB-INDEX-02")


def lookup_symbol(idx: dict[int, str], addr: int) -> str:
    """TODO [TL-PDB-LOOKUP-03]: lookup or hex fallback."""
    raise NotImplementedError("TL-PDB-LOOKUP-03")
