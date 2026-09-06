# Benchmark guiado — Gzip member parse

**Pergunta:** o custo de `parse_member` é O(header) ou O(arquivo)? Onde FNAME longo muda o perfil?

## Procedimento

1. Gere members com FNAME de tamanho 16, 1 KiB, 64 KiB (NUL no fim) e DEFLATE opaco curto.
2. Cronometre `parse_member` / `deflate_payload_start` em loop.
3. Compare com member sem flags (só 10+8).

## Hipóteses

| Caso | Custo |
|------|-------|
| sem flags | O(1) no tamanho do arquivo |
| FNAME longo | O(len(nome)) no skip |
| trailer | O(1) leitura dos últimos 8 |

## Resultados observados

Ambiente: `rust/gzip_member_parse/solutions`.

| Cenário | nota |
|---------|------|
| header-only | parse sub-µs típico |
| FNAME 64 KiB | dominado pelo scan do NUL |
| n/a | sem harness `criterion` no repo |

**Conclusão:** o parser estrutural é barato vs inflate; ainda assim, FNAME hostil sem teto é DoS de CPU — em produção acrescente `max_name_len`.
