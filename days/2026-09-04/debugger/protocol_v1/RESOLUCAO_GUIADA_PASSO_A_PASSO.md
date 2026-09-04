# Resolução guiada passo a passo — chris-debugger protocol v1

## Baseline

```bash
cmake -S days/2026-09-04/debugger/protocol_v1/starter -B days/2026-09-04/debugger/protocol_v1/starter/build
cmake --build days/2026-09-04/debugger/protocol_v1/starter/build
ctest --test-dir days/2026-09-04/debugger/protocol_v1/starter/build --output-on-failure
```

## Fácil — serialização little-endian
Em `starter/src/protocol.cpp`, `append_u16`:

```cpp
out.push_back(static_cast<std::uint8_t>(value & 0xFFu));
out.push_back(static_cast<std::uint8_t>((value >> 8) & 0xFFu));
```

`append_u32`:

```cpp
for (int shift = 0; shift < 32; shift += 8) {
    out.push_back(static_cast<std::uint8_t>((value >> shift) & 0xFFu));
}
```

Decoder inverso:

```cpp
return static_cast<std::uint16_t>(
    bytes[offset] | (static_cast<std::uint16_t>(bytes[offset + 1]) << 8));
```

E para u32:

```cpp
std::uint32_t value = 0;
for (int shift = 0; shift < 32; shift += 8) {
    value |= static_cast<std::uint32_t>(bytes[offset++]) << shift;
}
return value;
```

## Médio — checksum FNV-1a

```cpp
std::uint32_t hash = 2166136261U;
for (std::size_t i = 0; i < size; ++i) {
    hash ^= data[i];
    hash *= 16777619U;
}
return hash;
```

Explique: isso é checksum/hash simples para detectar corrupção, **não** MAC/assinatura.

## Difícil — encode
Primeiro limite payload:

```cpp
if (packet.payload.size() > 1024 * 1024) {
    throw std::invalid_argument("debug packet payload too large");
}
```

Reserve e escreva campos na ordem do layout:

```cpp
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

## Desafio — decode defensivo
Implemente validações nesta ordem: `bytes.size() >= 20`; magic; version; leia command/id/size/hash; verifique tamanho exato; copie payload; calcule hash; compare; retorne packet.

Código essencial:

```cpp
if (bytes.size() < kHeaderSize) throw std::runtime_error("debug packet header truncated");
if (read_u32(bytes, 0) != kMagic) throw std::runtime_error("debug packet magic mismatch");
if (read_u16(bytes, 4) != kVersion) throw std::runtime_error("unsupported debug protocol version");
```

Depois:

```cpp
const auto command = static_cast<DebugCommand>(read_u16(bytes, 6));
const std::uint32_t request_id = read_u32(bytes, 8);
const std::uint32_t payload_size = read_u32(bytes, 12);
const std::uint32_t expected_hash = read_u32(bytes, 16);
```

Valide tamanho antes de construir payload:

```cpp
if (bytes.size() != kHeaderSize + payload_size) {
    throw std::runtime_error("debug packet length mismatch");
}
```

Crie payload, valide hash e retorne `{command, request_id, std::move(payload)}`.

## Testes/Debug
O teste altera o último byte (`^=0xFF`) e espera checksum failure. Coloque breakpoint no `actual_hash != expected_hash` e compare ambos. O teste truncado `{1,2,3}` deve falhar antes de qualquer `read_u32`.

## Benchmark
O benchmark faz 300 mil encode+decode de payload de 64 bytes. Registre packets/s; depois compare quando adicionar CRC32C/SIMD ou transporte real, mantendo o mesmo payload.
