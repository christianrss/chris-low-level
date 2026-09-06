# Exercícios — Blocked merge sort

## Fácil

- Trace manual de `merge_runs` para `src=[5,6,7,8 | 1,2,3,4]` mostrando `left`, `right`, `out` e cada `++comparisons`.
- Explique por que `n <= 1` retorna sem tocar em `block_reads` / `block_writes`.

## Médio

- **D2-BLOCK-SORT-TILE:** ordene um tile in-place (insertion sort) contando `comparisons`.
- **D2-BLOCK-MERGE-RUN:** mescle dois runs ordenados de `src` para `dst` com estabilidade (`<=`).
- **D2-BLOCK-IO-STATS:** some `block_reads` / `block_writes` em unidades `ceil(len / tile_size)`.

## Difícil

- **D2-BLOCK-PASSES:** orquestre sort de todos os tiles e merges de pares adjacentes até um único run, alternando buffers.

## Desafio

- Escreva H1/H2 sobre `tile_size` antes do benchmark; registre `cmp`, `bread`, `bwrite` e tempo para n=65536 em tiles 64/256/1024/4096.
- Descreva (sem implementar) como um k-way merge com min-heap reduziria o número de passes.
