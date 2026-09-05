# Exercícios — gossip

## Fácil

- **P2P-MODEL-01:** desenhe o grafo A-B-C-A e preveja quantas entregas ocorrem com TTL alto.
- **P2P-GOSSIP-01:** implemente fila BFS com `seen` por peer.

## Médio

- **P2P-TTL-01:** decremente TTL ao encaminhar; valide linha A-B-C-D com TTL=1.
- **P2P-DEDUP-01:** garanta que o mesmo `message_id` não entrega duas vezes no mesmo peer.

## Difícil

- **P2P-ORDER-01:** use `sorted(neighbors)` para encaminhamento determinístico.
- **P2P-METRIC-01:** registre `len(deliveries)` no benchmark, não só tempo.

## Desafio

- **P2P-FAIL-01:** descreva como simular um peer que cai após receber metade das mensagens.
- **P2P-PROD-01:** compare com epidemic broadcast em um paper ou documentação do Consul.
