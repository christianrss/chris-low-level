"""Byte-level tokenizer for capstone."""
from __future__ import annotations


def bytes_to_ids(data: bytes) -> list[int]:
    """TODO [CAP-AI-TOK-01]: map each byte to int 0..255."""
    raise NotImplementedError("CAP-AI-TOK-01")


def merge_runs(ids: list[int]) -> list[tuple[int, int]]:
    """TODO [CAP-AI-TOK-02]: run-length pairs (id, count)."""
    raise NotImplementedError("CAP-AI-TOK-02")


def vocab_size(ids: list[int]) -> int:
    """TODO [CAP-AI-TOK-03]: count distinct token ids."""
    raise NotImplementedError("CAP-AI-TOK-03")
