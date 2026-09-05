# Exercícios — Pesquisa empírica de sorting

## Fácil

- Trace manual de `merge_range` para `[3,1,2]` mostrando `left`, `right`, `out` a cada passo.
- Explique por que `end - begin <= 1` encerra a recursão do merge sort.

## Médio

- **D2-SORT-MERGE-RANGE:** implemente intercalação com contagem em `SortStats`.
- **D2-SORT-MERGE-RECURSE:** divida recursivamente e chame `merge_range` nos semiintervalos.

## Difícil

- **D2-SORT-PARTITION:** implemente partição Lomuto com último elemento como pivot.
- **D2-SORT-QUICK-LOOP:** limite profundidade recursiva iterando no lado maior do partition.

## Desafio

- Escreva H1/H2 antes do benchmark; registre comparisons e tempo para random/sorted/reversed/duplicates em n=65536.
- Proponha pivot aleatório ou mediana-de-três como experimento isolado e descreva resultado esperado sem implementar ainda.
