# Testes guiados

### Caso 1: `cmake -B build && cmake --build build` em starter/.
### Caso 2: **Trace page→byte→bit:** página 13 → byte 1, bit 5.
### Caso 3: **OOM:** alocador com 3 páginas retorna -1 na 4ª chamada.
### Caso 4: **Double-free:** `free_page` duas vezes na mesma página retorna false.
### Caso 5: **Out-of-range:** `free_page(99)` retorna false.
### Caso 6: Valide solutions/ com os mesmos testes.

## SYS-PAGE-ALLOC-01

Invariante protegida pelo teste com `PEDAGOGY-TEST: SYS-PAGE-ALLOC-01`.

## SYS-PAGE-FREE-02

Invariante protegida pelo teste com `PEDAGOGY-TEST: SYS-PAGE-FREE-02`.
