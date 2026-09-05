# Teoria passo a passo — gossip em rede simulada

## 1. O que estamos construindo

Um protocolo de gossip determinístico em memória: peers conectados encaminham mensagens com TTL e suprimem duplicatas por `(peer, message_id)`.

## 2. Por que gossip

Em sistemas distribuídos, multicast confiável é caro. Gossip troca exatidão imediata por propagação eventual com redundância controlada.

## 3. Estrutura interna

```text
GossipNetwork
  neighbors: peer -> set(peers)
  seen:      peer -> set(message_ids)
  deliveries: lista (peer, message_id)
  queue: BFS (sender, dest, message)
```

Fluxo de `broadcast(origin, msg)`:

```text
enfileira (None, origin, msg)
enquanto fila:
  se msg_id já visto em dest: continue
  marcar visto, registrar entrega
  se ttl > 0:
    para cada vizinho != sender:
      enfileira (dest, vizinho, msg com ttl-1)
```

## 4. Exemplo numérico — triângulo A-B-C-A

`broadcast("a", Message("m1", "hello", ttl=8))`:

```text
entregas: a, b, c  (3 peers, 3 deliveries)
```

Sem deduplicação, a mensagem circularia infinitamente.

## 5. Exemplo — linha A-B-C-D, TTL=1

```text
a recebe (ttl=8->7 ao encaminhar...)
com ttl=1 em a: encaminha só para b com ttl=0
b não reencaminha (ttl==0)
reached = {a, b}
```

## 6. Invariantes

- Cada par `(peer, message_id)` entrega no máximo uma vez.
- Encaminhamento nunca volta imediatamente para `sender`.
- TTL decresce a cada hop; zero bloqueia novos forwards.
- `reached` contém peers que receberam a mensagem.

## 7. Complexidade

- Pior caso: O(V + E) por hop efetivo com dedup; sem TTL pode explodir.
- Com TTL=T e grau médio d: entregas limitadas em prática por T e topologia.
- Memória: O(V * M) IDs vistos para M mensagens.

## 8. Bugs comuns

- Esquecer `seen` por peer (usa global e suprime demais ou de menos).
- Não decrementar TTL ao encaminhar.
- Encaminhar de volta para `sender` imediato.
- Ordem não determinística sem `sorted(neighbors)` (testes flaky).
- Contar deliveries duplicadas no benchmark.

## 9. Comparação com produção

| Simulação | Cassandra / Consul / IPFS pubsub |
|-----------|----------------------------------|
| grafo estático | membros dinâmicos |
| TTL fixo | hop limit + fanout |
| sem perda de pacotes | UDP/TCP, retries |
| dedup em memória | caches com expiração |

A supressão de duplicatas e o TTL são padrões reais.

## 10. Passo a passo guiado

1. Modele vizinhos e `seen`.
2. Implemente fila BFS (`P2P-GOSSIP-01`).
3. Teste triângulo (3 entregas).
4. Teste linha TTL=1 (só a e b).
5. Rode benchmark e conte deliveries.

## 11. Como saber se está correto

```text
gossip tests passed
```

Exatamente 3 entregas no ciclo; linha com TTL=1 não alcança `c` e `d`.
## 5. Modelo de rede

```text
  A --- B --- C
  |           |
  +----- D -----+
```

## 6. TTL e supressão

Cada hop decrementa TTL. `seen[peer]` evita reentrega local.

## 7. Invariantes

- Mesmo `message_id` entregue no máximo uma vez por peer.
- Encaminhamento não volta ao `sender` imediato.
- TTL=0 não propaga.

## 8. Complexidade

Fila BFS: O(V+E) por mensagem em grafo esparsO.

## 9. Bugs comuns

- Esquecer dedup antes de enfileirar filhos.
- TTL infinito em ciclo ⇒ loop.
- Contar retransmissões como entregas.

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?
Conectar teoria de baixo nível a decisões de implementação verificáveis — não decorar API.

### Por quê estas invariantes?
Cada `TODO [ID]` protege uma propriedade que quebra silenciosamente em produção se ignorada (overflow, estado inválido, parsing parcial).

### Por quê medir e portar para `projects/`?
Lab isola o aprendizado; `projects/chris-*` consolida engenharia de portfólio com testes e benchmarks reproduzíveis.
