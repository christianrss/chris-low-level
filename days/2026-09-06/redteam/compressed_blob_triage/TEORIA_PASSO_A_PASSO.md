# Teoria passo a passo — Compressed blob triage (RT-COMP)

## 1. O que estamos construindo

Um triager defensivo em Python: detectar **gzip** / **zlib** por magic bytes, validar **limites** compressed/uncompressed antes de confiar no blob, e extrair **strings ASCII** imprimíveis. APIs em `blob_triage.py`: `detect_compression_magic`, `validate_size_limits`, `extract_ascii_strings`, mais o helper `safe_inflate_preview` (já no starter).

TODOs: `RT-COMP-01` (magic), `RT-COMP-02` (limites), `RT-COMP-03` (strings).

## 2. Por que triage antes de inflate

Descomprimir sem teto é o caminho clássico de **zip bomb** e DoS em parsers. Magic bytes roteiam o decompressor certo; limites cortam alocação absurda; strings revelam artefatos (`SECRET_KEY=...`) sem executar o payload. Lab só com fixtures próprias.

## 3. Magic bytes — gzip e zlib (`RT-COMP-01`)

### O quê
`detect_compression_magic(data) → "gzip" | "zlib" | "unknown"`.

```text
offset | bytes     | kind
-------|-----------|--------
0..1   | 1F 8B     | gzip (RFC 1952)
0..1   | 78 01/5E/9C/DA | zlib (CMF/FLG típicos RFC 1950)
else / curto       | unknown
```

### Como
```text
se len(data) < 2 → unknown
se data[0]==0x1F e data[1]==0x8B → gzip
se data[0]==0x78 e data[1] ∈ {0x01,0x5E,0x9C,0xDA} → zlib
senão → unknown
```

Ordem: gzip primeiro (não há overlap com `78 xx`).

### Por quê
Evita alimentar `gzip.decompress` com zlib (e vice-versa) e permite pipelines distintos (HTTP Content-Encoding vs PNG IDAT/zlib).

### Trace manual

```text
gzip.compress(b"hello triage")[:2]  → 1f 8b
zlib.compress(b"zlib header test")[:2] → 78 9c   (nível default)
```

CMF=`0x78` (CM=8 DEFLATE, CINFO=7 → janela 32K). FLG `0x9C` = default compression + check bits.

### Invariantes
- Buffer `< 2` → `"unknown"` (sem IndexError).
- Só os quatro FLG listados contam como zlib neste lab (reduz falso positivo em `78 xx` aleatório).

### Bugs comuns
- Aceitar qualquer `78 ??`.
- Não checar `len` antes de indexar.
- Tratar `1F 8B` como zlib.

## 4. Limites seguros (`RT-COMP-02`)

### O quê
`validate_size_limits(data, max_compressed, max_uncompressed) → bool`.

### Como (espelha `solutions/blob_triage.py`)
```text
se len(data) > max_compressed → False
kind ← detect_compression_magic(data)
se kind == unknown → retornar len(data) <= max_uncompressed
tentar preview ← safe_inflate_preview(data, max_out=max_uncompressed+1)
  se exceção → False
retornar len(preview) <= max_uncompressed
```

`safe_inflate_preview` (já implementado) descomprime gzip/zlib e lança `ValueError` se `len(out) > max_out`.

### Por quê
O Caso 4 do teste: `gzip.compress(b"x"*200_000)` pode caber em `max_compressed=100_000`, mas o plaintext (200k) estoura `max_uncompressed=50_000` → deve retornar `False`. Compactado pequeno ≠ seguro.

### Trace manual — rejeição

```text
big = gzip(b"x"×200000)
len(big) pode ser < 100000 (runs longas)
inflate → 200000 > 50000 → validate False

small = gzip(b"ok")
len(small) e len(inflate) ≤ 10000 → True
```

### Invariantes
- Compressed oversized → `False` sem inflate.
- Unknown: só compara tamanho do buffer cru com `max_uncompressed`.
- Qualquer falha de decompress → `False` (não propaga exceção).

### Bugs comuns
- Validar só `len(data)` e ignorar tamanho expandido.
- Não capturar exceção do inflate.
- Usar `max_out=max_uncompressed` sem +1 e aceitar exatamente o limite de forma inconsistente — o gabarito usa `+1` e depois `<= max_uncompressed`.

## 5. Strings ASCII (`RT-COMP-03`)

### O quê
`extract_ascii_strings(data, min_len=4) → list[str]` — runs de bytes imprimíveis `\x20-\x7e` com comprimento ≥ `min_len`.

### Como
```text
pattern ← rb"[\x20-\x7e]{min_len,}"
findall → decode ascii cada match
```

### Por quê
Em triage, strings em wrappers, stubs e blobs mistos (`\x00SECRET_KEY=abc123\xff` + gzip) saltam sem precisar do inflate completo. O teste exige `"SECRET_KEY=abc123"` no resultado.

### Trace manual

```text
raw = b"\x00SECRET_KEY=abc123\xff" + gzip(...)
regex encontra SECRET_KEY=abc123 (len ≥ 4)
não exige que o gzip interno seja aberto
```

### Invariantes
- Só ASCII imprimível (espaço até `~`).
- `min_len` default 4 (filtra ruído de 1–3 chars).
- Ordem = ordem de aparição no buffer.

### Bugs comuns
- Usar `[A-Za-z0-9]` e perder `=`, `_`.
- `min_len` hardcoded 4 ignorando o parâmetro.
- Decodificar Latin-1 com bytes > 0x7e.

## 6. Fluxo mental

```text
blob
 │
 ├─ detect_compression_magic ──► gzip | zlib | unknown
 │
 ├─ validate_size_limits ──► False? parar
 │         │
 │         └─ safe_inflate_preview (helper)
 │
 └─ extract_ascii_strings ──► pistas sem executar
```

## 7. Complexidade

| Função | Tempo | Nota |
|--------|-------|------|
| magic | O(1) | 2 bytes |
| validate | O(n) inflate | pior caso descomprime |
| strings | O(n) | regex linear |

Produção: preferir streaming + `max_length` nativo; este lab usa inflate one-shot pedagógico.

## 8. Comparação com produção

| Este lab | Produção forense |
|----------|------------------|
| magic 2 B | libmagic / YARA |
| inflate completo + teto | streaming + cgroup |
| regex ASCII | + UTF-16LE strings |

## 9. Passo a passo guiado

1. `RT-COMP-01` — magic.
2. `RT-COMP-02` — limites (depende de magic + helper).
3. `RT-COMP-03` — strings.
4. `python starter/test_blob_triage.py` → `OK blob triage`.

## 10. Como saber se está correto

- Gzip fixture → `"gzip"`; zlib default → `"zlib"` e prefixo `78 9c`.
- Blob 200k×`x` gzipado rejeitado com limites (100k, 50k).
- `"SECRET_KEY=abc123"` em `extract_ascii_strings`.

## 11. Invariantes globais

- Tipos: `CompressionKind = Literal["gzip","zlib","unknown"]`.
- Não inventar magics além da lista do gabarito.
- `safe_inflate_preview` já existe — `validate_size_limits` deve chamá-lo.

## 12. Bugs comuns (checklist)

| Sintoma | Causa |
|---------|--------|
| zlib não detectado | só aceitou `9C` |
| IndexError | sem `len < 2` |
| big aceito | não checou uncompressed |
| string sumida | charset sem `=` `_` |

## 13. Por quê este módulo existe

Treinar o hábito **detectar → limitar → inspecionar** antes de confiar em blob comprimido. Cada TODO evita uma falha real de triage (formato errado, DoS, blindagem de strings).
