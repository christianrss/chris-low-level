# Teoria passo a passo — Sorting como pesquisa algorítmica

## 1. Complexidade e entrada
Merge sort mantém O(n log n) no pior caso. Um quicksort com pivot ingênuo pode cair para O(n²) em entradas já ordenadas.

## 2. Corretude
Uma implementação de sorting precisa preservar o multiconjunto de elementos e produzir ordem não decrescente. Os testes comparam contra `std::sort` como oráculo, mas a explicação da corretude não depende dele.

## 3. Instrumentação
Contar comparações e movimentos cria uma métrica independente do relógio. O tempo real adiciona cache, branch prediction, compilador e alocação.

## 4. Pesquisa
Use a mesma seed e distribuições: random, sorted, reversed e duplicates. Não tire conclusão universal de uma única máquina.

## 5. Exercícios
**Fácil:** trace merge de `[2,5]` com `[1,7]`.  
**Médio:** implemente merge sort instrumentado.  
**Difícil:** implemente quicksort e explique o pior caso do pivot final.  
**Desafio:** adicione pivot aleatório/median-of-three e faça uma ablation controlada.
