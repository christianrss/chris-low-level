# Resolução guiada — Tooling — PNG IDAT pipeline

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `COMP-PNG-01` | `starter/png.cpp` | `png_chunk_crc`, `png_chunk` |
| `COMP-PNG-02` | `starter/png.cpp` | `build_ihdr` |
| `COMP-PNG-03` | `starter/png.cpp` | `filter_none_scanlines` |
| `COMP-PNG-04` | `starter/png.cpp` | `encode_png`, `decode_png` |

Helpers já prontos: `crc32` (`crc32.hpp`), `zlib_min_compress` / `zlib_min_decompress` (`zlib_min.hpp`).

Cada ID: `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` no gabarito, `PEDAGOGY-TEST: ID` em `starter/test_png.cpp`.

> Trabalhe em `days/2026-09-06/tooling/png_idat_pipeline/starter/`. Não copie `solutions/` no início.

---

## 0. Baseline — build e FAIL esperado

```powershell
cd E:\Aulas\low-level-unified-portfolio
cmake -S days/2026-09-06/tooling/png_idat_pipeline/starter -B days/2026-09-06/tooling/png_idat_pipeline/starter/build -A x64
cmake --build days/2026-09-06/tooling/png_idat_pipeline/starter/build --config Release
ctest --test-dir days/2026-09-06/tooling/png_idat_pipeline/starter/build -C Release --output-on-failure
```

Build OK; testes **falham** (funções retornam `{}` / `0`). Baseline confirmado.

Inclua no topo de `png.cpp` (já no starter):

```cpp
#include "png.hpp"
#include "zlib_min.hpp"
#include <cstring>
#include <stdexcept>
```

Você pode adicionar helpers locais `kSignature` e `read_be32` quando chegar em COMP-PNG-04 (como no gabarito).

---

## Exercício Fácil — `COMP-PNG-01` chunk + CRC

### 1. O problema

```cpp
std::uint32_t png_chunk_crc(const char* type, const std::vector<std::uint8_t>& data) {
    // TODO [COMP-PNG-01]: CRC32 sobre type+data
    return 0;
}

std::vector<std::uint8_t> png_chunk(const char* type, const std::vector<std::uint8_t>& data) {
    // TODO [COMP-PNG-01]: length BE + type + data + crc BE
    return {};
}
```

### 2. O algoritmo

1. Buffer = 4 bytes do type + data.
2. `crc32` IEEE (já implementado no starter deste módulo).
3. Chunk = `BE32(len) || type || data || BE32(crc)`.

### 3. Escreva o código

```cpp
std::uint32_t png_chunk_crc(const char* type, const std::vector<std::uint8_t>& data) {
    std::vector<std::uint8_t> buf(4 + data.size());
    std::memcpy(buf.data(), type, 4);
    if (!data.empty()) {
        std::memcpy(buf.data() + 4, data.data(), data.size());
    }
    return crc32(buf.data(), buf.size());
}

std::vector<std::uint8_t> png_chunk(const char* type, const std::vector<std::uint8_t>& data) {
    std::vector<std::uint8_t> out(4 + 4 + data.size() + 4);
    const auto len = static_cast<std::uint32_t>(data.size());
    out[0] = static_cast<std::uint8_t>((len >> 24) & 0xFFu);
    out[1] = static_cast<std::uint8_t>((len >> 16) & 0xFFu);
    out[2] = static_cast<std::uint8_t>((len >> 8) & 0xFFu);
    out[3] = static_cast<std::uint8_t>(len & 0xFFu);
    std::memcpy(out.data() + 4, type, 4);
    if (!data.empty()) {
        std::memcpy(out.data() + 8, data.data(), data.size());
    }
    const auto c = png_chunk_crc(type, data);
    const std::size_t o = 8 + data.size();
    out[o + 0] = static_cast<std::uint8_t>((c >> 24) & 0xFFu);
    out[o + 1] = static_cast<std::uint8_t>((c >> 16) & 0xFFu);
    out[o + 2] = static_cast<std::uint8_t>((c >> 8) & 0xFFu);
    out[o + 3] = static_cast<std::uint8_t>(c & 0xFFu);
    return out;
}
```

Lembre `#include "crc32.hpp"` se o starter não o puxar via outro header — no gabarito entra por `png.cpp` com `#include "crc32.hpp"`.

Adicione no `png.cpp` do starter:

```cpp
#include "crc32.hpp"
```

### 4. Entenda linha por linha

- `memcpy(type, 4)`: type PNG é binário de 4 bytes, não `strlen`.
- Length **não** entra no CRC.
- CRC e length em BE: MSB no menor endereço.
- `o = 8 + data.size()`: índice do primeiro byte do CRC.

### 5. Verificação

- `IEND` vazio → CRC `0xAE426082` (TEORIA).
- `png_chunk("IHDR", ihdr13).size() == 25` após COMP-PNG-02.

### Por que funciona?

É a regra exata da spec PNG: CRC(type||data). Viewers rejeitam o ficheiro se length/CRC/endian divergirem.

---

## Exercício Médio A — `COMP-PNG-02` IHDR

### 1. O problema

```cpp
std::vector<std::uint8_t> build_ihdr(const PngImage& spec) {
    // TODO [COMP-PNG-02]: 13 bytes IHDR (width/height BE, bit depth, color type)
    return {};
}
```

### 2. Layout

Ver TEORIA §4. Width/height BE; bytes 8–12 = depth, color, 0, 0, 0.

### 3. Escreva o código

```cpp
std::vector<std::uint8_t> build_ihdr(const PngImage& spec) {
    std::vector<std::uint8_t> data(13);
    data[0] = static_cast<std::uint8_t>((spec.width >> 24) & 0xFFu);
    data[1] = static_cast<std::uint8_t>((spec.width >> 16) & 0xFFu);
    data[2] = static_cast<std::uint8_t>((spec.width >> 8) & 0xFFu);
    data[3] = static_cast<std::uint8_t>(spec.width & 0xFFu);
    data[4] = static_cast<std::uint8_t>((spec.height >> 24) & 0xFFu);
    data[5] = static_cast<std::uint8_t>((spec.height >> 16) & 0xFFu);
    data[6] = static_cast<std::uint8_t>((spec.height >> 8) & 0xFFu);
    data[7] = static_cast<std::uint8_t>(spec.height & 0xFFu);
    data[8] = spec.bit_depth;
    data[9] = spec.color_type;
    data[10] = 0;
    data[11] = 0;
    data[12] = 0;
    return data;
}
```

### 4. Entenda

- Índices 0–3 / 4–7: inteiros BE — mesma ordem mental do Adler zlib.
- `data[10..12]=0`: compression/filter/interlace fixos no subset.
- Não chama `png_chunk` aqui — só o payload.

### 5. Checkpoint

Para img 3×2: `size==13`, `data[8]==8`, `data[9]==0`, hex `00000003000000020800000000`.

### Por que funciona?

Testes isolam o layout antes do framing. Errar endian aqui propaga para todo decode.

---

## Exercício Médio B — `COMP-PNG-03` filter None

### 1. O problema

```cpp
std::vector<std::uint8_t> filter_none_scanlines(const PngImage& img) {
    // TODO [COMP-PNG-03]: prefix 0 por linha + pixels
    return {};
}
```

### 2. O algoritmo

Stride = `width + 1`. Byte 0 de cada stride = filtro 0; resto = cópia da linha.

### 3. Escreva o código

```cpp
std::vector<std::uint8_t> filter_none_scanlines(const PngImage& img) {
    const std::size_t row_bytes = img.width;
    std::vector<std::uint8_t> raw((row_bytes + 1) * img.height);
    for (std::uint32_t y = 0; y < img.height; ++y) {
        raw[y * (row_bytes + 1)] = 0;
        std::memcpy(raw.data() + y * (row_bytes + 1) + 1,
                    img.pixels.data() + y * row_bytes,
                    row_bytes);
    }
    return raw;
}
```

### 4. Entenda

- `row_bytes = width` só vale para `color_type=0` 8-bit (1 amostra/pixel).
- `memcpy` a partir de `+1` preserva o filter byte.
- Output alimenta `zlib_min_compress` em COMP-PNG-04.

### 5. Verificação

Pixels `{10,20,30,40,50,60}` → `filtered.size()==8`, `filtered[0]==0`, `filtered[1]==10`.

### Por que funciona?

Sem o prefixo 0, o inflater devolveria 6 bytes e o decoder leria lixo como “filtro”.

---

## Exercício Difícil — `COMP-PNG-04` encode/decode

### Helpers recomendados (anonymous namespace)

```cpp
namespace {
constexpr std::uint8_t kSignature[8] = {137, 80, 78, 71, 13, 10, 26, 10};

std::uint32_t read_be32(const std::uint8_t* p) {
    return (static_cast<std::uint32_t>(p[0]) << 24) |
           (static_cast<std::uint32_t>(p[1]) << 16) |
           (static_cast<std::uint32_t>(p[2]) << 8) |
           static_cast<std::uint32_t>(p[3]);
}
}  // namespace
```

### encode_png

```cpp
std::vector<std::uint8_t> encode_png(const PngImage& img) {
    std::vector<std::uint8_t> out(std::begin(kSignature), std::end(kSignature));
    const auto ihdr = build_ihdr(img);
    const auto ihdr_chunk = png_chunk("IHDR", ihdr);
    out.insert(out.end(), ihdr_chunk.begin(), ihdr_chunk.end());
    const auto filtered = filter_none_scanlines(img);
    const auto idat_payload = zlib_min_compress(filtered);
    const auto idat_chunk = png_chunk("IDAT", idat_payload);
    out.insert(out.end(), idat_chunk.begin(), idat_chunk.end());
    const auto iend_chunk = png_chunk("IEND", {});
    out.insert(out.end(), iend_chunk.begin(), iend_chunk.end());
    return out;
}
```

### decode_png

```cpp
PngImage decode_png(const std::vector<std::uint8_t>& blob) {
    if (blob.size() < 8 || std::memcmp(blob.data(), kSignature, 8) != 0) {
        throw std::runtime_error("bad png signature");
    }
    PngImage img;
    std::vector<std::uint8_t> idat;
    std::size_t pos = 8;
    while (pos + 12 <= blob.size()) {
        const auto len = read_be32(blob.data() + pos);
        const char* type = reinterpret_cast<const char*>(blob.data() + pos + 4);
        const auto data_off = pos + 8;
        const auto crc_off = data_off + len;
        if (crc_off + 4 > blob.size()) {
            throw std::runtime_error("truncated png chunk");
        }
        std::vector<std::uint8_t> data;
        if (len) {
            data.assign(blob.begin() + data_off, blob.begin() + data_off + len);
        }
        const auto expect = png_chunk_crc(type, data);
        const auto got = read_be32(blob.data() + crc_off);
        if (expect != got) {
            throw std::runtime_error("png chunk crc mismatch");
        }
        if (std::strncmp(type, "IHDR", 4) == 0 && len == 13) {
            img.width = read_be32(data.data());
            img.height = read_be32(data.data() + 4);
            img.bit_depth = data[8];
            img.color_type = data[9];
        } else if (std::strncmp(type, "IDAT", 4) == 0) {
            idat.insert(idat.end(), data.begin(), data.end());
        } else if (std::strncmp(type, "IEND", 4) == 0) {
            break;
        }
        pos = crc_off + 4;
    }
    const auto raw = zlib_min_decompress(idat);
    const std::size_t row_bytes = img.width;
    img.pixels.resize(row_bytes * img.height);
    for (std::uint32_t y = 0; y < img.height; ++y) {
        const auto filter = raw[y * (row_bytes + 1)];
        if (filter != 0) {
            throw std::runtime_error("only filter none supported");
        }
        std::memcpy(img.pixels.data() + y * row_bytes,
                    raw.data() + y * (row_bytes + 1) + 1,
                    row_bytes);
    }
    return img;
}
```

Precisa de `#include <cstring>` para `memcmp` / `strncmp`.

### Entenda encode

- Signature primeiro — sem ela o ficheiro não é PNG.
- Ordem IHDR → IDAT → IEND é o mínimo válido.
- `zlib_min_compress` já coloca Adler; o CRC do chunk IDAT protege o **blob zlib**, não os pixels crus.

### Entenda decode

- `pos + 12 <= size`: cabe length+type+crc mesmo com data vazia.
- CRC antes de interpretar — nunca confie em IHDR corrompido.
- IDATs concatenados: spec permite vários; inflate uma vez no fim.
- Loop de unfilter espelha COMP-PNG-03.

### Verificação final

```powershell
cmake --build days/2026-09-06/tooling/png_idat_pipeline/starter/build --config Release
ctest --test-dir days/2026-09-06/tooling/png_idat_pipeline/starter/build -C Release --output-on-failure
```

Esperado: `OK png idat pipeline`.

Opcional: escreva `blob` num `tiny.png` e abra num viewer — grayscale 3×2 é um “carimbo” minúsculo, mas valida interoperabilidade.

### Por que funciona?

Cada camada (chunk CRC → IHDR BE → filter → zlib) já foi testada; COMP-PNG-04 só as empilha na ordem da spec.

---

## Debug — mensagens típicas

| Erro | Causa provável |
|------|----------------|
| `png chunk crc mismatch` | CRC sem type; endian |
| `bad png signature` | bytes 89 50… errados |
| `only filter none supported` | filter byte ≠ 0 |
| `adler32 mismatch` (via zlib_min) | IDAT truncado / Adler |
| Round-trip pixels ≠ | `row_bytes` ou stride |

Hexdump: compare offset 8 (início IHDR chunk) com TEORIA §4.

---

## Mapa de consistência auditada

- `COMP-PNG-01` — `starter/png.cpp` → `solutions/png.cpp`
- `COMP-PNG-02` — `starter/png.cpp` → `solutions/png.cpp`
- `COMP-PNG-03` — `starter/png.cpp` → `solutions/png.cpp`
- `COMP-PNG-04` — `starter/png.cpp` → `solutions/png.cpp`

---

## Relatório de resolução

| ID | Função | Resultado |
|----|--------|-----------|
| COMP-PNG-01 | `png_chunk_crc` / `png_chunk` | IEND CRC `0xAE426082`; IHDR chunk 25 B |
| COMP-PNG-02 | `build_ihdr` | 13 B, depth 8, color 0 |
| COMP-PNG-03 | `filter_none_scanlines` | size `(w+1)*h`, `[0]=0` |
| COMP-PNG-04 | `encode_png` / `decode_png` | signature + pixels iguais |

- TODOs concluídos: ___/4
- `ctest` Release: PASS / FAIL
- Abri o PNG num viewer? Sim/Não
- Armadilha: _______________________
- Portei chunk CRC / zlib_min para `projects/`? Sim/Não — evidência: _______

### Próximo passo

Cronometre encode 8×8 em `BENCHMARK_GUIADO.md`. Depois integre com o lab zlib se ainda não fechou Adler/CRC mentalmente.
