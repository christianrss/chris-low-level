# Resolução guiada passo a passo — Systems: bitmap page allocator

Abra `starter/page_allocator.cpp`.

Em `allocate()`, percorra `page=0..page_count-1`, teste `is_used(page)`, marque o primeiro livre e retorne seu índice. Se nenhum existir, retorne `-1`.
```cpp
for (std::size_t page=0; page<page_count_; ++page) {
    if (!is_used(page)) { set_used(page,true); return static_cast<int>(page); }
}
return -1;
```
Em `free_page(page)`, valide faixa e estado; retornar `false` para double-free. Depois `set_used(page,false)`.

Build/test:
```bash
cmake -S starter -B starter/build && cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```
Debug: imprima `page`, `page/8`, `page%8` e byte do bitmap quando um assert falhar.

## Mapa de consistência auditada
- `SYS-PAGE-ALLOC-01` — starter → resolução → teste → solution.
- `SYS-PAGE-FREE-02` — starter → resolução → teste → solution.
