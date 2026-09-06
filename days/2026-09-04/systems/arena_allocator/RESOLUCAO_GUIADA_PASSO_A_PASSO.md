# RESOLUÇÃO GUIADA — Systems / Arena allocator

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `D2-ARENA-POWER2` | `starter/src/arena.cpp` | `is_power_of_two` |
| `D2-ARENA-ALIGN-UP` | `starter/src/arena.cpp` | `align_up` |
| `D2-ARENA-ALLOCATE` | `starter/src/arena.cpp` | `allocate` |
| `D2-ARENA-RESET` | `starter/src/arena.cpp` | `reset` |

> Trabalhe em `days/2026-09-04/systems/arena_allocator/starter/`. `solutions/` após tentativa.

Estado: `storage_` (`vector<byte>`), `offset_` (cursor). Consulta: `used()` / `capacity()` — não confundir `used()` com o endereço alinhado da próxima alocação.

---

## Baseline

```bash
cmake -S starter -B starter/build && cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

Build passa; testes falham (TODOs). Isso prova que o defeito é pedagógico, não de CMake/linker.

Ordem sugerida: POWER2 → ALIGN-UP → ALLOCATE → RESET. Sem as duas primeiras, `allocate` não tem como alinhar com segurança.

---

## Exercício Fácil — `D2-ARENA-POWER2`

### 1. O problema

Starter sempre retorna `false`. Alinhamentos válidos (8, 16, 32) são rejeitados depois, ou o teste de power-of-two falha.

### 2. O algoritmo

Potência de dois tem um único bit 1: `v & (v-1) == 0`, e `v != 0`.

### 3. Escreva o código

```cpp
return value != 0 && (value & (value - 1)) == 0;
```

### 4. Por que funciona

`8=1000b`, `7=0111b`, AND=0. Zero também daria AND=0 — por isso o guard `!= 0`.

Não use `value % 2 == 0`: aceita 6, 10, 12… e quebra `align_up` (máscara inválida).

### 5. Verifique

No papel: 1→true, 8→true, 16→true, 3→false, 6→false, 0→false.

---

## Exercício Médio — `D2-ARENA-ALIGN-UP`

### 1. O problema

Lança `TODO align_up`. Sem arredondamento, `allocate` não alinha ponteiros.

### 2. O algoritmo

```text
se !is_power_of_two(alignment) → invalid_argument
mask = alignment - 1
return (value + mask) & ~mask
```

### 3. Escreva o código

```cpp
if (!is_power_of_two(alignment)) {
    throw std::invalid_argument("alignment must be a power of two");
}
const std::size_t mask = alignment - 1;
return (value + mask) & ~mask;
```

### 4. Por que funciona

Máscara limpa os bits baixos após “empurrar” para o próximo múltiplo. Trace: `13,A=8` → mask=7 → 20 & ~7 = 16.

Já alinhado permanece: `16,A=8` → (16+7)&~7 = 16. Arredondar **para baixo** quebraria invariante “≥ value”.

### 5. Verifique

Alignment 3 deve lançar. Tabela rápida: (0,8)→0; (1,8)→8; (17,8)→24.

---

## Exercício Difícil — `D2-ARENA-ALLOCATE`

### 1. O problema

Lança `TODO allocate`. Precisa: size≠0, alinhar `base+offset_`, caber sem overflow, avançar cursor, retornar ptr interno.

### 2. O algoritmo

```text
size==0 → invalid_argument
base = uintptr_t(storage_.data())
aligned_addr = align_up(base + offset_, alignment)
aligned_offset = aligned_addr - base
se aligned_offset > size OU size > size - aligned_offset → bad_alloc
offset_ = aligned_offset + size
return data() + aligned_offset
```

### 3. Escreva o código

```cpp
if (size == 0) {
    throw std::invalid_argument("allocation size must be non-zero");
}
const std::size_t base = reinterpret_cast<std::uintptr_t>(storage_.data());
const std::size_t aligned_address = align_up(base + offset_, alignment);
const std::size_t aligned_offset = aligned_address - base;
if (aligned_offset > storage_.size() || size > storage_.size() - aligned_offset) {
    throw std::bad_alloc();
}
offset_ = aligned_offset + size;
return storage_.data() + static_cast<std::ptrdiff_t>(aligned_offset);
```

### 4. Por que funciona

Alinha o endereço **real** — correto mesmo se `data()` não for múltiplo de A. A checagem `size > cap - aligned` evita overflow de `size_t`. Cursor avança para a próxima alocação não sobrepor.

Armadilha: alinhar só `offset_` ignora desalinhamento da base.

Por que não `aligned_offset + size > storage_.size()`? Se `aligned_offset + size` wrapear em `size_t`, a comparação pode passar falsamente. Separar em duas checagens é o padrão seguro.

### 5. Verifique

Após duas alocações com A=32, `second % 32 == 0`. Capacidade curta → `bad_alloc`. size=0 → `invalid_argument` (não `bad_alloc`).

---

## Exercício Final — `D2-ARENA-RESET`

### 1. O problema

`reset` vazio: cursor não volta; reuso do bloco falha ou “vaza” logicamente. Testes que alocam, resetam e alocam de novo esperam o mesmo endereço base (ou ao menos `offset_==0`).

### 2. O algoritmo

`offset_ = 0` — O(1), sem percorrer objetos, sem `free` por bloco.

### 3. Escreva o código

```cpp
offset_ = 0;
```

Não chame `storage_.clear()` — isso mudaria a capacidade. Não itere ponteiros antigos.

### 4. Por que funciona

Arena bump: lifetime em lote. Não chama destrutores C++ — limitação consciente do lab. Placement-new de objetos com recursos exigiria destruição manual **antes** do reset.

### 5. Verifique

```bash
ctest --test-dir starter/build --output-on-failure
```

Esperado: `chris-arena tests passed`.

---

## Checkpoint no papel

Arena capacidade 32, comece `offset_=0`:

```text
allocate(5, 8)   → faixa 0..5; próximo cursor alinhado a 8
allocate(3, 8)   → 8..11; próximo 16
allocate(10, 16) → padding até 16; 16..26; próximo 32
allocate(1, 8)   → bad_alloc
reset()
allocate(20, 8)  → 0..20 OK
```

Caso base desalinhada (conceitual): `base=0x1001`, A=16, `offset_=0`:

```text
ERRADO: align_up(0, 16) = 0     → ptr 0x1001 (não múltiplo de 16)
CERTO:  align_up(0x1001, 16) = 0x1010 → offset 15
```

Responda em uma frase, antes do debugger: por que o lab alinha `base+offset_` e não só o cursor?

Padding conta como fragmentação interna: entre o fim de `allocate(5,8)` e o início do próximo alinhado a 8 há bytes “perdidos” até o reset.

## Debugging

| Sintoma | Olhar |
|---------|-------|
| `second % 32 != 0` | `base`, `offset_`, `aligned_address`, `aligned_offset` |
| `bad_alloc` cedo | `storage_.size() - aligned_offset` vs `size` |
| A=3 não lança | `is_power_of_two(3)` deve ser false |
| reset falha | `offset_` antes/depois; uso de ptr antigo após reset = UB |
| duas allocs sobrepõem | esqueceu `offset_ = aligned_offset + size` |

GDB/VS: breakpoint em `Arena::allocate`, Watch nas quatro variáveis acima. No VS, abra o test target e adicione `base`/`aligned_offset` ao Watch.

```bash
gdb --args starter/build/chris_arena_tests
```

## Benchmark

```bash
cmake -S starter -B starter/build-bench -DCHRIS_BUILD_BENCHMARKS=ON
cmake --build starter/build-bench
./starter/build-bench/chris_arena_benchmark
```

**Antes** de rodar, escreva a hipótese: para muitas alocações temporárias de tamanho fixo, arena reduz overhead vs várias `new`. Não transforme um resultado local em regra universal; anote se o loop mede destruição no lado heap.

## Mapa de consistência

`PEDAGOGY-SOLUTION` em `solutions/src/arena.cpp` ↔ quatro TODOs. Justifique cada linha: validação, alinhamento, capacidade, cursor, reset.

## Relatório

| ID | Aceite |
|----|--------|
| POWER2 | 0 e não-potências false |
| ALIGN-UP | máscara; A inválido lança |
| ALLOCATE | ptr alinhado; overflow → bad_alloc |
| RESET | `offset_=0` O(1) |

Critério: `chris-arena tests passed`. Se alinhamento falhar, revise `base+offset_`, não só `offset_`. Anote em `BENCHMARK_GUIADO.md` a hipótese e a mediana — não só o “vencedor”.

## Exemplo trabalhado — overflow vs invalid_argument

```text
capacity = 16, offset_ = 0
allocate(0, 8)     → invalid_argument  (size zero)
allocate(8, 8)     → OK, offset_ = 8
allocate(8, 8)     → OK, offset_ = 16
allocate(1, 8)     → bad_alloc         (não cabe)
allocate(8, 3)     → invalid_argument  (A não é potência de 2)
```

Separe mentalmente: **argumento ilegal** (`invalid_argument`) vs **arena cheia** (`bad_alloc`). Testes cobrem ambos; misturar as exceções falha asserts específicos.

Checklist rápido antes do `ctest` final:

- [ ] `is_power_of_two(0)==false`
- [ ] `align_up(13,8)==16`
- [ ] segundo `allocate(..., 32)` com ptr `% 32 == 0`
- [ ] `reset` zera cursor; alocação seguinte reutiliza o bloco

API do starter: `Arena(capacity)`, `allocate(size, alignment)`, `reset()`, `used()`, `capacity()`. Helpers `is_power_of_two` / `align_up` são privados — implemente-os, não exponha overloads novos.

Depois do verde: compare `PEDAGOGY-SOLUTION` em `solutions/src/arena.cpp` linha a linha. Se o gabarito tiver uma checagem que esta resolução não ensinou, abra issue no material — não “adivinhe” em silêncio.

Hipótese de portfólio: este bump allocator reaparece em parsers e em hot paths do `chris-os`; a disciplina de overflow é a mesma do page allocator (Day 05).

## Relatório de resolução

- TODOs concluídos: ___
- Testes starter: FAIL esperado antes / PASS depois? ___
- Paper-trace feito? Sim/Não
- Portei para projects/? Sim/Não — evidência: ___
