# Blocked / external-style merge sort

Você implementa um merge sort **em tiles**: ordena blocos que cabem em cache (ou em uma página de disco simulada), depois mescla runs adjacentes em passes até restar um único run. O custo de I/O é modelado por `SortIoStats`.

## Projeto cumulativo
`projects/chris-algorithms`

## Fluxo sugerido
1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Faça o paper-trace de um vetor pequeno com `tile_size` explícito.
3. Implemente os TODOs em `starter/` antes de consultar `solutions/`.
4. Rode os testes guiados.
5. Execute o benchmark variando `tile_size` e registre `block_reads` / `block_writes`.

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-algorithms` |
| O que levar | `blocked_merge_sort` + `SortIoStats` |
| Testes a replicar | correctness + I/O tile accounting |
| Milestone | MILESTONES.md — blocked merge sort |
| Commit sugerido | `feat(algo): port blocked merge sort from day02 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
