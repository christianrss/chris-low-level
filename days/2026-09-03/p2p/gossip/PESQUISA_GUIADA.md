# Pesquisa guiada — gossip e propagação P2P

## Fontes
- Literatura de epidemic/gossip protocols.
- Kademlia é referência futura para descoberta/DHT, não implementação do exercício atual.

## Termos
`epidemic gossip protocol duplicate suppression`, `TTL flooding graph`, `message id deduplication p2p`.

## Perguntas
1. Por que cada nó precisa lembrar IDs já vistos?
2. O que TTL limita?
3. Como ciclos do grafo causariam retransmissão infinita sem deduplicação?
4. Como medir cobertura e número de entregas?

O laboratório é totalmente in-process; não o confunda com uma rede P2P segura/real.

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha após ler as fontes acima) | | |

## Checkpoint

Antes de implementar o primeiro `TODO [ID]`, você deve conseguir explicar o conceito central **sem olhar a resolução**. Registre no Relatório de resolução se passou neste checkpoint.
