# Resolução guiada passo a passo — Systems — alocador bitmap de páginas

## Mapa exato starter → resolução

- `SYS-PAGE-ALLOC-01` → `starter/page_allocator.cpp` (`trace_page_to_bit`, `is_used`, `allocate`)
- `SYS-PAGE-FREE-02` → `starter/page_allocator.cpp` (`set_used`, `free_page`)

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-05/systems/bitmap_page_allocator/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

## 0. Preparar o projeto

Na raiz do repositório:

```bash
cmake -S days/2026-09-05/systems/bitmap_page_allocator/starter -B days/2026-09-05/systems/bitmap_page_allocator/starter/build
cmake --build days/2026-09-05/systems/bitmap_page_allocator/starter/build
ctest --test-dir days/2026-09-05/systems/bitmap_page_allocator/starter/build --output-on-failure
```

O build deve funcionar. O teste **deve falhar** enquanto os TODOs existirem — `trace_page_to_bit(13)` espera byte 1, bit 5.

## Exercício fácil — `trace_page_to_bit` (SYS-PAGE-ALLOC-01)

### Arquivo

Abra:

```text
starter/page_allocator.cpp
```

Localize:

```cpp
PageBitTrace trace_page_to_bit(std::size_t page) {
```

Substitua o corpo por:

```cpp
return {page, page / 8, page % 8};
```

### Por que funciona?

Cada byte cobre 8 páginas consecutivas. Divisão inteira `page / 8` seleciona o byte; resto `page % 8` seleciona o bit dentro desse byte. Para página 13: byte 1 (páginas 8–15), bit 5.

### Verificação manual

| page | byte_index | bit_index |
|-----:|-----------:|----------:|
| 0    | 0          | 0         |
| 7    | 0          | 7         |
| 8    | 1          | 0         |
| 13   | 1          | 5         |

## Exercício médio — `is_used` e `set_used`

### `is_used`

Localize `PageAllocator::is_used` e substitua por:

```cpp
if (page >= page_count_) {
    return true;
}
return (bits_[page / 8] & static_cast<std::uint8_t>(1u << (page % 8))) != 0;
```

### Por que funciona?

A máscara `1u << (page % 8)` isola exatamente um bit no byte. `&` diferente de zero significa página usada. Out-of-range retorna `true` para que `allocate` nunca “encontre” uma página inválida como livre.

### `set_used`

Localize `PageAllocator::set_used`:

```cpp
auto mask = static_cast<std::uint8_t>(1u << (page % 8));
if (used) {
    bits_[page / 8] |= mask;
} else {
    bits_[page / 8] &= static_cast<std::uint8_t>(~mask);
}
```

### Por que funciona?

`|=` liga o bit sem afetar os outros; `&= ~mask` limpa só aquele bit. Usar `std::uint8_t` evita promoção signed inesperada na máscara.

## Exercício difícil — `allocate` (SYS-PAGE-ALLOC-01)

Localize `PageAllocator::allocate`:

```cpp
for (std::size_t page = 0; page < page_count_; ++page) {
    if (!is_used(page)) {
        set_used(page, true);
        return static_cast<int>(page);
    }
}
return -1;
```

### Por que funciona?

Scan linear da menor página livre garante ordem 0, 1, 2… como o teste espera. Marcar antes de retornar evita race lógica (em single-thread, duas chamadas seguidas não recebem a mesma página). `-1` sinaliza OOM quando o loop termina sem candidato.

## Exercício final — `free_page` (SYS-PAGE-FREE-02)

Localize `PageAllocator::free_page`:

```cpp
if (page >= page_count_ || !is_used(page)) {
    return false;
}
set_used(page, false);
return true;
```

### Por que funciona?

`!is_used(page)` cobre double-free e liberação de página nunca alocada — o bit já está 0, então retorna `false` sem corromper estado. Só páginas válidas e usadas passam para `set_used(false)`.

## Rode os testes novamente

```bash
cmake --build days/2026-09-05/systems/bitmap_page_allocator/starter/build
ctest --test-dir days/2026-09-05/systems/bitmap_page_allocator/starter/build --output-on-failure
```

Saída esperada:

```text
OK page allocator
100% tests passed
```

## Como depurar se falhar

- **`trace.byte_index` errado para 13**: confira `page / 8` (não `% 8`).
- **`allocate` retorna -1 cedo**: `is_used` provavelmente sempre `true` — stub não foi substituído.
- **double-free passa**: `free_page` não checa `is_used` antes de limpar.
- **OOM não acontece com 3 páginas**: loop deve ir até `page_count_`, não `bits_.size() * 8` sem limite.

No GDB:

```bash
gdb --args days/2026-09-05/systems/bitmap_page_allocator/starter/build/chris_page_allocator_tests
```

Breakpoint em `allocate`; observe `bits_[0]` em hexadecimal após cada alocação.

## Solução final comentada

Compare seu arquivo com `solutions/page_allocator.cpp`. Você deve conseguir justificar mapeamento page→bit, scan, OOM e rejeição de double-free.

## Relatório de resolução

| ID | Função | Resultado esperado |
|----|--------|-------------------|
| SYS-PAGE-ALLOC-01 | `trace_page_to_bit` | página 13 → byte 1, bit 5 |
| SYS-PAGE-ALLOC-01 | `is_used`, `allocate` | sequência 0,1,2; depois -1 |
| SYS-PAGE-FREE-02 | `set_used`, `free_page` | libera 1; realoca 1; segunda free false |

Critério de aceite: `ctest` reporta `OK page allocator` e 100% dos testes. Se `free_page(99)` não retorna `false`, revise o guard `page >= page_count_`.
