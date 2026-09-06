# Pesquisa guiada — Blocked / external merge sort

## O que buscar
- `external merge sort runs disk pages`
- `blocked sorting cache-aware tile size`
- `k-way merge vs pairwise merge passes`
- `sort-merge join database I/O cost model`

## Referências sugeridas
- CLRS — sorting chapters + external sorting notes (quando disponíveis no seu material).
- Documentação de `ORDER BY` / sort nodes em engines (PostgreSQL EXPLAIN) — só para intuição de I/O, não para copiar código.

## Perguntas
1. Por que criar runs do tamanho da memória disponível antes de mesclar?
2. O que muda entre merge binário em passes e um único k-way merge com heap?
3. Por que `comparisons` sozinho não explica o custo em disco?
4. Quando um quicksort in-memory ainda é a escolha certa?
5. Como `tile_size` no lab se relaciona com page size / buffer pool?

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha após ler as fontes acima) | | |

## Checkpoint

Antes de implementar o primeiro `TODO [ID]`, você deve conseguir explicar no papel o trace `n=8, tile=4` (fase sort + um merge) **sem olhar a resolução**. Registre no Relatório de resolução se passou neste checkpoint.
