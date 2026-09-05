# Resolução guiada passo a passo

Abra `starter/page_allocator.cpp`.

## `allocate()` - SYS-PAGE-ALLOC-01
```cpp
for (std::size_t page = 0; page < page_count_; ++page) {
    if (!is_used(page)) {
        set_used(page, true);
        return static_cast<int>(page);
    }
}
return -1;
```

Rode o teste; as três primeiras alocações devem produzir 0, 1 e 2 e a quarta deve retornar -1.

## `free_page()` - SYS-PAGE-FREE-02
Valide `page >= page_count_` e `!is_used(page)`. Nesses casos retorne `false`. Caso contrário chame `set_used(page, false)` e retorne `true`.

Build/test:
```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

Debug: para uma página `p`, imprima temporariamente `p/8`, `p%8` e o valor do byte do bitmap.

## Mapa de consistência auditada
- `SYS-PAGE-ALLOC-01` - starter -> resolução -> teste -> solution.
- `SYS-PAGE-FREE-02` - starter -> resolução -> teste -> solution.
