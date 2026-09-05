# Arena Allocator e alinhamento

Você vai construir um bump/arena allocator para entender alinhamento, lifetime e custo de alocação. O desafio começa com aritmética de endereços e termina comparando uma arena com alocações individuais de heap.

## Projeto cumulativo
`projects/chris-arena`

## Fluxo sugerido
1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Abra `starter/EXERCISE_TODO.md`.
3. Implemente antes de consultar `solutions/`.
4. Rode os testes guiados.
5. Execute o benchmark e registre ambiente/resultados.

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-arena` |
| O que levar | Arena allocate/reset/align |
| Testes a replicar | arena unit tests |
| Milestone | MILESTONES.md — arena allocator |
| Commit sugerido | `feat(arena): port allocator from day02 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
