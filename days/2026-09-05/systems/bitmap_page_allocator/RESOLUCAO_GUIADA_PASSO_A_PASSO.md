# RESOLUÇÃO GUIADA — Systems / Bitmap page allocator

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `SYS-PAGE-ALLOC-01` | `starter/page_allocator.cpp` | `trace_page_to_bit`, `is_used`, `allocate` |
| `SYS-PAGE-FREE-02` | `starter/page_allocator.cpp` | `set_used`, `free_page` |

Cada ID existe como `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` no gabarito e `PEDAGOGY-TEST: ID` em `starter/test_page_allocator.cpp`.

> Trabalhe em `days/2026-09-05/systems/bitmap_page_allocator/starter/`. `solutions/` é gabarito — consulte só depois da tentativa.

> Não comece copiando `solutions/`. Compile e rode `ctest` após cada bloco.

---

## SYS-PAGE-ALLOC-01 — mapeamento, consulta e allocate

### 1. O problema (starter stub)

```cpp
PageBitTrace trace_page_to_bit(std::size_t page) {
    // TODO [SYS-PAGE-ALLOC-01]: retornar page, byte_index (page/8), bit_index (page%8)
    return {page, 0, 0};
}
bool PageAllocator::is_used(std::size_t page) const {
    // TODO [SYS-PAGE-ALLOC-01]: consultar bit no bitmap
    return true;
}
int PageAllocator::allocate() {
    // TODO [SYS-PAGE-ALLOC-01]: primeira página livre ou -1 (OOM)
    return -1;
}
```

`is_used` sempre `true` → `allocate` nunca encontra página livre → teste espera 0,1,2 depois `-1`.

### 2. O algoritmo

```text
trace(page):
  return {page, page/8, page%8}

is_used(page):
  se page ≥ page_count_ → true   // inexistente = não alocável
  return (bits_[page/8] & (1 << (page%8))) ≠ 0

allocate():
  para page em 0 .. page_count_-1:
    se !is_used(page):
      set_used(page, true)
      return (int)page
  return -1
```

### 3. Código completo

Em `starter/page_allocator.cpp` (API de `page_allocator.hpp` — `set_used` é privado):

```cpp
PageBitTrace trace_page_to_bit(std::size_t page) {
    return {page, page / 8, page % 8};
}

bool PageAllocator::is_used(std::size_t page) const {
    if (page >= page_count_) {
        return true;
    }
    return (bits_[page / 8] & static_cast<std::uint8_t>(1u << (page % 8))) != 0;
}

int PageAllocator::allocate() {
    for (std::size_t page = 0; page < page_count_; ++page) {
        if (!is_used(page)) {
            set_used(page, true);
            return static_cast<int>(page);
        }
    }
    return -1;
}
```

`set_used` ainda é stub: implemente `SYS-PAGE-FREE-02` antes do teste passar (allocate chama `set_used`).

### 4. Por que funciona?

- `page/8` e `page%8`: 8 páginas por byte; página 13 → byte 1, bit 5 (máscara `0x20`).
- Out-of-range como “usada”: `allocate` nunca devolve índice inválido.
- Scan 0…n−1: ordem determinística que o teste exige (0,1,2).
- Marcar antes de retornar: duas `allocate()` seguidas não pegam a mesma página.

### 5. Verificação parcial

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-05\systems\bitmap_page_allocator\starter
cmake -S . -B build
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

Com só ALLOC e `set_used` stub vazio, bits nunca mudam → `allocate` pode repetir 0 ou OOM. Complete FREE a seguir.

Trace esperado para página 13: `{13, 1, 5}`.

---

## SYS-PAGE-FREE-02 — set bit e free com double-free

### 1. O problema (starter stub)

```cpp
void PageAllocator::set_used(std::size_t page, bool used) {
    // TODO [SYS-PAGE-FREE-02]: setar ou limpar bit
}
bool PageAllocator::free_page(std::size_t page) {
    // TODO [SYS-PAGE-FREE-02]: liberar página usada; rejeitar double-free
    return false;
}
```

Sem `set_used`, allocate não persiste estado. Sem guard em `free_page`, double-free passa.

### 2. O algoritmo

```text
set_used(page, used):
  mask ← uint8(1 << (page % 8))
  se used: bits_[page/8] |= mask
  senão:   bits_[page/8] &= ~mask

free_page(page):
  se page ≥ page_count_ ou !is_used(page) → false
  set_used(page, false)
  return true
```

### 3. Código completo

```cpp
void PageAllocator::set_used(std::size_t page, bool used) {
    auto mask = static_cast<std::uint8_t>(1u << (page % 8));
    if (used) {
        bits_[page / 8] |= mask;
    } else {
        bits_[page / 8] &= static_cast<std::uint8_t>(~mask);
    }
}

bool PageAllocator::free_page(std::size_t page) {
    if (page >= page_count_ || !is_used(page)) {
        return false;
    }
    set_used(page, false);
    return true;
}
```

### 4. Por que funciona?

- `|=` / `&= ~mask`: altera um bit sem tocar nos vizinhos no mesmo byte.
- `uint8_t` na máscara: evita promoção signed em shifts.
- `!is_used` cobre double-free e never-allocated; `page >= page_count_` cobre `free_page(99)`.
- Após `free_page(1)`, o próximo `allocate()` devolve 1 (menor livre).

### 5. Verificação

```powershell
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

Saída esperada do executável:

```text
OK page allocator
```

Trace do Caso OOM (3 páginas):

```text
bits: 000 → 001 → 011 → 111 → allocate=-1
free(1) → 101; allocate → 1; free(1) de novo → false
```

---

## Mapa de consistência auditada

- `SYS-PAGE-ALLOC-01` — `starter/page_allocator.cpp` → `solutions/page_allocator.cpp`.
- `SYS-PAGE-FREE-02` — `starter/page_allocator.cpp` → `solutions/page_allocator.cpp`.

## Relatório de resolução

### O que foi validado

- TODOs `SYS-PAGE-ALLOC-01` e `SYS-PAGE-FREE-02` em `starter/page_allocator.cpp`.
- `PEDAGOGY-TEST`: trace página 13, sequência 0/1/2/−1, free+realloc, double-free, out-of-range.
- Starter falha até bits e scan estarem corretos.

### Armadilhas encontradas

- Trocar `/` e `%` no mapeamento.
- Scan até `bits_.size()*8` em vez de `page_count_` (bits fantasma no último byte).
- `free_page` sempre `true` sem checar `is_used`.

### Depuração e saída esperada

- **Depuração:** imprima `bits_[0]` em hex após cada `allocate`/`free_page`.
- **Saída esperada:** `OK page allocator`; `ctest` 100%.

### Próximo passo sugerido

Refazer sem a resolução. Meça scans em `BENCHMARK_GUIADO.md` (N grande, fragmentação artificial) e registre em **Resultados observados**.
