# Teoria passo a passo — Pesquisa empírica de sorting

## 1. Duas perguntas diferentes
Análise assintótica pergunta como custo cresce com n. Benchmark pergunta quanto uma implementação leva em uma máquina/configuração específica. Precisamos dos dois.

## 2. Merge sort
Divide ao meio até subarrays de tamanho 1; depois intercala. A recorrência é aproximadamente `T(n)=2T(n/2)+Theta(n)`, portanto O(n log n). Usa scratch adicional O(n).

## 3. Quicksort do laboratório
Usa Lomuto-like partition com **último elemento como pivot**. Em dados aleatórios pode funcionar bem, mas dados já ordenados produzem partições 0 e n-1 repetidamente, levando a ~n²/2 comparações.

## 4. Instrumentação
`SortStats.comparisons` conta comparações-chave; `moves` aproxima movimentações. Não mede branches, cache misses, alocações do runtime nem frequência de CPU.

## 5. Pesquisa empírica
O benchmark usa quatro distribuições com seed fixa: random, sorted, reversed e muitos duplicates. Hipótese deve ser escrita antes de rodar.
