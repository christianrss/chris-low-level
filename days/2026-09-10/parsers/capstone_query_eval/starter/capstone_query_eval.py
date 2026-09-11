"""Pratt query evaluator — capstone."""
from __future__ import annotations

BP_AND, BP_OR = 20, 10


def lex(s: str) -> list[str]:
    """TODO [CAP-PRATT-01]: split on spaces into tokens."""
    raise NotImplementedError("CAP-PRATT-01")


def parse_expr(tokens: list[str], pos: int, min_bp: int) -> tuple[bool, int]:
    """TODO [CAP-PRATT-02]: Pratt parse boolean field:value AND/OR."""
    raise NotImplementedError("CAP-PRATT-02")


def eval_query(s: str) -> bool:
    """TODO [CAP-PRATT-03]: evaluate query like 'a:1 AND b:2'."""
    raise NotImplementedError("CAP-PRATT-03")
