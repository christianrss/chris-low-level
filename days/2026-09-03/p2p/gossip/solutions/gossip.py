from __future__ import annotations
from collections import deque
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
        if origin not in self.neighbors:
            raise KeyError(origin)
        queue = deque([(None, origin, message)])
        reached: set[str] = set()
        while queue:
            sender, peer, current = queue.popleft()
            if current.message_id in self.seen[peer]:
                continue
            self.seen[peer].add(current.message_id)
            reached.add(peer)
            self.deliveries.append((peer, current.message_id))
            if current.ttl <= 0:
                continue
            forwarded = Message(current.message_id, current.payload, current.ttl - 1)
            for neighbor in sorted(self.neighbors[peer]):
                if neighbor != sender:
                    queue.append((peer, neighbor, forwarded))
        return reached
