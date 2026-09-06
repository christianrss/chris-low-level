# RESOLUÇÃO GUIADA — Debugger / Protocol v1

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `D2-DBG-APPEND-U16` | `starter/src/protocol.cpp` | `append_u16` |
| `D2-DBG-APPEND-U32` | `starter/src/protocol.cpp` | `append_u32` |
| `D2-DBG-READ-U16` | `starter/src/protocol.cpp` | `read_u16` |
| `D2-DBG-READ-U32` | `starter/src/protocol.cpp` | `read_u32` |
| `D2-DBG-FNV1A` | `starter/src/protocol.cpp` | `fnv1a` |
| `D2-DBG-ENCODE` | `starter/src/protocol.cpp` | `encode_debug_packet` |
| `D2-DBG-DECODE` | `starter/src/protocol.cpp` | `decode_debug_packet` |

Constantes do starter: `kMagic=0x31444B43`, `kVersion=1`, `kHeaderSize=20`.

> Trabalhe em `days/2026-09-04/debugger/protocol_v1/starter/`.

---

## Baseline

```bash
cmake -S starter -B starter/build && cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

---

## Exercício Fácil — LE u16/u32

### 1. O problema

Appends/reads são no-ops / retornam 0. Encode/decode não têm primitivas.

### 2. O algoritmo

LSB primeiro: byte0 = `value & 0xFF`, byte1 = `(value>>8)&0xFF`, … Decoder espelha com `|=` e shifts.

### 3. Escreva o código

```cpp
// append_u16
out.push_back(static_cast<std::uint8_t>(value & 0xFFu));
out.push_back(static_cast<std::uint8_t>((value >> 8) & 0xFFu));

// append_u32
for (int shift = 0; shift < 32; shift += 8) {
    out.push_back(static_cast<std::uint8_t>((value >> shift) & 0xFFu));
}

// read_u16
return static_cast<std::uint16_t>(
    bytes[offset] | (static_cast<std::uint16_t>(bytes[offset + 1]) << 8));

// read_u32
std::uint32_t value = 0;
for (int shift = 0; shift < 32; shift += 8) {
    value |= static_cast<std::uint32_t>(bytes[offset++]) << shift;
}
return value;
```

### 4. Por que funciona

Wire LE = padrão x86 e deste protocolo. Loop em u32 evita quatro linhas duplicadas.

Não use `memcpy` do host sem documentar endianness — em host BE o wire quebraria. Cast explícito para `uint8_t` evita warning de narrowing.

### 5. Verifique

No papel: `0x1234` → `34 12`. Magic → `43 4B 44 31` (`C K D 1`). Round-trip mental: append depois read no mesmo offset.

---

## Exercício Médio — `D2-DBG-FNV1A`

### 1. O problema

Hash sempre 0 — decode nunca detecta corrupção.

### 2. O algoritmo

Offset FNV-1a 32-bit + prime; XOR byte depois multiplica.

### 3. Escreva o código

```cpp
std::uint32_t hash = 2166136261U;
for (std::size_t i = 0; i < size; ++i) {
    hash ^= data[i];
    hash *= 16777619U;
}
return hash;
```

### 4. Por que funciona

Barato e sensível a qualquer byte. Não é autenticação criptográfica.

Constantes FNV-1a 32-bit: offset `2166136261`, prime `16777619` — não invente outras. Ordem XOR-depois-mul é o “1a”; FNV-1 multiplica antes (diferente).

### 5. Verifique

Altere último byte do payload (`^=0xFF`) — hash deve mudar. Payload vazio: hash = offset inicial (ainda assim grave no header).

---

## Exercício Difícil — `D2-DBG-ENCODE`

### 1. O problema

Encode devolve `{}`. Round-trip impossível.

### 2. O algoritmo

```text
se payload > 1MiB → invalid_argument
reserve(20+N)
append magic, version, command, request_id, size, fnv1a(payload)
insert payload
```

### 3. Escreva o código

```cpp
if (packet.payload.size() > 1024 * 1024) {
    throw std::invalid_argument("debug packet payload too large");
}
std::vector<std::uint8_t> out;
out.reserve(kHeaderSize + packet.payload.size());
append_u32(out, kMagic);
append_u16(out, kVersion);
append_u16(out, static_cast<std::uint16_t>(packet.command));
append_u32(out, packet.request_id);
append_u32(out, static_cast<std::uint32_t>(packet.payload.size()));
append_u32(out, fnv1a(packet.payload.data(), packet.payload.size()));
out.insert(out.end(), packet.payload.begin(), packet.payload.end());
return out;
```

### 4. Por que funciona

Ordem fixa do layout. Hash cobre só payload. Limite 1 MiB fecha alocação descontrolada.

`reserve` é otimização — correto mesmo sem ela, mas evita reallocs. Cast de `command`/`size` para larguras do wire deve bater com o layout (u16/u32).

### 5. Verifique

Encode com payload vazio: tamanho total = 20. Encode `{0xAA}`: size=21; bytes[12..16) = `01 00 00 00`.

---

## Exercício Desafio — `D2-DBG-DECODE`

### 1. O problema

Decode lança `TODO`. Testes negativos (truncado, magic, checksum) precisam de fail-fast ordenado.

### 2. O algoritmo

Validar nesta ordem: size≥20 → magic → version → ler campos → size==20+N → copiar → hash → comparar → packet.

### 3. Escreva o código

```cpp
if (bytes.size() < kHeaderSize) {
    throw std::runtime_error("debug packet header truncated");
}
if (read_u32(bytes, 0) != kMagic) {
    throw std::runtime_error("debug packet magic mismatch");
}
if (read_u16(bytes, 4) != kVersion) {
    throw std::runtime_error("unsupported debug protocol version");
}
const auto command = static_cast<DebugCommand>(read_u16(bytes, 6));
const std::uint32_t request_id = read_u32(bytes, 8);
const std::uint32_t payload_size = read_u32(bytes, 12);
const std::uint32_t expected_hash = read_u32(bytes, 16);
if (bytes.size() != kHeaderSize + payload_size) {
    throw std::runtime_error("debug packet length mismatch");
}
std::vector<std::uint8_t> payload(
    bytes.begin() + static_cast<std::ptrdiff_t>(kHeaderSize),
    bytes.end());
const std::uint32_t actual_hash = fnv1a(payload.data(), payload.size());
if (actual_hash != expected_hash) {
    throw std::runtime_error("debug packet checksum mismatch");
}
return {command, request_id, std::move(payload)};
```

### 4. Por que funciona

Falhar antes de copiar payload grande economiza trabalho. Mensagens distintas facilitam asserts dos testes.

### 5. Verifique

```bash
ctest --test-dir starter/build --output-on-failure
```

`{1,2,3}` → truncado; último byte XOR → checksum.

---

## Checkpoint no papel

Monte o header de payload `{0xAA,0xBB}`, command=1, request_id=42:

```text
magic CKD1 → 43 4B 44 31
version 1  → 01 00
command 1  → 01 00
request_id 42 → 2A 00 00 00
payload_size 2 → 02 00 00 00
hash = fnv1a([AA BB]) → 4 bytes LE
+ AA BB
```

Liste a ordem em que o decode deve falhar se: (a) buffer tem 19 bytes; (b) magic errado; (c) `payload_size` diz 100 mas buffer tem 22 bytes; (d) último byte XOR 0xFF.

## Debugging

1. Breakpoint em `actual_hash != expected_hash` — compare expected vs actual.
2. Não leia/copie payload se `bytes.size() != 20 + payload_size`.
3. Hexdump dos primeiros 20 bytes após encode; confira magic visualmente (`CKD1`).
4. Truncado `{1,2,3}` deve falhar **antes** de qualquer `read_u32` de campos além do guard de tamanho.

## Benchmark

```bash
cmake -S starter -B starter/build-bench -DCHRIS_BUILD_BENCHMARKS=ON
cmake --build starter/build-bench
./starter/build-bench/chris_debugger_protocol_benchmark
```

~300k encode+decode de payload 64 B — registre packets/s, máquina e compilador. Hipótese: FNV barato; custo domina em cópia do vetor.

## Mapa de consistência

Sete marcadores `PEDAGOGY-SOLUTION` em `solutions/src/protocol.cpp` ↔ sete TODOs.

## Relatório

| ID | Falha negativa |
|----|----------------|
| APPEND/READ | bytes invertidos |
| FNV1A | XOR último byte |
| ENCODE | >1 MiB rejeitado |
| DECODE | truncado / length / hash |

Aceite: `chris-debugger protocol tests passed`. Próximo: anote o que v1 **não** mitiga (replay, MITM).

## Ordem fail-fast (cole no caderno)

```text
1. size < 20           → header truncated
2. magic != CKD1       → magic mismatch
3. version != 1        → unsupported version
4. size != 20+N        → length mismatch
5. hash != expected    → checksum mismatch
```

Inverter 4 e 5 (hashar payload truncado/mentiroso) é o erro defensivo clássico — os testes negativos existem para pegar isso.

## Relatório de resolução

- TODOs concluídos: ___
- Testes starter: FAIL esperado antes / PASS depois? ___
- Paper-trace feito? Sim/Não
- Portei para projects/? Sim/Não — evidência: ___


Saída **esperada** no baseline do starter: testes falham até completar os TODOs. Após a solução, ctest/
pm test/dotnet run deve passar.
