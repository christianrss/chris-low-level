#!/usr/bin/env python3
"""Prove that the solution would reject the declared critical mutants."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "solutions" / "src" / "session.cpp"
TESTS = ROOT / "starter" / "tests" / "test_xdbg.py"


def fail(message: str) -> int:
    print(message)
    return 1


def step_body(src: str) -> str:
    idx = src.find("DbgStatus Session::step()")
    if idx < 0:
        return ""
    return src[idx:]


def check_no_bounds(src: str, tests: str) -> int:
    body = step_body(src)
    if "mem_in_bounds" not in src:
        return fail("MUTANT-NO-BOUNDS survived: mem_in_bounds missing")
    if "memory out of bounds" not in src:
        return fail("MUTANT-NO-BOUNDS survived: bounds error string missing")
    load_idx = body.find("case Op::Load")
    store_idx = body.find("case Op::Store")
    if load_idx < 0 or store_idx < 0:
        return fail("MUTANT-NO-BOUNDS survived: LOAD/STORE cases missing")
    load_chunk = body[load_idx : load_idx + 1200]
    store_chunk = body[store_idx : store_idx + 1200]
    if "mem_in_bounds" not in load_chunk or "mem_in_bounds" not in store_chunk:
        return fail("MUTANT-NO-BOUNDS survived: LOAD/STORE skip the bounds predicate")
    if "test_memory_out_of_bounds" not in tests:
        return fail("MUTANT-NO-BOUNDS survived: evidence test missing")
    print("MUTANT-NO-BOUNDS killed")
    return 0


def check_opsize(src: str, tests: str) -> int:
    body = step_body(src)
    push_idx = body.find("case Op::Push")
    if push_idx < 0:
        return fail("MUTANT-OPSIZE survived: PUSH case missing")
    push_chunk = body[push_idx : push_idx + 700]
    if "pc += 4" not in push_chunk:
        return fail("MUTANT-OPSIZE survived: PUSH does not consume 4 operand bytes")
    if "need(4)" not in push_chunk:
        return fail("MUTANT-OPSIZE survived: PUSH does not require 4 remaining bytes")
    if "operand_bytes" not in src or "Op::Push" not in src:
        return fail("MUTANT-OPSIZE survived: decoder has no PUSH width table")
    if "test_disasm_push_at_entry" not in tests:
        return fail("MUTANT-OPSIZE survived: evidence test missing")
    print("MUTANT-OPSIZE killed")
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        return fail("usage: run_mutant_check.py MUTANT-ID")
    mutant = sys.argv[1]
    src = SRC.read_text(encoding="utf-8")
    tests = TESTS.read_text(encoding="utf-8")
    if mutant == "MUTANT-NO-BOUNDS":
        return check_no_bounds(src, tests)
    if mutant == "MUTANT-OPSIZE":
        return check_opsize(src, tests)
    return fail(f"unknown mutant {mutant}")


if __name__ == "__main__":
    raise SystemExit(main())
