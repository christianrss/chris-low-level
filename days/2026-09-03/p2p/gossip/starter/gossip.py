from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Message:
    message_id: str
    payload: str
    ttl: int

class GossipNetwork:
    def __init__(self):
        self.neighbors: dict[str, set[str]] = {}
        self.seen: dict[str, set[str]] = {}
        self.deliveries: list[tuple[str, str]] = []

    def add_peer(self, peer: str) -> None:
        self.neighbors.setdefault(peer, set())
        self.seen.setdefault(peer, set())

    def connect(self, a: str, b: str) -> None:
        self.add_peer(a); self.add_peer(b)
        self.neighbors[a].add(b); self.neighbors[b].add(a)

    def broadcast(self, origin: str, message: Message) -> set[str]:
        # TODO: queue propagation + per-peer duplicate suppression + TTL.
        if origin not in self.neighbors: raise KeyError(origin)
        self.seen[origin].add(message.message_id)
        self.deliveries.append((origin, message.message_id))
        return {origin}
