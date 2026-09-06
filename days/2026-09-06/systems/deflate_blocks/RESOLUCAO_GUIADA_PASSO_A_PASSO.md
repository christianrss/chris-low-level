# Resolução guiada passo a passo — Systems — DEFLATE blocks

## Mapa exato starter → resolução

| TODO ID | Starter | Função/área |
|---------|---------|-------------|
| `COMP-DEFL-01` | `starter/bit_stream.cpp` | `BitWriter` / `BitReader` LSB-first |
| `COMP-DEFL-02` | `starter/deflate.cpp` | `encode_stored_block` |
| `COMP-DEFL-03` | `starter/deflate.cpp` | `decode_stored_blocks` |
| `COMP-DEFL-04` | `starter/deflate.cpp` | `build_fixed_literal_tables` + `encode_fixed_block` |
| `COMP-DEFL-05` | `starter/deflate.cpp` | `decode_fixed_block` |

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-06/systems/deflate_blocks/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

> Não comece copiando `solutions/`. Siga os passos abaixo e compile a cada etapa.

## 0. Preparar o projeto

```bash
cmake -S days/2026-09-06/systems/deflate_blocks/starter -B days/2026-09-06/systems/deflate_blocks/starter/build
cmake --build days/2026-09-06/systems/deflate_blocks/starter/build --config Release
ctest --test-dir days/2026-09-06/systems/deflate_blocks/starter/build -C Release --output-on-failure
```

O build compila; o teste falha nos `REQUIRE` de `0x1B` / stored / fixed enquanto os TODOs estão vazios.

---

## Exercício A — bitstream LSB-first (`COMP-DEFL-01`)

### 1. O problema

`BitWriter::write_bit` está vazio; `read_bit` sempre retorna `false`. Sem isso, nenhum bloco DEFLATE é testável.

### 2. O algoritmo

Acumule bits no `bit_buf_` com peso `1 << bit_count` (LSB-first); flush a cada 8. `write_bits` emite `(value >> i) & 1` para `i = 0..count-1`. Reader espelha com `(byte >> (bit_pos % 8)) & 1`.

### 3. Escreva o código completo

Em `starter/bit_stream.cpp`:

```cpp
void BitWriter::write_bit(bool bit) {
    if (bit) {
        bit_buf_ |= (1u << bit_count_);
    }
    ++bit_count_;
    if (bit_count_ == 8) {
        out_.push_back(static_cast<std::uint8_t>(bit_buf_ & 0xFFu));
        bit_buf_ = 0;
        bit_count_ = 0;
    }
}

void BitWriter::write_bits(std::uint32_t value, int count) {
    for (int i = 0; i < count; ++i) {
        write_bit((value >> i) & 1u);
    }
}

void BitWriter::align_byte() {
    if (bit_count_ != 0) {
        out_.push_back(static_cast<std::uint8_t>(bit_buf_ & 0xFFu));
        bit_buf_ = 0;
        bit_count_ = 0;
    }
}

bool BitReader::read_bit() {
    if (bit_pos_ >= in_.size() * 8) {
        return false;
    }
    const auto byte = in_[bit_pos_ / 8];
    const auto bit = (byte >> (bit_pos_ % 8)) & 1u;
    ++bit_pos_;
    return bit != 0;
}

std::uint32_t BitReader::read_bits(int count) {
    std::uint32_t value = 0;
    for (int i = 0; i < count; ++i) {
        if (read_bit()) {
            value |= (1u << i);
        }
    }
    return value;
}

bool BitReader::has_bits(int count) const {
    return (in_.size() * 8) - bit_pos_ >= static_cast<std::size_t>(count);
}

void BitReader::align_byte() {
    const auto rem = bit_pos_ % 8;
    if (rem != 0) {
        bit_pos_ += 8 - rem;
    }
}
```

`take_bytes()` já chama `align_byte()` — não remova isso.

### 4. Entenda linha por linha

- `(value >> i) & 1`: LSB primeiro (RFC). Flush em 8 → `out_`. Reader usa o mesmo peso.

### 5. Verify

`write_bits(0b1011,4); write_bits(0b0001,4); take_bytes() → {0x1B}` e reader recupera os nibbles.
---

## Exercício B — encode stored (`COMP-DEFL-02`)

### 1. O problema

`encode_stored_block` retorna `{}`. Precisa emitir header de 3 bits, alinhar, LEN/NLEN e payload.

### 2. O algoritmo

`BFINAL` (1 bit) + `BTYPE=00` (2 bits) → `align_byte` → `LEN`/`NLEN` u16 LE → payload byte a byte → `take_bytes()`.

### 3. Escreva o código completo

Em `starter/deflate.cpp`:

```cpp
std::vector<std::uint8_t> encode_stored_block(const std::vector<std::uint8_t>& data, bool final_block) {
    BitWriter writer;
    writer.write_bits(final_block ? 1u : 0u, 1);
    writer.write_bits(0u, 2);
    writer.align_byte();

    const auto len = static_cast<std::uint16_t>(data.size());
    const auto nlen = static_cast<std::uint16_t>(~len);
    writer.write_bits(len & 0xFFu, 8);
    writer.write_bits((len >> 8) & 0xFFu, 8);
    writer.write_bits(nlen & 0xFFu, 8);
    writer.write_bits((nlen >> 8) & 0xFFu, 8);
    for (const auto byte : data) {
        writer.write_bits(byte, 8);
    }
    return writer.take_bytes();
}
```

### 4. Entenda linha por linha

- `BTYPE=00` em 2 bits após BFINAL.
- `~len` em `uint16_t`: complemento de um em 16 bits.
- Payload via `write_bits(byte, 8)` mantém a mesma API de bits (já alinhada).

### 5. Verify

Encode `{'D','E','F','L'}` com `final_block=true`; tamanho ≥ 1+4+4+4. Decode ainda falta.

---

## Exercício C — decode stored (`COMP-DEFL-03`)

### 1. O problema

`decode_stored_blocks` deve ler um ou mais blocos stored até `BFINAL=1`, validando LEN/NLEN.

### 2. O algoritmo

Loop até `BFINAL`: ler `BTYPE` (deve ser 0), alinhar, validar `nlen == uint16_t(~len)`, copiar `len` bytes.

### 3. Escreva o código completo

```cpp
std::vector<std::uint8_t> decode_stored_blocks(const std::vector<std::uint8_t>& raw) {
    BitReader reader(raw);
    std::vector<std::uint8_t> out;
    bool final = false;
    while (!final) {
        final = reader.read_bit();
        const auto btype = reader.read_bits(2);
        if (btype != 0) {
            throw std::runtime_error("only stored blocks supported in this decoder path");
        }
        reader.align_byte();
        const auto len_lo = reader.read_bits(8);
        const auto len_hi = reader.read_bits(8);
        const auto nlen_lo = reader.read_bits(8);
        const auto nlen_hi = reader.read_bits(8);
        const auto len = static_cast<std::uint16_t>(len_lo | (len_hi << 8));
        const auto nlen = static_cast<std::uint16_t>(nlen_lo | (nlen_hi << 8));
        if (static_cast<std::uint16_t>(~len) != nlen) {
            throw std::runtime_error("LEN/NLEN mismatch");
        }
        for (std::uint16_t i = 0; i < len; ++i) {
            out.push_back(static_cast<std::uint8_t>(reader.read_bits(8)));
        }
    }
    return out;
}
```

### 4. Entenda linha por linha

- Loop `while (!final)`: permite vários blocos stored não-finais (lab testa um final).
- Checagem `~len`: contrato RFC; teste indireto via round-trip.

### 5. Verify

```text
decode_stored_blocks(encode_stored_block(payload, true)) == payload
```

---

## Exercício D — tabelas fixas + encode (`COMP-DEFL-04`)

### 1. O problema

`build_fixed_literal_tables` retorna zeros; `encode_fixed_block` retorna vazio. Sem códigos canônicos + `reverse_bits`, o fixed round-trip falha.

### 2. O algoritmo

Preencher `lens[]` RFC → `bl_count`/`next_code` canônico → `reverse_bits` → encode com `BTYPE=01` + literais + EOB 256.

### 3. Escreva o código completo

```cpp
namespace {

std::uint16_t reverse_bits(std::uint16_t code, int len) {
    std::uint16_t rev = 0;
    for (int i = 0; i < len; ++i) {
        if ((code >> i) & 1u) {
            rev |= static_cast<std::uint16_t>(1u << (len - 1 - i));
        }
    }
    return rev;
}

}  // namespace

FixedLitTables build_fixed_literal_tables() {
    std::uint8_t lens[288]{};
    for (int i = 0; i <= 143; ++i) lens[i] = 8;
    for (int i = 144; i <= 255; ++i) lens[i] = 9;
    lens[256] = 7;
    for (int i = 257; i <= 285; ++i) lens[i] = 8;
    for (int i = 286; i <= 287; ++i) lens[i] = 8;

    std::uint16_t bl_count[16]{};
    for (int i = 0; i < 288; ++i) {
        if (lens[i]) ++bl_count[lens[i]];
    }

    std::uint16_t next_code[16]{};
    std::uint16_t code = 0;
    for (int bits = 1; bits <= 15; ++bits) {
        code = static_cast<std::uint16_t>((code + bl_count[bits - 1]) << 1);
        next_code[bits] = code;
    }

    FixedLitTables tables{};
    for (int sym = 0; sym < 288; ++sym) {
        if (!lens[sym]) continue;
        const auto canonical = next_code[lens[sym]]++;
        tables.code[sym] = reverse_bits(canonical, lens[sym]);
        tables.len[sym] = lens[sym];
    }
    return tables;
}

std::vector<std::uint8_t> encode_fixed_block(const std::vector<std::uint8_t>& literals, bool final_block) {
    const auto tables = build_fixed_literal_tables();
    BitWriter writer;
    writer.write_bits(final_block ? 1u : 0u, 1);
    writer.write_bits(1u, 2);
    for (const auto byte : literals) {
        writer.write_bits(tables.code[byte], tables.len[byte]);
    }
    writer.write_bits(tables.code[256], tables.len[256]);
    return writer.take_bytes();
}
```

### 4. Entenda linha por linha

- Faixas de `lens`: cópia direta da RFC 1951 §3.2.6.
- `next_code`: numeração canônica por comprimento.
- `reverse_bits`: adapta à ordem de bits do DEFLATE.
- EOB 256: sem ele o decoder não sabe onde parar.

### 5. Verify

`tables.len[256] == 7`, `tables.len[65] == 8`. Encode de `"RFC1951"` produz bytes não vazios.

---

## Exercício E — decode fixed (`COMP-DEFL-05`)

### 1. O problema

`decode_fixed_block` deve ler BTYPE=01 e decodificar símbolos até 256.

### 2. O algoritmo

Acumular bits LSB-first até achar `(len, code)` nas tabelas; emitir literais 0–255; parar em 256; rejeitar length codes.

### 3. Escreva o código completo

```cpp
namespace {

// reverse_bits já definido no exercício D

int decode_symbol(BitReader& reader, const FixedLitTables& tables) {
    std::uint32_t code = 0;
    for (int len = 1; len <= 15; ++len) {
        code |= reader.read_bit() ? (1u << (len - 1)) : 0u;
        for (int sym = 0; sym < 288; ++sym) {
            if (tables.len[sym] == len && tables.code[sym] == code) {
                return sym;
            }
        }
    }
    throw std::runtime_error("invalid fixed huffman code");
}

}  // namespace

std::vector<std::uint8_t> decode_fixed_block(const std::vector<std::uint8_t>& raw) {
    const auto tables = build_fixed_literal_tables();
    BitReader reader(raw);
    std::vector<std::uint8_t> out;
    bool final = false;
    while (!final) {
        final = reader.read_bit();
        const auto btype = reader.read_bits(2);
        if (btype != 1) {
            throw std::runtime_error("expected fixed huffman block");
        }
        while (true) {
            const int sym = decode_symbol(reader, tables);
            if (sym == 256) {
                break;
            }
            if (sym < 0 || sym > 255) {
                throw std::runtime_error("literal out of range");
            }
            out.push_back(static_cast<std::uint8_t>(sym));
        }
    }
    return out;
}
```

### 4. Entenda linha por linha

- Acúmulo `code |= bit << (len-1)`: mesma ordem LSB-first do writer.
- Scan 288 símbolos: O(288·L) aceitável no lab.
- Rejeitar `sym > 255` (exceto 256 já tratado): lab sem matches.

### 5. Verify

```text
decode_fixed_block(encode_fixed_block("RFC1951", true)) == literals
stdout: OK deflate blocks
```

---

## Mapa de consistência auditada

- `COMP-DEFL-01` — `starter/bit_stream.cpp` → `solutions/bit_stream.cpp`.
- `COMP-DEFL-02` — `starter/deflate.cpp` → `solutions/deflate.cpp` (`encode_stored_block`).
- `COMP-DEFL-03` — `starter/deflate.cpp` → `solutions/deflate.cpp` (`decode_stored_blocks`).
- `COMP-DEFL-04` — `starter/deflate.cpp` → `solutions/deflate.cpp` (tables + `encode_fixed_block`).
- `COMP-DEFL-05` — `starter/deflate.cpp` → `solutions/deflate.cpp` (`decode_fixed_block`).

## Relatório de resolução

### O que foi validado

- TODOs `COMP-DEFL-01..05` implementados na ordem bitstream → stored → fixed.
- Suite `test_deflate` imprime `OK deflate blocks`.
- Starter continua falhando de propósito até cada ID ser preenchido.

### Armadilhas encontradas

- Loop MSB-first em `write_bits` passa em alguns padrões e falha no nibble `0x1B`.
- Esquecer `reverse_bits` nas tabelas: stored ok, fixed quebra.
- Omitir EOB 256: hang ou throw no decode.
- `NLEN` com `int16_t` signed shift: valores errados para LEN altos.

### Depuração e saída esperada

- **Depuração:** imprima `bit_buf_`/`bit_count_` após cada `write_bits`; no reader, logue `bit_pos_`.
- **Saída esperada:** `OK deflate blocks`. Hex stored de `DEFL` começa com `01 04 00 FB FF ...`.

### Próximo passo sugerido

Refaça sem consultar esta resolução. Meça encode fixed vs stored em `BENCHMARK_GUIADO.md`. Una com `lz77_dictionary` ao portar para `projects/chris-compress`.


### Por que funciona?

Cada passo acima preserva o contrato do header/API e o invariante de round-trip; veja o algoritmo na seção correspondente.
