"""Pratt query evaluator — capstone."""
from __future__ import annotations

BP_AND, BP_OR = 20, 10


def lex(s: str) -> list[str]:
    # PEDAGOGY-SOLUTION: CAP-PRATT-01
    return s.split()


def parse_expr(tokens: list[str], pos: int, min_bp: int) -> tuple[bool, int]:
    # PEDAGOGY-SOLUTION: CAP-PRATT-02
    if pos >= len(tokens):
        return False, pos
    tok = tokens[pos]
    if ":" in tok:
        left = True
        pos += 1
    elif tok == "true":
        left, pos = True, pos + 1
    elif tok == "false":
        left, pos = False, pos + 1
    else:
        return False, pos
    while pos < len(tokens):
        op = tokens[pos]
        if op == "AND" and BP_AND >= min_bp:
            pos += 1
            right, pos = parse_expr(tokens, pos, BP_AND + 1)
            left = left and right
        elif op == "OR" and BP_OR >= min_bp:
            pos += 1
            right, pos = parse_expr(tokens, pos, BP_OR + 1)
            left = left or right
        else:
            break
    return left, pos


def eval_query(s: str) -> bool:
    # PEDAGOGY-SOLUTION: CAP-PRATT-03
    toks = lex(s)
    val, end = parse_expr(toks, 0, 0)
    return val and end == len(toks)
