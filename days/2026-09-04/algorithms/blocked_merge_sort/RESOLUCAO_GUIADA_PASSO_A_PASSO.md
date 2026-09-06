# RESOLUÇÃO GUIADA — Algorithms / Blocked merge sort

## Mapa exato starter → resolução

| TODO ID | Starter | Função/área |
|---------|---------|-------------|
| `D2-BLOCK-IO-STATS` | `starter/src/blocked_sort.cpp` | `account_tile_io` |
| `D2-BLOCK-SORT-TILE` | `starter/src/blocked_sort.cpp` | `sort_tile` |
| `D2-BLOCK-MERGE-RUN` | `starter/src/blocked_sort.cpp` | `merge_runs` |
| `D2-BLOCK-PASSES` | `starter/src/blocked_sort.cpp` | `blocked_merge_sort` |

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-04/algorithms/blocked_merge_sort/starter/`. `solutions/` é gabarito.

Intervalos **semiabertos** `[begin, end)`. I/O em unidades de tile: `ceil((end-begin)/tile_size)`.

---

## Baseline

```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

Build passa; testes falham enquanto os TODOs existem (`logic_error` / asserts).

---

## Ordem sugerida

1. `D2-BLOCK-IO-STATS` — helper puro, fácil de testar mentalmente.
2. `D2-BLOCK-SORT-TILE` — cria os runs iniciais.
3. `D2-BLOCK-MERGE-RUN` — núcleo do merge.
4. `D2-BLOCK-PASSES` — orquestra fases e liga o I/O.

---

## Exercício Fácil — `D2-BLOCK-IO-STATS`

### 1. O problema

`account_tile_io` no starter é vazio. Sem ele, Caso 4 nunca vê `block_reads` / `block_writes`.

### 2. O algoritmo

```text
tiles = tiles_covering(begin, end, tile_size)
se is_write: block_writes += tiles
senão:       block_reads  += tiles
```

`tiles_covering` já está fornecido: retorna 0 se o intervalo é vazio.

### 3. Escreva o código

```cpp
const std::uint64_t tiles =
    static_cast<std::uint64_t>(tiles_covering(begin, end, tile_size));
if (is_write) {
    stats.block_writes += tiles;
} else {
    stats.block_reads += tiles;
}
```

### 4. Por que funciona

Um tile é a unidade de transferência do modelo. Um run de 8 elementos com `tile_size=4` conta **2** writes, não 8 — alinha o lab a páginas/cache lines.

### 5. Verifique

No papel: `[0,8)` com tile 4 → 2; `[4,5)` → 1; `[0,0)` → 0.

---

## Exercício Médio A — `D2-BLOCK-SORT-TILE`

### 1. O problema

TODO vazio: tiles permanecem desordenados; a fase 0 não cria runs.

### 2. O algoritmo

Insertion sort em `[begin, end)` contando cada comparação `data[j-1]` vs `key`:

```text
para i = begin+1 .. end-1:
  key = data[i]; j = i
  enquanto j > begin:
    ++comparisons
    se data[j-1] <= key: break
    data[j] = data[j-1]; --j
  data[j] = key
```

### 3. Escreva o código

```cpp
for (std::size_t i = begin + 1; i < end; ++i) {
    const int key = data[i];
    std::size_t j = i;
    while (j > begin) {
        ++stats.comparisons;
        if (data[j - 1] <= key) {
            break;
        }
        data[j] = data[j - 1];
        --j;
    }
    data[j] = key;
}
```

### 4. Por que funciona

Insertion é estável e previsível para tiles pequenos — melhor para o lab do que `std::sort` (comparisons variam entre libcs). Trace `{3,1,2}`:

```text
i=1 key=1: 3<=1? não → shift → [1,3,2]
i=2 key=2: 3<=2? não → shift; 1<=2? sim → [1,2,3]
```

### 5. Verifique

Caso 2 do teste: `{3,1,2}` com tile 8 → ordenado e exatamente 1 read + 1 write (quando o pass driver chamar o helper).

---

## Exercício Médio B — `D2-BLOCK-MERGE-RUN`

### 1. O problema

Duas metades ordenadas em `src` não se intercalam em `dst`.

### 2. O algoritmo

```text
left=begin, right=mid, out=begin
enquanto left<mid e right<end:
  ++comparisons
  se src[left] <= src[right]: dst[out++] = src[left++]
  senão:                      dst[out++] = src[right++]
copie sobras left e right (sem comparison)
```

### 3. Escreva o código

```cpp
std::size_t left = begin;
std::size_t right = mid;
std::size_t out = begin;
while (left < mid && right < end) {
    ++stats.comparisons;
    if (src[left] <= src[right]) {
        dst[out++] = src[left++];
    } else {
        dst[out++] = src[right++];
    }
}
while (left < mid) {
    dst[out++] = src[left++];
}
while (right < end) {
    dst[out++] = src[right++];
}
```

### 4. Por que funciona

Dois cursores em sequências ordenadas; o menor avança. `<=` mantém estabilidade. Trace `[5,6,7,8|1,2,3,4]`: quatro vezes `5<=k?` falha para k=1..4, depois sobras 5..8.

### 5. Verifique

Ainda sem `D2-BLOCK-PASSES` o suite falha; confira o trace no papel e conte as 4 comparisons iniciais do exemplo.

---

## Exercício Difícil — `D2-BLOCK-PASSES`

### 1. O problema

`blocked_merge_sort` lança `logic_error`. Falta: validar `tile_size`, sort de tiles com I/O, loop de merges, ping-pong `data`/`scratch`.

### 2. O algoritmo

```text
se tile_size==0: throw invalid_argument
se n<=1: return

para cada tile [begin,end):
  account READ; sort_tile; account WRITE

scratch[n]; src=&data; dst=&scratch; run_len=tile_size
enquanto run_len < n:
  para begin em passos 2*run_len:
    mid=min(begin+run_len,n); end=min(begin+2*run_len,n)
    account READ left; account READ right
    se mid>=end: copie src→dst
    senão: merge_runs(src,begin,mid,end,dst,stats)
    account WRITE [begin,end)
  swap src,dst; run_len *= 2
se src != &data: data.swap(scratch)
```

### 3. Escreva o código

```cpp
if (tile_size == 0) {
    throw std::invalid_argument("tile_size must be > 0");
}
const std::size_t n = data.size();
if (n <= 1) {
    return;
}

for (std::size_t begin = 0; begin < n; begin += tile_size) {
    const std::size_t end = std::min(begin + tile_size, n);
    account_tile_io(stats, begin, end, tile_size, false);
    sort_tile(data, begin, end, stats);
    account_tile_io(stats, begin, end, tile_size, true);
}

std::vector<int> scratch(n);
std::vector<int>* src = &data;
std::vector<int>* dst = &scratch;
std::size_t run_len = tile_size;

while (run_len < n) {
    for (std::size_t begin = 0; begin < n; begin += 2 * run_len) {
        const std::size_t mid = std::min(begin + run_len, n);
        const std::size_t end = std::min(begin + 2 * run_len, n);
        account_tile_io(stats, begin, mid, tile_size, false);
        account_tile_io(stats, mid, end, tile_size, false);
        if (mid >= end) {
            std::copy(src->begin() + static_cast<std::ptrdiff_t>(begin),
                      src->begin() + static_cast<std::ptrdiff_t>(end),
                      dst->begin() + static_cast<std::ptrdiff_t>(begin));
        } else {
            merge_runs(*src, begin, mid, end, *dst, stats);
        }
        account_tile_io(stats, begin, end, tile_size, true);
    }
    std::swap(src, dst);
    run_len *= 2;
}

if (src != &data) {
    data.swap(scratch);
}
```

### 4. Por que funciona

Fase 0 garante runs de comprimento ≤ `tile_size`. Cada pass dobra o comprimento do run ordenado — igual ao merge sort bottom-up, mas com I/O explícito por tile. O swap `src/dst` evita copiar o buffer inteiro entre passes; o `swap` final publica o resultado em `data` se o último pass escreveu em `scratch`.

Contagem Caso 4 (`n=8`, `tile=4`):

```text
sort: 2R+2W
merge run_len=4: READ 1+1, WRITE 2 → 2R+2W
total 4R+4W
```

### 5. Verifique

```bash
ctest --test-dir starter/build --output-on-failure
```

Saída esperada: `chris-algorithms tests passed`.

---

## Debugging

| Sintoma | Onde olhar |
|---------|------------|
| Ordenado, I/O errado | `account_tile_io` e se cada pass conta left+right+out |
| Últimos elementos bagunçados | run ímpar (`mid >= end`) sem `std::copy` |
| Resultado no scratch “fantasma” | faltou `data.swap(scratch)` |
| crash / throw inesperado | `tile_size==0` |

Depure com n=8 no papel antes de reler o código.

## Pesquisa / benchmark

Antes de rodar, escreva H1/H2 sobre `tile_size`. Depois:

```bash
cmake -S starter -B starter/build-bench -DCHRIS_BUILD_BENCHMARKS=ON
cmake --build starter/build-bench
./starter/build-bench/algorithm_benchmark
```

Registre `tile`, `cmp`, `bread`, `bwrite`, `us`. Uma variável por experimento.

## Relatório

| ID | Observação |
|----|------------|
| IO-STATS | unidades de tile, não de elemento |
| SORT-TILE | insertion + comparisons |
| MERGE-RUN | estabilidade com `<=` |
| PASSES | bottom-up + ping-pong buffers |

## Relatório de resolução

- TODOs concluídos: ___
- Testes starter: FAIL esperado antes / PASS depois? ___
- Paper-trace n=8 tile=4 feito? Sim/Não
- Portei para projects/? Sim/Não — evidência: ___

Saída **esperada** no baseline do starter: testes falham até completar os TODOs. Após a solução, `ctest` deve passar.
