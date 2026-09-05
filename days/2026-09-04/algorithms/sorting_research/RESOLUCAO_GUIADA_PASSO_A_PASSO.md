# Resolução guiada passo a passo — Merge sort vs quicksort

## Mapa exato starter → resolução

- `D2-SORT-MERGE-RECURSE` → `starter/src/sort.cpp`
- `D2-SORT-MERGE-RANGE` → `starter/src/sort.cpp`
- `D2-SORT-PARTITION` → `starter/src/sort.cpp`
- `D2-SORT-QUICK-LOOP` → `starter/src/sort.cpp`

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

## Baseline

```bash
cmake -S days/2026-09-04/algorithms/sorting_research/starter -B days/2026-09-04/algorithms/sorting_research/starter/build
cmake --build days/2026-09-04/algorithms/sorting_research/starter/build
ctest --test-dir days/2026-09-04/algorithms/sorting_research/starter/build --output-on-failure
```

## Parte A — merge sort
Abra `starter/src/sort.cpp`.

### A1. Recursão
Em `merge_sort_impl`, escreva:

```cpp
if (end - begin <= 1) {
    return;
}
const std::size_t middle = begin + (end - begin) / 2;
merge_sort_impl(values, scratch, begin, middle, stats);
merge_sort_impl(values, scratch, middle, end, stats);
merge_range(values, scratch, begin, middle, end, stats);
```

Use intervalo semiaberto `[begin,end)`. Para 6 elementos, `begin=0,end=6,middle=3`.

### A2. Merge
Em `merge_range`, comece com três cursores:

```cpp
std::size_t left = begin;
std::size_t right = middle;
std::size_t out = begin;
```

Enquanto ambos os lados têm itens:

```cpp
while (left < middle && right < end) {
    ++stats.comparisons;
    if (values[left] <= values[right]) {
        scratch[out++] = values[left++];
    } else {
        scratch[out++] = values[right++];
    }
    ++stats.moves;
}
```

Copie sobras:

```cpp
while (left < middle) {
    scratch[out++] = values[left++];
    ++stats.moves;
}
while (right < end) {
    scratch[out++] = values[right++];
    ++stats.moves;
}
```

Copie scratch de volta:

```cpp
for (std::size_t i = begin; i < end; ++i) {
    values[i] = scratch[i];
    ++stats.moves;
}
```

Rode testes antes de implementar quicksort. Eles ainda falharão no quicksort, mas você pode temporariamente colocar breakpoint/print para confirmar merge.

## Parte B — quicksort
### B1. Partition
Em `partition`:

```cpp
const int pivot = values[end - 1];
std::size_t store = begin;
```

Percorra tudo menos o pivot:

```cpp
for (std::size_t i = begin; i + 1 < end; ++i) {
    ++stats.comparisons;
    if (values[i] < pivot) {
        if (i != store) {
            std::swap(values[i], values[store]);
            stats.moves += 3;
        }
        ++store;
    }
}
```

Coloque pivot na posição final:

```cpp
if (store != end - 1) {
    std::swap(values[store], values[end - 1]);
    stats.moves += 3;
}
return store;
```

### B2. Controlar profundidade de stack
Em `quick_sort_impl`, use loop:

```cpp
while (end - begin > 1) {
    const std::size_t pivot = partition(values, begin, end, stats);
    const std::size_t left_size = pivot - begin;
    const std::size_t right_size = end - (pivot + 1);
```

Recursa no lado menor e continua iterando no maior:

```cpp
    if (left_size < right_size) {
        quick_sort_impl(values, begin, pivot, stats);
        begin = pivot + 1;
    } else {
        quick_sort_impl(values, pivot + 1, end, stats);
        end = pivot;
    }
}
```

Isso limita profundidade de recursão mesmo quando as partições são ruins; **não corrige** o número O(n²) de comparações.

## Testes

```bash
cmake --build days/2026-09-04/algorithms/sorting_research/starter/build
ctest --test-dir days/2026-09-04/algorithms/sorting_research/starter/build --output-on-failure
```

Esperado: `chris-algorithms tests passed`.

## Debug
Para `{2,1}`, coloque breakpoint em `partition`. Observe `pivot=1`, `store=0`, loop, swap final. Para entrada ordenada de 6 itens, registre pivots e tamanhos das partições; você deve ver a degeneração.

## Pesquisa/benchmark
Antes de rodar, escreva:

```text
H1: merge sort terá comparações próximas de n log2(n) em todas as distribuições.
H2: quicksort com último pivot degradará fortemente em sorted/reversed.
```

Então:

```bash
cmake -S days/2026-09-04/algorithms/sorting_research/starter -B days/2026-09-04/algorithms/sorting_research/starter/build-bench -DCHRIS_BUILD_BENCHMARKS=ON
cmake --build days/2026-09-04/algorithms/sorting_research/starter/build-bench
./days/2026-09-04/algorithms/sorting_research/starter/build-bench/chris_algorithm_benchmark
```

Registre distribuição, n, tempo e comparações. Depois proponha mediana-de-três ou pivot aleatório como **nova hipótese**; não mude duas coisas ao mesmo tempo.


## Solução final comentada
Depois de deixar o starter verde, compare somente os blocos `PEDAGOGY-SOLUTION` em `solutions/` correspondentes aos IDs do mapa. Se houver uma linha necessária no gabarito que não foi ensinada acima, trate como defeito do material e não como algo que você deveria adivinhar.
