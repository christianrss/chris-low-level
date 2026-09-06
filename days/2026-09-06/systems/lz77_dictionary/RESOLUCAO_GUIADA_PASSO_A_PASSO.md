# Resolução guiada passo a passo — Systems — LZ77 dictionary codec

## Mapa exato starter → resolução

| TODO ID | Starter | Função/área |
|---------|---------|-------------|
| `COMP-LZ77-01` | `starter/lz77.cpp` | `find_longest_match` — clipe `LZ77_WINDOW_SIZE` |
| `COMP-LZ77-02` | `starter/lz77.cpp` | `find_longest_match` — maior match ≥ `LZ77_MIN_MATCH` |
| `COMP-LZ77-03` | `starter/lz77.cpp` | `encode_lz77` — header CHLZ7 + tokens |
| `COMP-LZ77-04` | `starter/lz77.cpp` | `decode_lz77` — literais + cópia da janela |

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-06/systems/lz77_dictionary/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

> Não comece copiando `solutions/`. Siga os passos abaixo e compile a cada etapa.

## 0. Preparar o projeto

```bash
cmake -S days/2026-09-06/systems/lz77_dictionary/starter -B days/2026-09-06/systems/lz77_dictionary/starter/build
cmake --build days/2026-09-06/systems/lz77_dictionary/starter/build --config Release
ctest --test-dir days/2026-09-06/systems/lz77_dictionary/starter/build -C Release --output-on-failure
```

PowerShell (Windows):

```powershell
cmake -S days/2026-09-06/systems/lz77_dictionary/starter -B days/2026-09-06/systems/lz77_dictionary/starter/build
cmake --build days/2026-09-06/systems/lz77_dictionary/starter/build --config Release
ctest --test-dir days/2026-09-06/systems/lz77_dictionary/starter/build -C Release --output-on-failure
```

O build deve funcionar. O teste **deve falhar** enquanto `find_longest_match` retorna `false` e `encode_lz77`/`decode_lz77` retornam `false`.

---

## Exercício A — janela 32 KiB (`COMP-LZ77-01`)

### 1. O problema

Em `starter/lz77.cpp`, o stub zera `match` e retorna `false`. Sem clipe de janela, qualquer busca “desde o início do buffer” aceitaria offsets > 32768, o que o formato e o teste (`m.offset <= LZ77_WINDOW_SIZE`) rejeitam conceitualmente.

### 2. O algoritmo

```text
se pos >= data.size(): return false
window_start = (pos > LZ77_WINDOW_SIZE) ? pos - LZ77_WINDOW_SIZE : 0
candidatos = start ∈ [window_start, pos)
```

### 3. Escreva o código (esqueleto da busca)

Abra `starter/lz77.cpp` e comece `find_longest_match` assim:

```cpp
bool find_longest_match(std::span<const std::uint8_t> data, std::size_t pos, LZ77Match& match) {
    match = {};
    if (pos >= data.size()) {
        return false;
    }
    const std::size_t window_start = (pos > LZ77_WINDOW_SIZE) ? (pos - LZ77_WINDOW_SIZE) : 0;
    const std::size_t max_len =
        static_cast<std::size_t>(std::min<std::size_t>(LZ77_MAX_MATCH, data.size() - pos));
    std::size_t best_len = 0;
    std::uint16_t best_off = 0;
    for (std::size_t start = window_start; start < pos; ++start) {
        // COMP-LZ77-02 preenche o corpo do loop
        (void)start;
        (void)max_len;
        (void)best_len;
        (void)best_off;
    }
    (void)best_len;
    (void)best_off;
    return false;
}
```

Inclua `#include <algorithm>` no topo se ainda não estiver.

### 4. Entenda linha por linha

- `match = {}`: estado limpo se não houver match.
- `window_start`: início inclusivo da janela deslizante.
- `max_len`: não ler além do fim nem além de 255.
- Loop só dentro da janela: **isso é `COMP-LZ77-01`**.

### 5. Verify

Constantes do teste:

```cpp
CHECK(LZ77_WINDOW_SIZE == 32768);
CHECK(LZ77_MIN_MATCH == 3);
```

Ainda sem match real o teste falha no `find_longest_match` — avance para o exercício B.

---

## Exercício B — longest match (`COMP-LZ77-02`)

### 1. O problema

Dentro da janela, vários `start` podem coincidir parcialmente. Precisamos do **maior** `len >= LZ77_MIN_MATCH`, e o `offset = pos - start` correspondente.

### 2. O algoritmo

```text
best_len = 0, best_off = 0
para start em [window_start, pos):
  len = 0
  enquanto len < max_len e data[start+len] == data[pos+len]:
    len++
  se len >= MIN_MATCH e len > best_len:
    best_len = len; best_off = pos - start
se best_len >= MIN_MATCH:
  match = {best_off, best_len}; return true
senão return false
```

### 3. Escreva o código completo

Substitua o corpo de `find_longest_match` por:

```cpp
bool find_longest_match(std::span<const std::uint8_t> data, std::size_t pos, LZ77Match& match) {
    match = {};
    if (pos >= data.size()) {
        return false;
    }
    const std::size_t window_start = (pos > LZ77_WINDOW_SIZE) ? (pos - LZ77_WINDOW_SIZE) : 0;
    const std::size_t max_len =
        static_cast<std::size_t>(std::min<std::size_t>(LZ77_MAX_MATCH, data.size() - pos));
    std::size_t best_len = 0;
    std::uint16_t best_off = 0;
    for (std::size_t start = window_start; start < pos; ++start) {
        std::size_t len = 0;
        while (len < max_len && data[start + len] == data[pos + len]) {
            ++len;
        }
        if (len >= LZ77_MIN_MATCH && len > best_len) {
            best_len = len;
            best_off = static_cast<std::uint16_t>(pos - start);
        }
    }
    if (best_len >= LZ77_MIN_MATCH) {
        match.offset = best_off;
        match.length = static_cast<std::uint8_t>(best_len);
        return true;
    }
    return false;
}
```

### 4. Entenda linha por linha

- `while` de comparação: match guloso byte a byte.
- `len > best_len`: empate mantém o offset **mais antigo** (menor `start`); ambos são válidos.
- Cast para `uint8_t`/`uint16_t`: cabe nos campos do struct.

### 5. Verify

Com `phrase = "ABCABCABCD"`, `pos = 3`:

```text
esperado: length >= 3, offset <= 32768 (tipicamente offset=3, length=6)
```

Recompile e rode o teste — ainda falhará em encode/decode.

---

## Exercício C — encode CHLZ7 (`COMP-LZ77-03`)

### 1. O problema

`encode_lz77` limpa `out` e retorna `false`. Precisa emitir magic, tamanho LE32 e, para cada posição, ou literal `0x00`+byte ou match `0x01`+offset LE + length.

### 2. O algoritmo

```text
out ← "CHLZ7"
out ← u32le(input.size())
pos ← 0
enquanto pos < n:
  se find_longest_match(...):
    emitir 01 | off_lo | off_hi | length
    pos += length
  senão:
    emitir 00 | input[pos]
    pos += 1
return true
```

### 3. Escreva o código completo

```cpp
bool encode_lz77(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    out.insert(out.end(), CHLZ7_MAGIC, CHLZ7_MAGIC + 5);
    const std::uint32_t len = static_cast<std::uint32_t>(input.size());
    out.push_back(static_cast<std::uint8_t>(len & 0xFF));
    out.push_back(static_cast<std::uint8_t>((len >> 8) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((len >> 16) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((len >> 24) & 0xFF));
    std::size_t pos = 0;
    while (pos < input.size()) {
        LZ77Match m{};
        if (find_longest_match(input, pos, m)) {
            out.push_back(0x01);
            out.push_back(static_cast<std::uint8_t>(m.offset & 0xFF));
            out.push_back(static_cast<std::uint8_t>((m.offset >> 8) & 0xFF));
            out.push_back(m.length);
            pos += m.length;
        } else {
            out.push_back(0x00);
            out.push_back(input[pos]);
            ++pos;
        }
    }
    return true;
}
```

### 4. Entenda linha por linha

- `CHLZ7_MAGIC + 5`: **não** copie o `\0` do array de 6 chars.
- LE32: byte baixo primeiro — bate com o decode.
- `pos += m.length`: pular o trecho coberto pelo match.

### 5. Verify

Após encode, `enc.size() >= 9` e `memcmp(enc.data(), "CHLZ7", 5) == 0`. O teste ainda exige decode round-trip.

---

## Exercício D — decode sliding window (`COMP-LZ77-04`)

### 1. O problema

`decode_lz77` deve validar magic, ler `len`, expandir tokens até `out.size() == len`, rejeitando streams inválidos (incluindo magic corrompido no teste).

### 2. O algoritmo

```text
se size < 9 ou magic ≠ CHLZ7: fail
len ← u32le(bytes[5..8])
p ← 9
enquanto out.size() < len e p < input.size():
  tag ← input[p++]
  se tag == 0x00: push literal
  se tag == 0x01: ler offset, length; validar; copiar byte a byte
  senão: fail
return out.size() == len
```

### 3. Escreva o código completo

Inclua `#include <cstring>` para `std::memcmp`.

```cpp
bool decode_lz77(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    if (input.size() < 9 || std::memcmp(input.data(), CHLZ7_MAGIC, 5) != 0) {
        return false;
    }
    std::uint32_t len = 0;
    len |= input[5];
    len |= static_cast<std::uint32_t>(input[6]) << 8;
    len |= static_cast<std::uint32_t>(input[7]) << 16;
    len |= static_cast<std::uint32_t>(input[8]) << 24;
    out.reserve(len);
    std::size_t p = 9;
    while (out.size() < len && p < input.size()) {
        const std::uint8_t tag = input[p++];
        if (tag == 0x00) {
            if (p >= input.size()) {
                return false;
            }
            out.push_back(input[p++]);
        } else if (tag == 0x01) {
            if (p + 2 >= input.size()) {
                return false;
            }
            const std::uint16_t offset =
                static_cast<std::uint16_t>(input[p] | (static_cast<std::uint16_t>(input[p + 1]) << 8));
            p += 2;
            if (p >= input.size()) {
                return false;
            }
            const std::uint8_t match_len = input[p++];
            if (offset == 0 || offset > out.size()) {
                return false;
            }
            const std::size_t start = out.size() - offset;
            for (std::uint8_t i = 0; i < match_len && out.size() < len; ++i) {
                out.push_back(out[start + i]);
            }
        } else {
            return false;
        }
    }
    return out.size() == len;
}
```

### 4. Entenda linha por linha

- `offset > out.size()`: histórico insuficiente.
- `out.push_back(out[start + i])`: permite overlap (runs).
- `out.size() < len` no for: não ultrapassar o tamanho declarado.
- Retorno estrito `out.size() == len`: truncamento → false.

### 5. Verify

```text
encode → decode → dec == in
enc[0] = 'X' → !decode_lz77(...)
stdout: OK lz77
```

---

## Mapa de consistência auditada

- `COMP-LZ77-01` — `starter/lz77.cpp` → `solutions/lz77.cpp` (`find_longest_match` window).
- `COMP-LZ77-02` — `starter/lz77.cpp` → `solutions/lz77.cpp` (`find_longest_match` best len).
- `COMP-LZ77-03` — `starter/lz77.cpp` → `solutions/lz77.cpp` (`encode_lz77`).
- `COMP-LZ77-04` — `starter/lz77.cpp` → `solutions/lz77.cpp` (`decode_lz77`).

## Relatório de resolução

### O que foi validado

- Todos os TODOs do `starter/` foram implementados na ordem 01→04.
- `PEDAGOGY-TEST: COMP-LZ77-01..04` passam com a suite `test_lz77`.
- O starter original falha de propósito até cada ID ser preenchido.

### Armadilhas encontradas

- Copiar 6 bytes de `CHLZ7_MAGIC` inclui `\0` e quebra o magic.
- `memcpy` em match overlapping falha em runs (`AAAA`).
- Offset big-endian passa em dados simétricos e quebra em offsets ≥ 256.
- Esquecer `pos += m.length` gera tokens duplicados e decode “longo demais”.

### Depuração e saída esperada

- **Depuração:** imprima `pos`, `m.offset`, `m.length` no encode; no decode, imprima `tag` e `out.size()`.
- **Saída esperada:** `OK lz77`. Magic corrompido → decode false. Round-trip idêntico.

### Próximo passo sugerido

Refaça sem olhar esta resolução. Depois leia `BENCHMARK_GUIADO.md` e registre medianas na seção **Resultados observados**. Considere portar o codec para `projects/chris-compress` como estágio de dicionário.


### Por que funciona?

Cada passo acima preserva o contrato do header/API e o invariante de round-trip; veja o algoritmo na seção correspondente.
