# Teoria passo a passo — Tooling — PNG IDAT pipeline

## 1. O que estamos construindo

Encoder/decoder PNG **mínimo**: grayscale 8-bit, filtro None, um IDAT com zlib stored.

```text
assinatura 8 B
  IHDR chunk  (13 B de data)
  IDAT chunk  (zlib(scanlines filtradas))
  IEND chunk  (data vazia)
```

API real (`png.hpp`): `png_chunk_crc`, `png_chunk`, `build_ihdr`, `filter_none_scanlines`, `encode_png`, `decode_png`. Zlib mínimo: `zlib_min_compress` / `zlib_min_decompress`. CRC: mesmo IEEE de gzip.

## 2. Por que PNG depois de zlib

PNG **não** inventa compressão nova: IDAT carrega um stream zlib. O que PNG adiciona é framing de chunks (length, type, CRC) + filtro por scanline + IHDR. Este lab fecha o ciclo container→imagem.

```text
pixels → filter None → zlib → IDAT data
                      ↑
              (mesmo Adler do lab zlib)
```

---

## 3. Chunk PNG e CRC (COMP-PNG-01)

### O quê

Todo chunk:

```text
| length u32 BE | type 4 ASCII | data[length] | CRC u32 BE |
```

CRC cobre **type + data**, nunca o length.

### Como

```text
png_chunk_crc(type, data):
  buf = type[4] || data
  return crc32(buf)

png_chunk(type, data):
  out = BE32(len) || type || data || BE32(crc)
```

### Por quê

Incluir o type no CRC impede trocar `IDAT` por `IEND` sem invalidar o checksum. Length fica de fora para o parser poder ler o tamanho antes de saber se o CRC confere.

### Trace — chunk `IEND` vazio

```text
type = "IEND", data = []
CRC32("IEND") = 0xAE426082   // valor canônico

bytes do chunk (12 B):
  00 00 00 00           length = 0
  49 45 4E 44           I E N D
  AE 42 60 82           CRC BE
```

### Trace — layout genérico

```text
offset 0: length BE
offset 4: type
offset 8: data...
offset 8+len: CRC BE
tamanho total = 12 + len
```

Para IHDR com 13 bytes de data: chunk = **25** bytes (`4+4+13+4`).

### Invariantes

- Length é BE; CRC é BE.
- `png_chunk_crc` e o CRC gravado no ficheiro devem coincidir no decode.
- Type é exatamente 4 bytes (não string C com NUL extra no CRC).

### Bugs comuns

| Sintoma | Causa | Depuração |
|---------|-------|-----------|
| `png chunk crc mismatch` | CRC só sobre data | Inclua type |
| Chunk curto | Esqueceu 4 B do CRC | `size == 12+len` |
| CRC “quase” | Endian LE no trailer | Escreva BE como Adler zlib |

---

## 4. IHDR 13 bytes (COMP-PNG-02)

### O quê

Primeiro chunk obrigatório. Data layout (todos BE onde aplicável):

```text
offset | tam | campo
-------|-----|--------
0      | 4   | width (u32 BE)
4      | 4   | height (u32 BE)
8      | 1   | bit_depth
9      | 1   | color_type
10     | 1   | compression (0 = zlib/deflate)
11     | 1   | filter method (0 = adaptive standard)
12     | 1   | interlace (0 = none)
```

Neste lab: `bit_depth=8`, `color_type=0` (grayscale), demais zeros.

### Como (`build_ihdr`)

Empacota `PngImage` nesses 13 bytes — **sem** encapsular em chunk ainda (`encode_png` chama `png_chunk("IHDR", …)`).

### Por quê

Separar “data IHDR” de “chunk IHDR” permite testar o layout isoladamente (teste checa `ihdr.size()==13`, `ihdr[8]==8`, `ihdr[9]==0`).

### Trace — imagem 3×2 grayscale

```text
width=3, height=2, bit_depth=8, color_type=0

IHDR data (13 B hex):
  00 00 00 03   width
  00 00 00 02   height
  08            bit_depth
  00            color_type
  00 00 00      compression, filter, interlace

CRC do chunk (type+data) = 0xB81F39C6
chunk completo = 25 bytes
```

### Invariantes

- Width/height ≠ 0 em PNG real; o lab usa 3×2 nos testes.
- `color_type=0` ⇒ 1 byte por pixel; `row_bytes = width`.

### Bugs comuns

- Width/height little-endian (hábito x86) → viewers mostram dimensões absurdas.
- `color_type=2` (RGB) com buffer grayscale → tamanho de linha errado.
- Escrever 12 ou 14 bytes → decode rejeita `len == 13`.

---

## 5. Filtro None por scanline (COMP-PNG-03)

### O quê

Antes de zlib, cada linha vira: **1 byte de tipo de filtro** + pixels da linha.

Filtro `0` = None (cópia literal). Outros (Sub, Up, Average, Paeth) ficam fora do milestone.

### Como (`filter_none_scanlines`)

```text
row_bytes = width          // grayscale 8-bit
raw.size  = (row_bytes + 1) * height
para y in 0..height-1:
  raw[y * (row_bytes+1)] = 0
  copiar pixels[y*row_bytes ..] para raw[...+1]
```

### Por quê

O decoder PNG **sempre** espera o byte de filtro. Omitir encolhe o stream e desalinha todas as linhas — sintoma clássico “imagem diagonalada”.

### Trace — pixels `{10,20,30, 40,50,60}` (3×2)

```text
linha 0: 00 | 0A 14 1E
linha 1: 00 | 28 32 3C
raw length = 4 * 2 = 8
raw[0]==0, raw[1]==10
```

### Invariantes

- `filtered.size() == (width+1)*height`.
- Primeiro byte de cada stride é 0.
- Decode rejeita filter ≠ 0 neste lab.

### Bugs comuns

| Sintoma | Causa |
|---------|-------|
| size errado | Esqueceu `+1` por linha |
| pixels deslocados | Escreveu filter no fim da linha |
| decode “only filter none” | Encoder usou outro tipo |

---

## 6. Encode / decode completo (COMP-PNG-04)

### O quê

Assinatura + IHDR + IDAT(zlib(filtered)) + IEND. Decode: validar signature, iterar chunks, juntar IDATs, inflate zlib, remover filtros.

### Como — signature

```text
89 50 4E 47 0D 0A 1A 0A
= 137, 'P', 'N', 'G', CR, LF, EOF, LF
```

### Como — encode_png

```text
out = signature
out += png_chunk("IHDR", build_ihdr(img))
filtered = filter_none_scanlines(img)
out += png_chunk("IDAT", zlib_min_compress(filtered))
out += png_chunk("IEND", {})
```

`zlib_min_compress`: header `78 01` + stored + Adler BE (mesmo padrão do lab zlib).

### Como — decode_png

```text
checar signature
pos = 8
enquanto couber chunk:
  len = BE32; type = 4 chars; data; crc = BE32
  se png_chunk_crc(type,data) != crc → erro
  IHDR → width/height/depth/color
  IDAT → append data (pode haver vários; lab usa um)
  IEND → break
raw = zlib_min_decompress(idat)
por linha: filter==0; copiar pixels
```

### Por quê

Round-trip sem libpng prova que você entende o formato. Viewers reais (IrfanView, browsers) abrem o ficheiro se IHDR+IDAT+CRC estiverem corretos — mesmo com stored (ficheiro maior).

### Trace — fluxo 3×2

```text
pixels 6 B
  → filtered 8 B
  → zlib_min (78 01 | stored | Adler)
  → IDAT chunk (12 + zlib_len)
arquivo ≈ 8 + 25 + IDAT + 12 bytes
decode → pixels idênticos
```

### Invariantes

- Signature exata nos 8 primeiros bytes.
- CRC de cada chunk verificado antes de confiar no data.
- Só `color_type=0` / filter 0 neste subset.

### Bugs comuns

- Concatenar IDAT errado (só o primeiro) — aqui há um, mas o loop já prepara N.
- Não avançar `pos = crc_off + 4` → loop infinito / truncate.
- Tratar type como `std::string` com `\0` no CRC.

---

## 7. Camadas empilhadas

```text
PNG file
 └─ chunks (length/type/data/CRC)     COMP-PNG-01
     ├─ IHDR 13 B                     COMP-PNG-02
     ├─ IDAT
     │   └─ zlib
     │       └─ filtered scanlines    COMP-PNG-03
     │           └─ pixels
     └─ IEND
encode/decode orquestra tudo          COMP-PNG-04
```

## 8. Complexidade

- Chunk CRC: O(len) por chunk.
- Filter None: O(width×height).
- Encode/decode: O(n) + inflate stored O(n).

## 9. Comparação com produção

| Lab | libpng / browsers |
|-----|-------------------|
| 1 IDAT stored | vários IDAT, Huffman |
| filter 0 only | filters 0–4 |
| grayscale 8 | RGB/RGBA, 16-bit, Adam7 |

O framing de chunks e a regra CRC(type+data) são idênticos.

## 10. Passo a passo guiado

1. `COMP-PNG-01` — CRC e `png_chunk`.
2. `COMP-PNG-02` — `build_ihdr` 13 B.
3. `COMP-PNG-03` — filter None.
4. `COMP-PNG-04` — `encode_png` / `decode_png`.
5. `ctest` → `OK png idat pipeline`.

## 11. Como saber se está correto

- IHDR size 13; chunk IHDR size 25.
- Filtered `[0,10,…]` para o vetor de teste.
- Signature `137,80,…`; pixels round-trip iguais.
- Opcional: gravar `.png` e abrir num viewer.

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?

Ligar checksums/containers do dia a um formato de imagem que você já usa — feedback visual imediato.

### Por quê estas invariantes?

CRC do type, IHDR BE e byte de filtro são as três falhas mais comuns em encoders “quase certos”.

### Por quê portar?

`projects/chris-compress` / ferramentas de dump podem reutilizar chunk CRC e zlib_min para extrair IDAT em forense leve.
