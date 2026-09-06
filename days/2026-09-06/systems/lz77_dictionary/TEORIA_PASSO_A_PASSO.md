# Teoria passo a passo — Systems — LZ77 dictionary codec (CHLZ7)

## 1. O quê estamos construindo

Um codec didático LZ77 com janela deslizante de 32 KiB, match mínimo 3 e máximo 255, formato próprio `CHLZ7` e round-trip `encode_lz77` ↔ `decode_lz77`. Não é DEFLATE completo: aqui o foco é o dicionário e a cópia por `(offset, length)`.

API em `starter/lz77.hpp`:

```text
find_longest_match(data, pos, match) → bool + LZ77Match{offset, length}
encode_lz77(input, out)              → header CHLZ7 + tokens
decode_lz77(input, out)              → expandir literais e matches
```

Constantes do laboratório:

| Símbolo | Valor | Papel |
|---------|------:|-------|
| `LZ77_WINDOW_SIZE` | 32768 | alcance máximo do offset |
| `LZ77_MIN_MATCH` | 3 | match mais curto que vale a pena |
| `LZ77_MAX_MATCH` | 255 | cabe em `uint8_t length` |
| Magic | `CHLZ7` | 5 bytes ASCII no header |

## 2. Como funciona a ideia LZ77

Em vez de repetir bytes, apontamos para uma ocorrência anterior dentro da janela:

```text
entrada:  A B C A B C A B C D
posição:  0 1 2 3 4 5 6 7 8 9

em pos=3 ("ABC..."):
  melhor match = offset=3, length=6  → "ABCABC"
  resto: literal 'D'
```

`offset` conta **quantos bytes atrás** do cursor atual começa a cópia. `length` é quantos bytes copiar. O decoder reconstrói empurrando bytes no buffer de saída e, para matches, lendo de `out[out.size() - offset]`.

### Diagrama janela × lookahead

```text
[........ história ........][pos .... fim]
 ^ window_start              ^ cursor
 |←──── ≤ 32768 bytes ────→|
```

`COMP-LZ77-01` exige que `window_start = max(0, pos - LZ77_WINDOW_SIZE)`. Buscar antes disso é bug (offset > 32 KiB) e quebra o contrato do teste.

## 3. Por quê MIN_MATCH = 3

No formato deste lab, um match ocupa 4 bytes de token (`0x01` + offset LE16 + length), enquanto um literal ocupa 2 (`0x00` + byte). Match de length 1 ou 2 quase nunca comprime; length ≥ 3 já pode empatar ou ganhar. Por isso `COMP-LZ77-02` só aceita `len >= LZ77_MIN_MATCH`.

## 4. Trace byte a byte — `find_longest_match`

Entrada de teste: `"ABCABCABCD"` (10 bytes). Em `pos = 3`:

```text
data = [A B C A B C A B C D]
        0 1 2 3 4 5 6 7 8 9
              ^pos

candidatos start ∈ [0, 3):
  start=0: data[0..] vs data[3..] → A=A,B=B,C=C,A=A,B=B,C=C → len=6, off=3
  start=1: B vs A → len=0
  start=2: C vs A → len=0

melhor: offset=3, length=6  (≥ MIN_MATCH) → return true
```

Se o melhor `len` for 1 ou 2, a função zera `match` e retorna `false` — o encoder emite literal.

### Trace com janela limitada (COMP-LZ77-01)

Suponha `pos = 40000` e um padrão idêntico em `pos - 40000`. Sem clipe, o offset seria 40000 (> 32768). Com clipe:

```text
window_start = 40000 - 32768 = 7232
start ∈ [7232, 40000)
```

A ocorrência em 0 **não** é candidata. Isso espelha zlib/gzip: a janela deslizante é memória limitada.

## 5. Formato binário CHLZ7 (COMP-LZ77-03)

```text
offset | tamanho | campo
-------|---------|---------------------------
0      | 5       | magic "CHLZ7"
5      | 4       | uncompressed_len u32 LE
9      | …       | stream de tokens
```

Tokens:

| Tag | Bytes seguintes | Significado |
|-----|-----------------|-------------|
| `0x00` | 1 byte literal | emitir esse byte |
| `0x01` | offset u16 LE + length u8 | copiar `length` bytes de `out[size-offset]` |

### Encode trace — `"ABCABCABCD"`

Passos mentais (após header):

```text
pos=0: sem match → 00 'A'
pos=1: sem match → 00 'B'
pos=2: sem match → 00 'C'
pos=3: match off=3 len=6 → 01 03 00 06
pos=9: sem match → 00 'D'
```

Header: magic + `len=10` = `0A 00 00 00`. Stream começa no byte 9.

Hex aproximado do arquivo:

```text
43 48 4C 5A 37   # C H L Z 7
0A 00 00 00       # length 10 LE
00 41             # lit 'A'
00 42             # lit 'B'
00 43             # lit 'C'
01 03 00 06       # match offset=3 length=6
00 44             # lit 'D'
```

## 6. Decode — janela deslizante na saída (COMP-LZ77-04)

O decoder **não** guarda um buffer circular separado: a própria `out` é o histórico.

```text
tag 0x00: out.push(byte)
tag 0x01:
  start = out.size() - offset
  para i em 0..length-1:
    out.push(out[start + i])   // pode overlap se length > offset (run-length via match)
```

### Trace overlap (run)

```text
out = [A]
match offset=1 length=4  → copia A,A,A,A
out = [A A A A A]
```

Isso é correto e comum em LZ77: `start + i` avança sobre bytes **já escritos nesta expansão**. Loop byte a byte (como no gabarito) é obrigatório; `memcpy` de região sobreposta é UB / resultado errado.

### Validações que o decode deve falhar

| Condição | Por quê |
|----------|---------|
| magic ≠ CHLZ7 | arquivo errado / corrompido |
| `offset == 0` | aponta “antes” do início |
| `offset > out.size()` | aponta além do histórico |
| tag desconhecida | stream inválido |
| `out.size() != len` no fim | truncamento ou overflow |

O teste corrompe `enc[0] = 'X'` e exige `decode_lz77` → `false`.

## 7. Algoritmo de busca — complexidade e trade-offs

Busca ingenua (gabarito):

```text
para cada start na janela:
  comparar byte a byte até mismatch ou MAX_MATCH
  guardar melhor (len, off)
```

Complexidade pior caso ≈ `O(n · W · M)` com `W=32768`, `M=255`. Aceitável no lab; produção usa hash chains / patricia / suffix arrays (zlib, zstd, LZ4).

`max_len = min(LZ77_MAX_MATCH, data.size() - pos)` — sem isso, leitura past-the-end.

## 8. Invariantes do módulo

1. Offset sempre em `[1, min(pos, LZ77_WINDOW_SIZE)]` quando há match.
2. Length em `[LZ77_MIN_MATCH, LZ77_MAX_MATCH]`.
3. Header `uncompressed_len` bate com bytes produzidos no decode.
4. Encode sempre retorna `true` neste lab (entrada finita); decode pode falhar.
5. Round-trip: `decode(encode(x)) == x` para qualquer `x` finito.

## 9. Bugs clássicos de estudante

1. **Janela sem clipe** — `start` de 0 sempre (`COMP-LZ77-01`).
2. **Aceitar len < 3** — tokens maiores que literais (`COMP-LZ77-02`).
3. **Offset big-endian** — testes em LE; `03 00` ≠ `00 03` para offset 3.
4. **`memcpy` em match overlapping** — run “AAAA…” quebra.
5. **Magic com `\0`** — `CHLZ7_MAGIC` tem 6 chars no array; gravar só 5 bytes.
6. **Avançar `pos` de 1 após match** — deve ser `pos += length`.
7. **Não reservar / não checar `out.size() == len`** — aceita stream truncado.
8. **offset em signed** — use `uint16_t`; offset 0 é inválido no decode.

## 10. Relação com DEFLATE / zlib

| Este lab (CHLZ7) | DEFLATE (RFC 1951) |
|------------------|--------------------|
| tokens explícitos 0x00/0x01 | literais/lengths Huffman + distances |
| offset u16 cru | códigos de distância + bits extras |
| length u8 | length codes 257–285 |
| sem BFINAL/BTYPE | blocos stored/fixed/dynamic |

O módulo `deflate_blocks` do mesmo dia empacota bits e Huffman; aqui você isola o dicionário.

## 11. Passo a passo de estudo

1. Leia constantes e `LZ77Match` em `starter/lz77.hpp`.
2. Implemente `find_longest_match` (`COMP-LZ77-01`, `COMP-LZ77-02`).
3. Implemente `encode_lz77` (`COMP-LZ77-03`).
4. Implemente `decode_lz77` (`COMP-LZ77-04`).
5. Rode `test_lz77` até `OK lz77`.
6. Só então compare com `solutions/lz77.cpp`.

## 12. Como saber se está correto

- `find_longest_match` em `"ABCABCABCD"` @3 → length ≥ 3, offset ≤ 32768.
- Round-trip idêntico ao input.
- Magic corrompido → decode false.
- Manual: header 9 bytes + tokens batem com o hex da seção 5.

## 13. Perguntas de verificação

1. Por que `window_start` usa `pos > LZ77_WINDOW_SIZE` e não `>=`?
2. Qual o tamanho mínimo de um arquivo CHLZ7 vazio (len=0)?
3. Por que o loop de cópia no decode usa `out[start + i]` e não `out[out.size() - offset]` a cada iteração?
4. O que acontece se `MAX_MATCH` fosse 258 como no DEFLATE, mas o campo length continuar `uint8_t`?

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?
Forçar o aluno a ver compressão como **referências em memória**, não como “caixa preta gzip”.

### Por quê estas invariantes?
Cada `TODO [COMP-LZ77-0x]` trava uma falha silenciosa: janela infinita, match curto caro, header frouxo, cópia overlapping quebrada.

### Por quê medir e portar?
O lab isola o dicionário; `projects/chris-compress` pode reutilizar a lógica como estágio antes de Huffman/DEFLATE.
