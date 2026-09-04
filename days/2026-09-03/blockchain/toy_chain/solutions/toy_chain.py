# PEDAGOGY-SOLUTION: CHAIN-MERKLE-01
# PEDAGOGY-SOLUTION: CHAIN-DIGEST-01
# PEDAGOGY-SOLUTION: CHAIN-MINE-01
# PEDAGOGY-SOLUTION: CHAIN-VALID-01

from __future__ import annotations
from dataclasses import dataclass, asdict
import hashlib, json


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def merkle_root(items: list[str]) -> str:
    if not items:
        return sha256(b"")
    level = [sha256(x.encode()) for x in items]
    while len(level) > 1:
        if len(level) % 2: level.append(level[-1])
        level = [sha256((level[i] + level[i+1]).encode()) for i in range(0, len(level), 2)]
    return level[0]

@dataclass
class Block:
    index: int
    previous_hash: str
    transactions: list[str]
    timestamp: int
    nonce: int = 0

    def digest(self) -> str:
        payload = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "merkle_root": merkle_root(self.transactions),
        }
        return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())

    def mine(self, difficulty: int) -> str:
        prefix = "0" * difficulty
        while True:
            digest = self.digest()
            if digest.startswith(prefix): return digest
            self.nonce += 1

class ToyChain:
    def __init__(self, difficulty: int = 2):
        self.difficulty = difficulty
        genesis = Block(0, "0" * 64, ["genesis"], 0)
        genesis.mine(difficulty)
        self.blocks = [genesis]

    def append(self, transactions: list[str], timestamp: int) -> Block:
        block = Block(len(self.blocks), self.blocks[-1].digest(), list(transactions), timestamp)
        block.mine(self.difficulty)
        self.blocks.append(block)
        return block

    def valid(self) -> bool:
        prefix = "0" * self.difficulty
        for i, block in enumerate(self.blocks):
            if not block.digest().startswith(prefix): return False
            if i == 0:
                if block.previous_hash != "0" * 64: return False
            elif block.previous_hash != self.blocks[i-1].digest():
                return False
        return True
