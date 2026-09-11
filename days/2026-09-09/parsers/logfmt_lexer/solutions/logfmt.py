"""logfmt key=value lexer."""

from __future__ import annotations

import shlex


def tokenize(line: str) -> list[str]:
    # PEDAGOGY-SOLUTION: PR-LOGFMT-LEX-01
    return shlex.split(line.strip())


def parse_kv(tok: str) -> tuple[str, str]:
    # PEDAGOGY-SOLUTION: PR-LOGFMT-KV-02
    k, v = tok.split('=', 1)
    return k, v


def parse_line(line: str) -> dict[str, str]:
    # PEDAGOGY-SOLUTION: PR-LOGFMT-ESC-03
    out: dict[str, str] = {}
    for tok in tokenize(line):
        k, v = parse_kv(tok)
        out[k] = v.strip('"')
    return out
