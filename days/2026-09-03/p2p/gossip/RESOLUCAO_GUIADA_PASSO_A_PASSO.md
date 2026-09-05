# Resolucao guiada

## Mapa exato starter → resolução

| TODO ID | Starter | Função/área |
|---------|---------|-------------|
| `P2P-GOSSIP-01` | `starter/gossip.py` | `GossipNetwork.broadcast()` — fila, dedup e TTL |

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-03/p2p/gossip/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

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

### Por que funciona?
Cada peer mantém seu próprio `seen` — a mesma mensagem pode chegar por caminhos diferentes, mas só conta uma entrega por peer. Ignorar ID já visto antes de enfileirar vizinhos evita explosão em grafos com ciclos.

## Etapa de encaminhamento

```python
if current.ttl > 0:
    forwarded = Message(current.message_id, current.payload, current.ttl - 1)
    for neighbor in sorted(self.neighbors[peer]):
        if neighbor != sender:
            queue.append((peer, neighbor, forwarded))
```

### Por que funciona?
TTL limita alcance — cada hop decrementa, então mensagens não viajam para sempre. Excluir o `sender` imediato evita ping-pong A↔B. `sorted(neighbors)` torna o teste determinístico independente da ordem de iteração do dict.

## Teste de ciclo

Crie A-B-C-A. Uma mensagem com TTL alto deve gerar exatamente 3 entregas, não um loop infinito. Depois crie A-B-C-D com TTL=1 e espere apenas A e B.

Agora compare sua implementação com a seção acima e rode os testes antes de consultar `solutions/gossip.py`.

## Etapa de teste determinístico

```bash
python starter/tests/test_gossip.py
```

Triângulo: exatamente 3 entregas da mensagem `m1`. Linha com TTL=1: conjunto `{"a","b"}` apenas.

## Etapa de depuração

| Sintoma | Causa | Correção |
|---------|-------|----------|
| >3 entregas no triângulo | sem dedup por peer | `seen[peer]` antes de enfileirar |
| loop aparentemente infinito | TTL não decrementa | `ttl-1` ao encaminhar |
| teste flaky | ordem de vizinhos | `sorted(neighbors)` |

## Etapa de benchmark

Registre `len(deliveries)` e tempo; ver `BENCHMARK_GUIADO.md`.


## Mapa de consistência auditada

Cada TODO obrigatório do starter está mapeado abaixo. O identificador deve existir no starter, nesta resolução, na solução correspondente e na cobertura de testes/validação do módulo.

- `P2P-GOSSIP-01` — `starter/gossip.py` → `solutions/gossip.py`.

## Relatório de resolução

Checklist ao concluir:

- [ ] `P2P-GOSSIP-01` implementado com fila BFS, dedup e TTL.
- [ ] `python starter/tests/test_gossip.py` passa (triângulo e linha TTL=1).
- [ ] Encaminhamento não volta ao `sender` imediato.
- [ ] Métrica de entregas registrada no benchmark.

**Saída esperada:** `gossip tests passed` (3 entregas no triângulo; TTL=1 na linha).

**Depuração:** imprima `(sender, peer, msg_id, ttl)` a cada dequeue até o triângulo estabilizar em 3 entregas.

**Arquivos starter editados:** `starter/gossip.py`.
## Etapa de benchmark mental

Para N peers em anel, uma mensagem com TTL=N deve visitar todos exatamente uma vez.

## Perguntas de verificação

1. O que acontece se TTL for omitido (default)?
2. Como evitar explosão em grafo completo?
3. Qual estrutura de dados substituiria `deque` em produção?
