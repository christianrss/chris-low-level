# Teoria passo a passo — Tooling — zlib/gzip containers

## 1. O que estamos construindo

Dois envelopes sobre o mesmo payload DEFLATE (neste lab: **stored**, BTYPE=00):

| Container | RFC | Checksum | Endian do trailer |
|-----------|-----|----------|-------------------|
| zlib | 1950 | Adler-32 | big-endian |
| gzip | 1952 | CRC-32 + ISIZE | little-endian |

API real do starter: `adler32`, `crc32`, `zlib_compress` / `zlib_blob_from_packet` / `zlib_decompress`, `gzip_compress` / `gzip_decompress`. O DEFLATE stored já está em `deflate_stored.hpp` (`encode_stored_block` / `decode_stored_blocks`).

## 2. Por que containers antes de Huffman dinâmico

Sem header/trailer corretos, um decoder de produção rejeita o blob mesmo com bits DEFLATE perfeitos. Este módulo isola **empacotamento e integridade** — o mesmo padrão de PNG IDAT, HTTP Content-Encoding e arquivos `.gz`.

```text
plaintext
   │
   ├─► zlib:  CMF FLG | DEFLATE | Adler32 BE
   └─► gzip:  1F 8B … | DEFLATE | CRC32 LE | ISIZE LE
```

---

## 3. Adler-32 (COMP-ZLIB-01)

### O quê

Checksum de 32 bits: dois acumuladores `s1` e `s2` módulo **65521** (maior primo < 2^16). Resultado `(s2 << 16) | s1`.

### Como

```text
s1 = 1
s2 = 0
para cada byte b:
  s1 = (s1 + b) % 65521
  s2 = (s2 + s1) % 65521
return (s2 << 16) | s1
```

Contrato: `std::uint32_t adler32(const std::uint8_t* data, std::size_t len)` e overload de `vector`.

### Por quê

Mais barato que CRC-32 (só somas). zlib escolheu Adler para o trailer do stream; gzip escolheu CRC. Confundir os dois quebra interoperabilidade.

### Trace manual — string `"Wikipedia"`

Bytes ASCII (9): `W i k i p e d i a` = 87, 105, 107, 105, 112, 101, 100, 105, 97.

```text
byte   s1     s2
W 87   88     88
i 105  193    281
k 107  300    581
i 105  405    986
p 112  517    1503
e 101  618    2121
d 100  718    2839
i 105  823    3662
a 97   920    4582

s1 = 0x0398, s2 = 0x11E6
Adler = (0x11E6 << 16) | 0x0398 = 0x11E60398
```

O teste `PEDAGOGY-TEST: COMP-ZLIB-01` exige exatamente `0x11e60398u`.

### Invariantes

- `s1` começa em **1**, não 0 (RFC 1950).
- Módulo **65521**, não 65536.
- Adler cobre o **plaintext**, nunca o header CMF/FLG.

### Bugs comuns

| Sintoma | Causa | Depuração |
|---------|-------|-----------|
| Valor ≠ `0x11E60398` | `s1` iniciou em 0 | Trace passo a passo acima |
| zlib round-trip falha | Adler LE em vez de BE | Hexdump dos 4 últimos bytes |
| Overflow estranho | Esqueceu `% 65521` | Compare com `zlib.adler32` em Python |

---

## 4. Header zlib CMF/FLG (COMP-ZLIB-02)

### O quê

Dois bytes antes do DEFLATE:

| Byte | Nome | Neste lab |
|------|------|-----------|
| CMF | compression method/flags | `0x78` (CM=8 deflate, CINFO=7 → janela 32 KiB) |
| FLG | flags | `0x01` (FCHECK; FDICT=0, FLEVEL baixo) |

### Como

```text
check = (CMF << 8) + FLG
check % 31 == 0   // obrigatório
```

`zlib_compress` preenche `ZlibPacket{cmf, flg, deflate_raw, adler_checksum}`:

1. `cmf=0x78`, `flg=0x01` (já satisfaz `% 31 == 0`);
2. `deflate_raw = encode_stored_block(data, true)`;
3. `adler_checksum = adler32(data)`.

`zlib_blob_from_packet` serializa: `[CMF][FLG][deflate…][Adler BE]`.

### Por quê

O FCHECK de 5 bits força `(CMF<<8)+FLG` múltiplo de 31 — detecção imediata de header truncado ou endian trocado sem olhar o Adler.

### Trace — payload `{'z','l','i','b'}`

```text
CMF=0x78 FLG=0x01
(0x7801) % 31 = 0  ✓
Adler32("zlib") calculado sobre 4 bytes plaintext
blob = 78 01 | <stored block> | AA BB CC DD (Adler BE)
```

### Invariantes

- `(cmf & 0x0F) == 8` (só deflate).
- Sem dicionário preset (`FLG` bit 5 = 0).
- Adler no trailer é **big-endian**.

### Bugs comuns

- Escolher FLG que não passa em `% 31` → decoder rejeita antes do inflate.
- Empurrar Adler little-endian (hábito de gzip/x86).
- Esquecer `final_block=true` no stored → stream incompleto.

---

## 5. Decompress zlib (COMP-ZLIB-03)

### O quê

Inverso de COMP-ZLIB-02: validar header, cortar trailer, inflate stored, conferir Adler.

### Como (`zlib_decompress`)

```text
se size < 6 → erro
ler CMF, FLG; checar % 31 e CM==8
adler = blob[-4:] como u32 BE
raw = blob[2 : -4]
data = decode_stored_blocks(raw)
se adler32(data) != adler → erro
return data
```

### Por quê

Ordem importa: só após confirmar tamanho mínimo e header é seguro fatiar `end-4`. Validar Adler **depois** do inflate — o trailer protege plaintext, não o bitstream.

### Invariantes

- Blob mínimo 6 bytes (2 header + 0 deflate + 4 Adler) na prática stored precisa de mais; o lab usa `< 6` como guarda grossa.
- Mismatch Adler → `runtime_error`, nunca devolver dados “quase certos”.

### Bugs comuns

| Sintoma | Causa |
|---------|-------|
| `adler32 mismatch` | Endian do trailer invertido na leitura |
| `only deflate method` | CM ≠ 8 |
| Crash em `end-4` | Não checou `size < 6` |

---

## 6. CRC-32 IEEE + gzip (COMP-ZLIB-04)

### O quê

CRC-32 (polinômio refletido `0xEDB88320`), init/xor `0xFFFFFFFF`. gzip: magic `1F 8B`, método 8, header mínimo 10 bytes, trailer CRC32 LE + ISIZE LE (tamanho plaintext mod 2^32).

### Como — tabela CRC

```text
para i in 0..255:
  c = i
  8 vezes: c = (c&1) ? (0xEDB88320 ^ (c>>1)) : (c>>1)
  table[i] = c

crc = 0xFFFFFFFF
para cada byte b: crc = table[(crc ^ b) & 0xFF] ^ (crc >> 8)
return crc ^ 0xFFFFFFFF
```

### Como — gzip_compress

```text
out = 1F 8B 08 00  00 00 00 00  00 03   // 10 bytes
out += encode_stored_block(data, true)
out += crc32(data) em LE
out += data.size() em LE (ISIZE)
```

### Como — gzip_decompress

```text
magic 1F 8B; size >= 18
pos = 10  // lab: sem FNAME/FEXTRA
crc  = u32 LE em blob[-8:-4]
isize = u32 LE em blob[-4:]
data = decode_stored_blocks(blob[10:-8])
checar crc32(data) e isize
```

### Por quê

gzip e zlib **não** são intercambiáveis: magic diferente, checksum diferente, endian diferente. Um gunzip real falha se você embutir Adler no lugar do CRC.

### Trace CRC — ideia

CRC cobre plaintext. No PNG (próximo módulo) o mesmo `crc32` cobre **type+data** do chunk; em gzip cobre só os bytes descomprimidos.

### Invariantes

- Header fixo do lab: flags=0, mtime=0, xfl=0, os=3 (Unix).
- CRC e ISIZE little-endian.
- ISIZE é `size & 0xFFFFFFFF`, não o tamanho do blob comprimido.

### Bugs comuns

- Polinômio `0x04C11DB7` sem reflexão (CRC “normal” vs reflected).
- Esquecer XOR final `0xFFFFFFFF`.
- Ler CRC como big-endian (mistura com zlib/PNG).

---

## 7. Relação zlib ↔ gzip ↔ PNG

```text
mesmo DEFLATE stored
   │
   ├─ zlib trailer: Adler BE     ← este lab
   ├─ gzip trailer: CRC LE+ISIZE ← este lab
   └─ PNG IDAT: zlib dentro de chunk com CRC do chunk ← png_idat_pipeline
```

## 8. Complexidade

- Adler/CRC: O(n) no plaintext.
- Wrap/unwrap: O(n) cópia + inflate stored O(n).
- Tabela CRC: O(1) setup (256×8).

## 9. Comparação com produção

| Lab | zlib/gzip reais |
|-----|-----------------|
| só stored | Huffman fixo/dinâmico |
| header gzip mínimo | FNAME, FEXTRA, FHCRC |
| Adler/CRC à mão | `zlib`/`libdeflate` |

O pipeline header→deflate→trailer é idêntico ao industrial.

## 10. Passo a passo guiado

1. `COMP-ZLIB-01` — Adler em `adler32.cpp`; confira `0x11E60398`.
2. `COMP-ZLIB-02` — `zlib_compress` + `zlib_blob_from_packet`.
3. `COMP-ZLIB-03` — `zlib_decompress` com validação.
4. `COMP-ZLIB-04` — `crc32` + gzip wrap/unwrap.
5. `ctest` Release deve imprimir `OK zlib gzip containers`.

## 11. Como saber se está correto

- Adler(`Wikipedia`) = `0x11E60398`.
- zlib: CMF `0x78`, `(CMF<<8)+FLG` % 31 == 0, round-trip `zlib`.
- gzip: magic `1F 8B`, round-trip idêntico.

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?

Ler e escrever containers reais sem biblioteca opaca — skill de forense, rede e embed.

### Por quê estas invariantes?

Cada `TODO [ID]` protege uma propriedade que falha silenciosamente (endian, módulo, magic).

### Por quê portar para `projects/chris-compress`?

O lab isola aprendizado; o CLI cumulativo reutiliza zlib wrap em pipeline RLE→deflate.
