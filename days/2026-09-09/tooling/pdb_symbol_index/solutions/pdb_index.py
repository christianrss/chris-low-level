"""PDB symbol index basics (text fixture format)."""

from __future__ import annotations


def parse_symbol_line(line: str) -> tuple[int, str]:
    # PEDAGOGY-SOLUTION: TL-PDB-PARSE-01
    addr_s, name = line.strip().split(None, 1)
    return int(addr_s, 16), name


def build_index(lines: list[str]) -> dict[int, str]:
    # PEDAGOGY-SOLUTION: TL-PDB-INDEX-02
    idx: dict[int, str] = {}
    for ln in lines:
        if not ln.strip():
            continue
        addr, name = parse_symbol_line(ln)
        idx[addr] = name
    return idx


def lookup_symbol(idx: dict[int, str], addr: int) -> str:
    # PEDAGOGY-SOLUTION: TL-PDB-LOOKUP-03
    return idx.get(addr, f"0x{addr:x}")
