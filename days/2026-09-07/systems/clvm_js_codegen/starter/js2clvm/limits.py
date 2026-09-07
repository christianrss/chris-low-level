"""Hard limits aligned with the chris-vm interpreter."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Limits:
    mem_size: int = 256
    slot_bytes: int = 4
    max_call: int = 256
    max_stack: int = 1024
    max_steps: int = 1_000_000

    @property
    def max_slots(self) -> int:
        return self.mem_size // self.slot_bytes


DEFAULT_LIMITS = Limits()
