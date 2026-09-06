## Mapa exato starter → resolução

| TODO ID | Starter |
|---------|--------|
| `SYS-PAGE-ALLOC-01` | `starter/page_allocator.cpp` |
| `SYS-PAGE-FREE-02` | `starter/page_allocator.cpp` |

# Resolução guiada passo a passo

Abra `starter/page_allocator.cpp`.

## `allocate()` - SYS-PAGE-ALLOC-01

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/page_allocator.cpp` |
| **Função / âncora** | comentário `TODO [SYS-PAGE-ALLOC-01]` neste arquivo |
| **Substituir** | o stub / corpo / case marcado por `TODO [SYS-PAGE-ALLOC-01]` |
| **Não mexer** | demais arquivos do starter até este ID passar nos testes |
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

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/page_allocator.cpp` |
| **Função / âncora** | comentário `TODO [SYS-PAGE-FREE-02]` neste arquivo |
| **Substituir** | o stub / corpo / case marcado por `TODO [SYS-PAGE-FREE-02]` |
| **Não mexer** | demais arquivos do starter até este ID passar nos testes |
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
## Relatório de resolução

- **TODOs concluídos:** (liste os IDs implementados)
- **Comandos de teste:**
  ```bash
  # cole aqui o comando exato usado
  ```
- **Saída esperada:** PASS nos testes do módulo
- **Invariantes verificadas:** (liste)
- **Edge cases testados:** (liste)
- **Benchmark:** hipótese + resultado ou declaração honesta de skip
- **Toolchain não executada:** (se aplicável)

### 4. Por que funciona

O stub no âncora TODO é substituído pelo comportamento testado.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.
