# Pesquisa guiada — Merge sort vs quicksort

## O que buscar
- `merge sort recurrence T(n)=2T(n/2)+Theta(n)`
- `quicksort worst case sorted input last element pivot`
- `quicksort tail recursion smaller partition`
- `std::sort introsort implementation concept`

## Referências sugeridas
- Cormen, Leiserson, Rivest e Stein (CLRS), capítulos de sorting/divide-and-conquer.
- cppreference `std::sort` apenas para comparação da biblioteca padrão, não para copiar implementação.

## Perguntas
1. Por que merge sort mantém O(n log n) no pior caso?
2. Por que escolher sempre o último elemento como pivot cria O(n²) para dados ordenados?
3. Por que nosso `quick_sort_impl` recursa no lado menor e itera no maior?
4. O que `comparisons` mede? O que **não** mede?
5. Por que tempo real pode divergir do número de comparações?
