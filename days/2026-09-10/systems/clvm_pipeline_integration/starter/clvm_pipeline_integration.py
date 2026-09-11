"""CLVM pipeline: disasm → peephole → verify."""
from __future__ import annotations

PUSH, ADD, HALT = 0x01, 0x02, 0x08


def disasm(code: bytes) -> list[str]:
    """TODO [CAP-CLVM-DIS-01]: decode PUSH imm8, ADD, HALT."""
    raise NotImplementedError("CAP-CLVM-DIS-01")


def peephole(code: bytes) -> bytes:
    """TODO [CAP-CLVM-PEEP-02]: fold PUSH 0; ADD → NOP sequence removal."""
    raise NotImplementedError("CAP-CLVM-PEEP-02")


def verify_stack(code: bytes) -> bool:
    """TODO [CAP-CLVM-VFY-03]: static stack depth check (PUSH +1, ADD -1, HALT ok at 0)."""
    raise NotImplementedError("CAP-CLVM-VFY-03")
