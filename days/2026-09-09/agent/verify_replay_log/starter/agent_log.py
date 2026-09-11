"""Verify + replay log FSM."""

from __future__ import annotations

import hashlib


def append_log(log: list[dict], event: str, payload: dict) -> None:
    """TODO [AG-VERIFY-LOG-01]: append structured entry."""
    raise NotImplementedError("AG-VERIFY-LOG-01")


def replay_fsm(log: list[dict]) -> str:
    """TODO [AG-REPLAY-FSM-02]: replay to final state."""
    raise NotImplementedError("AG-REPLAY-FSM-02")


def trace_hash(log: list[dict]) -> str:
    """TODO [AG-TRACE-HASH-03]: stable short hash."""
    raise NotImplementedError("AG-TRACE-HASH-03")
