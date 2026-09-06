# Resolução guiada — Tooling — zlib/gzip containers

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `COMP-ZLIB-01` | `starter/adler32.cpp` | `adler32(const uint8_t*, size_t)` |
| `COMP-ZLIB-02` | `starter/zlib_wrap.cpp` | `zlib_compress`, `zlib_blob_from_packet` |
| `COMP-ZLIB-03` | `starter/zlib_wrap.cpp` | `zlib_decompress` |
| `COMP-ZLIB-04` | `starter/crc32.cpp` + `starter/gzip_wrap.cpp` | `crc32`, `gzip_compress`, `gzip_decompress` |

Cada ID existe como `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` no gabarito e `PEDAGOGY-TEST: ID` em `starter/test_zlib.cpp`.

> Trabalhe em `days/2026-09-06/tooling/zlib_gzip_containers/starter/`. Não comece copiando `solutions/`.

---

## 0. Baseline — build e FAIL esperado

```powershell
cd E:\Aulas\low-level-unified-portfolio
cmake -S days/2026-09-06/tooling/zlib_gzip_containers/starter -B days/2026-09-06/tooling/zlib_gzip_containers/starter/build -A x64
cmake --build days/2026-09-06/tooling/zlib_gzip_containers/starter/build --config Release
ctest --test-dir days/2026-09-06/tooling/zlib_gzip_containers/starter/build -C Release --output-on-failure
```

Build OK; teste **falha** (Adler retorna 0, wraps vazios). Esse é o baseline.

---

## Exercício Fácil — `COMP-ZLIB-01` Adler-32

### 1. O problema

Em `starter/adler32.cpp`:

```cpp
std::uint32_t adler32(const std::uint8_t* data, std::size_t len) {
    // TODO [COMP-ZLIB-01]: RFC1950 Adler32 com mod 65521
    return 0;
}
```

Sem Adler correto, zlib nunca fecha o round-trip.

### 2. O algoritmo

Dois somadores módulo 65521; `s1` inicia em 1.

### 3. Escreva o código

Substitua o corpo por:

```cpp
std::uint32_t adler32(const std::uint8_t* data, std::size_t len) {
    std::uint32_t s1 = 1;
    std::uint32_t s2 = 0;
    for (std::size_t i = 0; i < len; ++i) {
        s1 = (s1 + data[i]) % 65521u;
        s2 = (s2 + s1) % 65521u;
    }
    return (s2 << 16) | s1;
}
```

O overload `vector` já delega — não mexa.

### 4. Entenda linha por linha

- `s1 = 1`: offset basis do RFC (não zero).
- Loop: cada byte atualiza `s1`, depois `s2` acumula o novo `s1`.
- `% 65521u`: primo < 2^16; evita wrap silencioso em 16 bits.
- `(s2 << 16) | s1`: empacota 16+16 bits no u32 de retorno.

### 5. Verificação

No papel, `"Wikipedia"` → `0x11E60398` (trace em TEORIA). Recompile e, se quiser um teste parcial, temporariamente imprima `adler32` dessa string. O `ctest` completo ainda falha nos wraps.

### Por que funciona?

A fórmula é bit-a-bit a do RFC 1950 / zlib. Qualquer desvio no init ou no módulo quebra o vetor de teste e qualquer decoder externo.

---

## Exercício Médio A — `COMP-ZLIB-02` compress + serialize

### 1. O problema

`starter/zlib_wrap.cpp`:

```cpp
ZlibPacket zlib_compress(const std::vector<std::uint8_t>& data) {
    // TODO [COMP-ZLIB-02]: CMF/FLG + deflate stored + Adler32 BE
    return {};
}

std::vector<std::uint8_t> zlib_blob_from_packet(const ZlibPacket& pkt) {
    // TODO [COMP-ZLIB-02]: serializar CMF/FLG + deflate + Adler32 BE
    return {};
}
```

Headers: `zlib_wrap.hpp` define `ZlibPacket` com `cmf`, `flg`, `deflate_raw`, `adler_checksum`.

### 2. O algoritmo

1. Fixar `CMF=0x78`, `FLG=0x01` (já passa FCHECK `% 31`).
2. Encapsular plaintext com `encode_stored_block(data, true)`.
3. Adler sobre **plaintext** (não sobre o stored).
4. Serializar BE no blob.

### 3. Escreva `zlib_compress`

```cpp
ZlibPacket zlib_compress(const std::vector<std::uint8_t>& data) {
    ZlibPacket pkt;
    pkt.cmf = 0x78;
    pkt.flg = 0x01;
    if (((pkt.cmf << 8) + pkt.flg) % 31 != 0) {
        throw std::runtime_error("bad zlib header checksum");
    }
    pkt.deflate_raw = encode_stored_block(data, true);
    pkt.adler_checksum = adler32(data);
    return pkt;
}
```

### 4. Escreva `zlib_blob_from_packet`

```cpp
std::vector<std::uint8_t> zlib_blob_from_packet(const ZlibPacket& pkt) {
    std::vector<std::uint8_t> out{pkt.cmf, pkt.flg};
    out.insert(out.end(), pkt.deflate_raw.begin(), pkt.deflate_raw.end());
    out.push_back(static_cast<std::uint8_t>((pkt.adler_checksum >> 24) & 0xFFu));
    out.push_back(static_cast<std::uint8_t>((pkt.adler_checksum >> 16) & 0xFFu));
    out.push_back(static_cast<std::uint8_t>((pkt.adler_checksum >> 8) & 0xFFu));
    out.push_back(static_cast<std::uint8_t>(pkt.adler_checksum & 0xFFu));
    return out;
}
```

### 5. Entenda linha por linha

- `0x78 / 0x01`: CM=8, CINFO=7; FCHECK escolhido para `(0x7801)%31==0`.
- Guard `# % 31`: documenta o contrato; se alguém mudar FLG, falha cedo.
- `encode_stored_block(..., true)`: BFINAL=1 — stream de um bloco.
- Quatro `push_back` do Adler: **MSB primeiro** (network order).

### 6. Checkpoint

Recompile. Ainda falta decompress — mas `pkt.cmf == 0x78` e FCHECK já passam se o teste for quebrado em partes. Siga para COMP-ZLIB-03 antes de esperar `ctest` verde.

### Por que funciona?

Separar `ZlibPacket` (campos) de `blob` (bytes) deixa o header inspecionável nos testes sem parsear o bitstream.

---

## Exercício Médio B — `COMP-ZLIB-03` decompress

### 1. O problema

```cpp
std::vector<std::uint8_t> zlib_decompress(const std::vector<std::uint8_t>& blob) {
    // TODO [COMP-ZLIB-03]: validar header, inflar stored, checar Adler32
    return {};
}
```

### 2. O algoritmo

Validar → fatiar → inflate → conferir Adler do plaintext.

### 3. Escreva o código

```cpp
std::vector<std::uint8_t> zlib_decompress(const std::vector<std::uint8_t>& blob) {
    if (blob.size() < 6) {
        throw std::runtime_error("zlib blob too small");
    }
    const std::uint8_t cmf = blob[0];
    const std::uint8_t flg = blob[1];
    if (((cmf << 8) + flg) % 31 != 0) {
        throw std::runtime_error("zlib header check failed");
    }
    if ((cmf & 0x0Fu) != 8) {
        throw std::runtime_error("only deflate method supported");
    }
    const auto adler = (static_cast<std::uint32_t>(blob[blob.size() - 4]) << 24) |
                       (static_cast<std::uint32_t>(blob[blob.size() - 3]) << 16) |
                       (static_cast<std::uint32_t>(blob[blob.size() - 2]) << 8) |
                       static_cast<std::uint32_t>(blob[blob.size() - 1]);
    std::vector<std::uint8_t> raw(blob.begin() + 2, blob.end() - 4);
    const auto data = decode_stored_blocks(raw);
    if (adler32(data) != adler) {
        throw std::runtime_error("adler32 mismatch");
    }
    return data;
}
```

### 4. Entenda linha por linha

- `size < 6`: evita underflow ao ler trailer.
- Máscara `cmf & 0x0F`: campo CM nos 4 bits baixos.
- Adler montado com shifts 24..0: espelha a serialização BE.
- Fatia `[2, end-4)`: remove header e trailer; o miolo é DEFLATE puro.
- Comparar Adler **recalculado** com o trailer — não confiar no encoder.

### 5. Verificação

Payload `{'z','l','i','b'}`: `zlib_decompress(zlib_blob_from_packet(zlib_compress(payload))) == payload`.

### Por que funciona?

É o contrato simétrico de COMP-ZLIB-02. Qualquer endian invertido no trailer falha o `REQUIRE` de round-trip em `test_zlib.cpp`.

---

## Exercício Difícil — `COMP-ZLIB-04` CRC-32 + gzip

### Parte A — `crc32` em `starter/crc32.cpp`

#### Problema

```cpp
std::uint32_t crc32(const std::uint8_t* data, std::size_t len) {
    // TODO [COMP-ZLIB-04]: CRC32 IEEE (polinômio 0xEDB88320)
    return 0;
}
```

#### Código completo

```cpp
namespace {
std::uint32_t table[256];
bool table_init = false;

void init_table() {
    for (std::uint32_t i = 0; i < 256; ++i) {
        std::uint32_t c = i;
        for (int k = 0; k < 8; ++k) {
            c = (c & 1u) ? (0xEDB88320u ^ (c >> 1)) : (c >> 1);
        }
        table[i] = c;
    }
    table_init = true;
}
}  // namespace

std::uint32_t crc32(const std::uint8_t* data, std::size_t len) {
    if (!table_init) {
        init_table();
    }
    std::uint32_t crc = 0xFFFFFFFFu;
    for (std::size_t i = 0; i < len; ++i) {
        crc = table[(crc ^ data[i]) & 0xFFu] ^ (crc >> 8);
    }
    return crc ^ 0xFFFFFFFFu;
}
```

#### Entenda

- Polinômio **refletido** `0xEDB88320` (LSB-first), padrão PNG/gzip/Ethernet.
- Init e XOR final com `0xFFFFFFFF` — omitir um dos dois inverte o resultado.
- Tabela lazy: evita custo global se CRC nunca for chamado.

### Parte B — `gzip_compress` / `gzip_decompress` em `starter/gzip_wrap.cpp`

#### Compress

```cpp
std::vector<std::uint8_t> gzip_compress(const std::vector<std::uint8_t>& data) {
    std::vector<std::uint8_t> out{
        0x1F, 0x8B, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03};
    const auto raw = encode_stored_block(data, true);
    out.insert(out.end(), raw.begin(), raw.end());
    const auto crc = crc32(data);
    const auto isize = static_cast<std::uint32_t>(data.size());
    out.push_back(static_cast<std::uint8_t>(crc & 0xFFu));
    out.push_back(static_cast<std::uint8_t>((crc >> 8) & 0xFFu));
    out.push_back(static_cast<std::uint8_t>((crc >> 16) & 0xFFu));
    out.push_back(static_cast<std::uint8_t>((crc >> 24) & 0xFFu));
    out.push_back(static_cast<std::uint8_t>(isize & 0xFFu));
    out.push_back(static_cast<std::uint8_t>((isize >> 8) & 0xFFu));
    out.push_back(static_cast<std::uint8_t>((isize >> 16) & 0xFFu));
    out.push_back(static_cast<std::uint8_t>((isize >> 24) & 0xFFu));
    return out;
}
```

#### Decompress

```cpp
std::vector<std::uint8_t> gzip_decompress(const std::vector<std::uint8_t>& blob) {
    if (blob.size() < 18 || blob[0] != 0x1F || blob[1] != 0x8B) {
        throw std::runtime_error("not a gzip stream");
    }
    std::size_t pos = 10;
    const auto crc = static_cast<std::uint32_t>(blob[blob.size() - 8]) |
                     (static_cast<std::uint32_t>(blob[blob.size() - 7]) << 8) |
                     (static_cast<std::uint32_t>(blob[blob.size() - 6]) << 16) |
                     (static_cast<std::uint32_t>(blob[blob.size() - 5]) << 24);
    const auto isize = static_cast<std::uint32_t>(blob[blob.size() - 4]) |
                       (static_cast<std::uint32_t>(blob[blob.size() - 3]) << 8) |
                       (static_cast<std::uint32_t>(blob[blob.size() - 2]) << 16) |
                       (static_cast<std::uint32_t>(blob[blob.size() - 1]) << 24);
    std::vector<std::uint8_t> raw(blob.begin() + pos, blob.end() - 8);
    const auto data = decode_stored_blocks(raw);
    if (crc32(data) != crc) {
        throw std::runtime_error("gzip crc mismatch");
    }
    if (static_cast<std::uint32_t>(data.size()) != isize) {
        throw std::runtime_error("gzip isize mismatch");
    }
    return data;
}
```

#### Entenda

- `1F 8B 08`: magic + método deflate.
- Bytes 3–9: flags/mtime/xfl/os zerados; `os=3` (Unix) no último.
- Trailer **LE**: contraste consciente com Adler BE do zlib.
- `pos = 10`: lab sem FNAME — se flags≠0 no futuro, o parser precisa pular campos.

### Verificação final

```powershell
cmake --build days/2026-09-06/tooling/zlib_gzip_containers/starter/build --config Release
ctest --test-dir days/2026-09-06/tooling/zlib_gzip_containers/starter/build -C Release --output-on-failure
```

Saída esperada: `OK zlib gzip containers`.

### Por que funciona?

CRC IEEE + trailer LE são exatamente o que `gunzip` / `zlib.decompress(wbits=31)` esperam. O teste só checa magic e round-trip — suficiente para o subset stored.

---

## Debug — mensagens típicas

| Erro | Onde olhar |
|------|------------|
| `FAIL` na linha do Adler | `s1` init / módulo |
| `zlib header check failed` | CMF/FLG ou blob truncado |
| `adler32 mismatch` | endian do trailer |
| `not a gzip stream` | magic ou size < 18 |
| `gzip crc mismatch` | polinômio / XOR final / endian LE |

Compare hexdump do blob com a TEORIA (offsets do trailer).

---

## Mapa de consistência auditada

- `COMP-ZLIB-01` — `starter/adler32.cpp` → `solutions/adler32.cpp`
- `COMP-ZLIB-02` — `starter/zlib_wrap.cpp` → `solutions/zlib_wrap.cpp`
- `COMP-ZLIB-03` — `starter/zlib_wrap.cpp` → `solutions/zlib_wrap.cpp`
- `COMP-ZLIB-04` — `starter/crc32.cpp`, `starter/gzip_wrap.cpp` → `solutions/`

---

## Relatório de resolução

| ID | Função | Resultado |
|----|--------|-----------|
| COMP-ZLIB-01 | `adler32` | `Wikipedia` → `0x11E60398` |
| COMP-ZLIB-02 | `zlib_compress` / blob | CMF `0x78`, FCHECK ok |
| COMP-ZLIB-03 | `zlib_decompress` | round-trip `zlib` |
| COMP-ZLIB-04 | `crc32` + gzip | magic `1F 8B`, round-trip |

- TODOs concluídos: ___/4
- `ctest` Release: PASS / FAIL
- Armadilha que encontrei: _______________________
- Portei para `projects/chris-compress`? Sim/Não — evidência: _______

### Próximo passo

Refaça sem olhar esta resolução; depois meça throughput em `BENCHMARK_GUIADO.md` e avance para `tooling/png_idat_pipeline`.
