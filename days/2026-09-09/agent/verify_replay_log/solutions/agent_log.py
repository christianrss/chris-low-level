"""Verify + replay log FSM."""

from __future__ import annotations

import hashlib


def append_log(log: list[dict], event: str, payload: dict) -> None:
    # PEDAGOGY-SOLUTION: AG-VERIFY-LOG-01
    log.append({"event": event, "payload": payload})


def replay_fsm(log: list[dict]) -> str:
    # PEDAGOGY-SOLUTION: AG-REPLAY-FSM-02
    state = "IDLE"
    for entry in log:
        ev = entry["event"]
        if ev == "start":
            state = "RUN"
        elif ev == "verify" and entry["payload"].get("ok"):
            state = "DONE"
        elif ev == "verify":
            state = "REVISE"
    return state


def trace_hash(log: list[dict]) -> str:
    # PEDAGOGY-SOLUTION: AG-TRACE-HASH-03
    data = repr(log).encode()
    return hashlib.sha256(data).hexdigest()[:16]
