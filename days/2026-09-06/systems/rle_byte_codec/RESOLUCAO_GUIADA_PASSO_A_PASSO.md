# RESOLUÇÃO GUIADA — Systems / RLE byte codec

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `COMP-RLE-01` | `starter/rle.cpp` | `encode_rle` — header CHRLE + LE32 + runs |
| `COMP-RLE-02` | `starter/rle.cpp` | `decode_rle` — magic + expansão de pares |
| `COMP-RLE-03` | `starter/rle.cpp` | `decode_rle` — `out.size() == len` |

Cada ID existe como `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` no gabarito e `PEDAGOGY-TEST: ID` em `starter/test_rle.cpp`.

> Trabalhe em `days/2026-09-06/systems/rle_byte_codec/starter/`. `solutions/` é gabarito — consulte só depois da tentativa.

> Não comece copiando `solutions/`. Compile e rode `ctest` após cada TODO.

---

## COMP-RLE-01 — encode: header + runs

### 1. O problema (starter stub)

Em `starter/rle.cpp`:

```cpp
bool encode_rle(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    // TODO [COMP-RLE-01]: escrever header CHRLE + length LE32 e compactar runs (count, byte)
    (void)input;
    return false;
}
```

Com `return false`, o Caso 1 de `test_rle.cpp` falha imediatamente em `CHECK(encode_rle(in, enc))`.

### 2. O algoritmo

```text
out ← vazio
anexar bytes de "CHRLE" (5)
anexar input.size() como u32 little-endian
i ← 0
enquanto i < n:
  j ← i+1
  enquanto j < n e input[j]==input[i] e (j-i) < 255:
    j ← j+1
  emitir uint8(j-i), input[i]
  i ← j
retornar true
```

### 3. Código completo

Substitua o corpo de `encode_rle` em `starter/rle.cpp` (mantenha `#include "rle.hpp"` e `<cstring>`):

```cpp
bool encode_rle(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    out.insert(out.end(), CHRLE_MAGIC, CHRLE_MAGIC + 5);
    const std::uint32_t len = static_cast<std::uint32_t>(input.size());
    out.push_back(static_cast<std::uint8_t>(len & 0xFF));
    out.push_back(static_cast<std::uint8_t>((len >> 8) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((len >> 16) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((len >> 24) & 0xFF));
    std::size_t i = 0;
    while (i < input.size()) {
        std::size_t j = i + 1;
        while (j < input.size() && input[j] == input[i] && (j - i) < 255) {
            ++j;
        }
        const std::uint8_t count = static_cast<std::uint8_t>(j - i);
        out.push_back(count);
        out.push_back(input[i]);
        i = j;
    }
    return true;
}
```

### 4. Por que funciona? (entenda linha a linha)

- `out.clear()`: cada encode começa do zero; evita concatenar com chamada anterior.
- `out.insert(..., CHRLE_MAGIC, CHRLE_MAGIC + 5)`: copia só os 5 caracteres, não o NUL do array.
- Quatro `push_back` do `len`: little-endian explícito — portável sem `memcpy` de host-endian.
- `i` / `j`: janela da run atual; `(j - i) < 255` garante que `count` cabe em `uint8_t` e nunca vira 0 por wrap.
- `count` depois `input[i]`: ordem do contrato CHRLE — decoder lê na mesma ordem.
- `return true`: qualquer `span` finito é representável.

### 5. Verificação cmake/ctest (ainda parcial)

No diretório do módulo:

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\systems\rle_byte_codec\starter
cmake -S . -B build
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

Esperado **ainda FAIL**: `decode_rle` continua stub. O encode sozinho não completa o Caso 1. Se quiser inspecionar hex antes do decode, chame `encode_rle` num scratch e confira que 10 zeros geram:

```text
43 48 52 4C 45 0A 00 00 00 0A 00
```

---

## COMP-RLE-02 — decode: magic + expansão

### 1. O problema (starter stub)

```cpp
bool decode_rle(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    // TODO [COMP-RLE-02]: validar magic e expandir runs
    // TODO [COMP-RLE-03]: rejeitar payload truncado (out.size() != len)
    (void)input;
    return false;
}
```

Sem validação, o Caso 3 (magic corrompido) não pode ser exercitado de forma significativa; sem expansão, Casos 1–2 falham.

### 2. O algoritmo

```text
out ← vazio
se input.size() < 9 → false
se memcmp(input, "CHRLE", 5) ≠ 0 → false
len ← u32 LE dos bytes [5..8]
p ← 9
enquanto p+1 < size e out.size() < len:
  count ← input[p++]; value ← input[p++]
  para k = 0..count-1 enquanto out.size() < len:
    out.push(value)
# COMP-RLE-03 trata o return — ver próxima seção
```

### 3. Código completo (magic + loop; return na seção seguinte)

Implemente a validação e o loop em `decode_rle`:

```cpp
bool decode_rle(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    if (input.size() < 9 || std::memcmp(input.data(), CHRLE_MAGIC, 5) != 0) {
        return false;
    }
    std::uint32_t len = 0;
    len |= input[5];
    len |= static_cast<std::uint32_t>(input[6]) << 8;
    len |= static_cast<std::uint32_t>(input[7]) << 16;
    len |= static_cast<std::uint32_t>(input[8]) << 24;
    out.reserve(len);
    std::size_t p = 9;
    while (p + 1 < input.size() && out.size() < len) {
        const std::uint8_t count = input[p++];
        const std::uint8_t value = input[p++];
        for (std::uint8_t k = 0; k < count && out.size() < len; ++k) {
            out.push_back(value);
        }
    }
    return out.size() == len;  // COMP-RLE-03
}
```

### 4. Por que funciona? (entenda linha a linha)

- `size < 9`: header incompleto — não leia `input[8]`.
- `memcmp(..., 5)`: contrato do Caso 3; `enc[0]='X'` faz retornar `false` sem tentar expandir.
- Montagem de `len` com `|` e shifts: espelho do encoder LE32.
- `out.reserve(len)`: evita realloc em runs longas (opcional para passar testes, útil em prática).
- `p + 1 < input.size()`: precisa de **dois** bytes (count e value) antes de consumir.
- `out.size() < len` no `for`: se o encoder mentir com count grande, não escreve além do declarado.
- `CHRLE_MAGIC` vem de `rle.hpp` — mesma constante do encode.

### 5. Verificação cmake/ctest

Rebuild e teste:

```powershell
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

Com `return out.size() == len` já no código acima, Casos 1–3 devem passar. Se você deixou `return true` temporário, o Caso de truncamento artificial (exercício) falharia — por isso `COMP-RLE-03` é explícito.

---

## COMP-RLE-03 — rejeitar payload truncado

### 1. O problema

Mesmo com magic correto e loop de expansão, um implementador ingênuo faz:

```cpp
return true;  // ERRADO
```

Isso aceita header `len=10` com um único par `(3,0)` → três zeros “válidos”. O contrato CHRLE exige plaintext completo.

O starter marca isso no mesmo `decode_rle`:

```cpp
// TODO [COMP-RLE-03]: rejeitar payload truncado (out.size() != len)
```

### 2. O algoritmo

Após o loop de expansão:

```text
sucesso ⟺ out.size() == len
```

Não use `>=` (não deveria ocorrer se o loop respeita `len`) nem ignore `len`.

### 3. Código completo (linha crítica)

A linha final de `decode_rle`:

```cpp
    return out.size() == len;
```

Junto com o corpo da seção `COMP-RLE-02`, isso fecha o decoder.

### 4. Por que funciona? (entenda linha a linha)

- `out.size()`: bytes realmente emitidos.
- `len`: promessa do header (plaintext original).
- Igualdade estrita: truncado → `false`; completo → `true`.
- Se `len == 0` e magic ok com payload vazio: `out` vazio → `true` (encode de input vazio: só header 9 bytes).

### 5. Verificação cmake/ctest

Os testes oficiais cobrem round-trip e magic; para forçar `COMP-RLE-03` manualmente, no depurador ou num scratch:

```cpp
std::vector<std::uint8_t> bad = {'C','H','R','L','E', 6,0,0,0, 3,'A'}; // len=6, só 3 bytes
std::vector<std::uint8_t> out;
assert(!decode_rle(bad, out));
```

Suite oficial:

```powershell
ctest --test-dir build -C Release --output-on-failure
```

Saída esperada do executável:

```text
OK rle
```

---

## Ordem sugerida e smoke no gabarito

1. Implemente `COMP-RLE-01` em `starter/rle.cpp`.
2. Implemente `COMP-RLE-02` + `COMP-RLE-03` no mesmo arquivo.
3. Confira `starter/test_rle.cpp` — Casos 1, 2, 3 com marcadores `PEDAGOGY-TEST`.
4. Opcional: compare com `solutions/rle.cpp` só no final.

Gabarito (esperado PASS):

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\systems\rle_byte_codec\solutions
cmake -S . -B build
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

Starter sem TODOs (esperado FAIL):

```powershell
cd ..\starter
cmake -S . -B build
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

---

## Hex de referência (Caso 1)

Input: 10 bytes `0x00`.

| Região | Hex |
|--------|-----|
| magic | `43 48 52 4C 45` |
| len | `0A 00 00 00` |
| run | `0A 00` |

## Hex de referência (Caso 2)

Input: `41 42 43 44` (`ABCD`).

| Região | Hex |
|--------|-----|
| magic + len=4 | `43 48 52 4C 45 04 00 00 00` |
| runs | `01 41 01 42 01 43 01 44` |

Observe expansão: 4 bytes → 8 de payload + 9 de header.

---

## Mapa de consistência auditada

- `COMP-RLE-01` — `starter/rle.cpp` → `solutions/rle.cpp` (`encode_rle`).
- `COMP-RLE-02` — `starter/rle.cpp` → `solutions/rle.cpp` (`decode_rle` magic/loop).
- `COMP-RLE-03` — `starter/rle.cpp` → `solutions/rle.cpp` (`out.size() == len`).

## Relatório de resolução

### O que foi validado

- TODOs `COMP-RLE-01..03` implementados em `starter/rle.cpp` na ordem encode → decode → contrato de tamanho.
- `starter/test_rle.cpp` com `PEDAGOGY-TEST: COMP-RLE-01/02/03` passa após a implementação.
- Starter original retorna `false` e falha o `ctest` até cada ID ser preenchido.

### Armadilhas encontradas

- Cap de run em 255 (não 256): `(j - i) < 255` antes do cast para `uint8_t`.
- Magic com 5 bytes no fio; array C tem NUL — use `+ 5`, não `sizeof`.
- LE32 manual evita surpresas de endianness do host.
- `return true` no decode sem comparar `len` aceita truncamento silencioso.

### Depuração e saída esperada

- **Depuração:** imprima `out` em hex após encode; confira magic e o primeiro par `(count,byte)`.
- **Saída esperada:** `OK rle` no stdout do `test_rle`; `ctest` 100% no Release.

### Próximo passo sugerido

Refazer o encode/decode sem olhar esta resolução. Depois meça razão de compressão em `BENCHMARK_GUIADO.md` (runs longas vs ASCII sem repetição) e registre em **Resultados observados**.
