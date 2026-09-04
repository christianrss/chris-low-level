from __future__ import annotations
from dataclasses import dataclass
import hashlib

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def merkle_root(items: list[str]) -> str:
    # TODO [CHAIN-MERKLE-01]: build pairwise Merkle levels.
    return sha256(b"")

@dataclass
class Block:
    index: int
    previous_hash: str
    transactions: list[str]
    timestamp: int
    nonce: int = 0
    def digest(self) -> str:
        # TODO [CHAIN-DIGEST-01]: canonical deterministic serialization.
        return sha256(str(self.index).encode())
    def mine(self, difficulty: int) -> str:
        # TODO [CHAIN-MINE-01]: increment nonce until the digest has the requested zero prefix.
        return self.digest()

class ToyChain:
    def __init__(self, difficulty: int = 2):
        self.difficulty = difficulty
        self.blocks = [Block(0, "0" * 64, ["genesis"], 0)]
    def append(self, transactions: list[str], timestamp: int) -> Block:
        block = Block(len(self.blocks), self.blocks[-1].digest(), list(transactions), timestamp)
        self.blocks.append(block)
        return block
    def valid(self) -> bool:
        # TODO [CHAIN-VALID-01]: validate PoW and previous-hash links.
        return False
