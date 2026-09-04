# Resolucao guiada

1. Modele vizinhos como `dict[str,set[str]]`.
2. Cada peer mantem `seen`, um conjunto de message IDs.
3. Use uma fila contendo sender, destino e mensagem.
4. Ao retirar item, ignore se o ID ja foi visto; caso contrario registre entrega.
5. Se TTL > 0, encaminhe para vizinhos exceto o sender.
6. Teste um triangulo: exatamente tres entregas, nunca mais.
7. Teste uma linha A-B-C-D com TTL=1: apenas A e B devem receber.
8. Benchmark com milhares de peers e registre quantidade de deliveries, nao apenas tempo.

## Etapa de código - fila e deduplicação

```python
queue = deque([(None, origin, message)])
reached: set[str] = set()
while queue:
    sender, peer, current = queue.popleft()
    if current.message_id in self.seen[peer]:
        continue
    self.seen[peer].add(current.message_id)
    reached.add(peer)
    self.deliveries.append((peer, current.message_id))
```

## Etapa de encaminhamento

```python
if current.ttl > 0:
    forwarded = Message(current.message_id, current.payload, current.ttl - 1)
    for neighbor in sorted(self.neighbors[peer]):
        if neighbor != sender:
            queue.append((peer, neighbor, forwarded))
```

## Teste de ciclo

Crie A-B-C-A. Uma mensagem com TTL alto deve gerar exatamente 3 entregas, não um loop infinito. Depois crie A-B-C-D com TTL=1 e espere apenas A e B.

A solução final está em `solutions/gossip.py`.

