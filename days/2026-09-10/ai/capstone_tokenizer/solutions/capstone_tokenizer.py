"""Byte-level tokenizer for capstone."""
from __future__ import annotations


def bytes_to_ids(data: bytes) -> list[int]:
    # PEDAGOGY-SOLUTION: CAP-AI-TOK-01
    return list(data)


def merge_runs(ids: list[int]) -> list[tuple[int, int]]:
    # PEDAGOGY-SOLUTION: CAP-AI-TOK-02
    if not ids:
        return []
    out = []
    cur, run = ids[0], 1
    for x in ids[1:]:
        if x == cur:
            run += 1
        else:
            out.append((cur, run))
            cur, run = x, 1
    out.append((cur, run))
    return out


def vocab_size(ids: list[int]) -> int:
    # PEDAGOGY-SOLUTION: CAP-AI-TOK-03
    return len(set(ids))
