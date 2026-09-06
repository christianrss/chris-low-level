# Teoria passo a passo — Systems — DEFLATE blocks (RFC 1951 subset)

## 1. O quê estamos construindo

Um subset didático de DEFLATE: bitstream LSB-first, blocos **stored** (`BTYPE=00`) e **fixed Huffman** (`BTYPE=01`) só com literais 0–255 + EOB 256. Sem matches LZ77 neste módulo — o dicionário fica em `lz77_dictionary`.

API:

```text
BitWriter / BitReader          → COMP-DEFL-01
encode_stored_block / decode_stored_blocks → COMP-DEFL-02 / 03
build_fixed_literal_tables + encode_fixed_block → COMP-DEFL-04
decode_fixed_block             → COMP-DEFL-05
```

Arquivos: `starter/bit_stream.{hpp,cpp}`, `starter/deflate.{hpp,cpp}`.

## 2. Como o bitstream LSB-first funciona

DEFLATE empacota bits **do bit menos significativo primeiro** dentro de cada byte (RFC 1951 §3.1.1).

Exemplo do teste: escrever nibble `0b1011` e depois `0b0001`:

```text
write_bits(0b1011, 4)  → bits no buffer: b0=1, b1=1, b2=0, b3=1
write_bits(0b0001, 4)  → b4=1, b5=0, b6=0, b7=0
byte final = 0b00011011 = 0x1B
```

Trace bit a bit:

```text
bit_count  bit_buf (após write_bit)
0→1        1          (bit0 de 0b1011)
1→2        11
2→3        011
3→4        1011
4→5        1_1011     (LSB de 0b0001 = 1)
5→6        01_1011
6→7        001_1011
7→8        0001_1011 → flush 0x1B
```

`BitReader` espelha: `(byte >> (bit_pos % 8)) & 1`. Errar MSB-first quebra stored e fixed ao mesmo tempo.

### `align_byte`

Stored blocks exigem alinhamento a byte após o header de 3 bits (`BFINAL`+`BTYPE`). Bits de padding até o próximo múltiplo de 8 são descartados (writer flush; reader avança `bit_pos`).

## 3. Por quê separar BitWriter do restante

Quase todo bug em DEFLATE é de **ordem de bits**. Isolar `COMP-DEFL-01` permite provar o contrato `0x1B` antes de montar blocos. Sem isso, stored “às vezes funciona” com payloads alinhados por acaso.

## 4. Bloco stored — layout (COMP-DEFL-02 / 03)

```text
bits:  BFINAL (1) | BTYPE (2) = 00
align to byte
bytes: LEN (u16 LE) | NLEN (u16 LE) = ~LEN | payload[LEN]
```

### Trace — payload `DEFL`, `final_block=true`

```text
BFINAL=1, BTYPE=00 → bits 1,0,0  (LSB first: write 1 then 0,0)
após 3 bits: bit_count=3 → align_byte flusha byte parcial 0x01
  (bit0=1, bits1-2=0, bits3-7=0) → 0x01

LEN = 4 = 0x0004 → bytes 04 00
NLEN = ~4 = 0xFFFB → bytes FB FF
payload: 44 45 46 4C  ('D','E','F','L')
```

Hex típico:

```text
01 | 04 00 | FB FF | 44 45 46 4C
```

(O primeiro byte depende só dos 3 bits + padding; implementação com `write_bits`+`align_byte` produz esse padrão.)

### Decode stored

```text
enquanto !final:
  final ← read_bit()
  btype ← read_bits(2)   // deve ser 0
  align_byte()
  len ← read u16 LE; nlen ← read u16 LE
  assert (~len) == nlen
  ler len bytes
```

`COMP-DEFL-03` rejeita `LEN/NLEN` inconsistentes — proteção clássica de zlib contra truncamento.

## 5. Huffman fixo — tabelas RFC 1951 (COMP-DEFL-04)

Comprimentos de código para literais/lengths (288 símbolos):

| Intervalo | bits |
|-----------|-----:|
| 0–143 | 8 |
| 144–255 | 9 |
| 256 (EOB) | 7 |
| 257–285 | 8 |
| 286–287 | 8 |

Algoritmo canônico (RFC / zlib):

1. Contar `bl_count[bits]`.
2. Calcular `next_code[bits]` (prefixos canônicos).
3. Atribuir `code[sym] = next_code[len[sym]]++`.
4. **Reverter bits** do código canônico para a ordem de transmissão LSB-first do DEFLATE (`reverse_bits` no gabarito).

Sem o reverse, o encoder escreve o código “de cabeça para baixo” e o decoder bit a bit não encontra o símbolo.

### Encode fixed block

```text
write BFINAL, BTYPE=01
para cada literal byte b:
  write_bits(tables.code[b], tables.len[b])
write_bits(tables.code[256], tables.len[256])  // EOB obrigatório
```

Não há `align_byte` obrigatório no meio: o stream termina no último bit do EOB; `take_bytes` alinha o flush final.

## 6. Decode fixed — árvore bit a bit (COMP-DEFL-05)

```text
ler BFINAL, BTYPE (deve ser 1)
loop:
  acumular bits LSB-first em `code` com comprimento crescente
  se algum sym tem len==L e code==tables.code[sym]:
    se sym==256: fim do bloco
    se 0..255: emitir literal
    senão: erro (lab não implementa length/distance)
```

O teste usa `"RFC1951"` → encode fixed → decode → igual.

## 7. Trace bit — símbolo EOB (256)

EOB tem 7 bits no alfabeto fixo. Após `reverse_bits`, o valor escrito por `write_bits(code, 7)` é consumido bit 0 primeiro pelo reader — o mesmo `code` armazenado em `tables.code[256]`.

Critério de sanidade: `tables.len[256] == 7` e `tables.len['A'] == 8` (porque `'A' == 65` ∈ 0–143).

## 8. Invariantes do laboratório

| Invariante | TODO |
|------------|------|
| Bits LSB-first; flush a cada 8 | COMP-DEFL-01 |
| Stored: BTYPE=00 + LEN/NLEN | COMP-DEFL-02 |
| Decode valida `nlen == ~len` | COMP-DEFL-03 |
| Tabelas fixas + EOB no encode | COMP-DEFL-04 |
| Decode para no símbolo 256 | COMP-DEFL-05 |

## 9. Bugs clássicos de estudante

1. **MSB-first em `write_bits`** — loop `for (i = count-1; i >= 0)` em vez de `i = 0..count-1`.
2. **Esquecer `align_byte` no stored** — LEN cai no meio do byte.
3. **NLEN = -len em signed** em vez de `uint16_t(~len)`.
4. **Não reverter bits canônicos** — fixed round-trip falha.
5. **Omitir símbolo 256** — decoder lê forever / throw.
6. **Tratar BTYPE=01 como stored** — payload lido como bytes crus.
7. **`has_bits` com overflow** — comparar `bit_pos + count` sem checar `size*8`.
8. **Decoder fixed aceitar length codes 257+** sem distance — lab deve rejeitar.

## 10. Relação com produção

| Este lab | zlib / gzip |
|----------|-------------|
| só stored + fixed literals | + dynamic Huffman + LZ77 matches |
| decode linear O(288) por bit | tables / inflate trees |
| um bloco final típico | múltiplos blocos, Adler/CRC no wrapper |

O wrapper zlib (CMF/FLG + Adler32) **não** faz parte deste exercício — só o bitstream DEFLATE interno.

## 11. Passo a passo de estudo

1. Implemente `BitWriter`/`BitReader` até o teste do nibble `0x1B`.
2. `encode_stored_block` + `decode_stored_blocks` com `DEFL`.
3. `build_fixed_literal_tables` (canônico + reverse).
4. `encode_fixed_block` / `decode_fixed_block` com `"RFC1951"`.
5. Compare com `solutions/`.

## 12. Como saber se está correto

- `take_bytes()` após `0b1011`+`0b0001` → `{0x1B}`.
- Stored round-trip `DEFL`.
- Fixed round-trip `RFC1951`.
- stdout: `OK deflate blocks`.

## 13. Perguntas de verificação

1. Por que stored precisa de `align_byte` e fixed (só literais) geralmente não no meio do bloco?
2. Qual o valor de `NLEN` para `LEN=0`?
3. Por que EOB usa 7 bits e `'A'` usa 8 no alfabeto fixo?
4. O que acontece se `write_bits` emitir MSB-first mas o reader continuar LSB-first?

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?
DEFLATE é o formato por trás de gzip/PNG/zip. Dominar bits + blocos é pré-requisito para compressores reais.

### Por quê estas invariantes?
Cada `TODO [COMP-DEFL-0x]` isola uma classe de bug (bit order, alinhamento, LEN/NLEN, tabelas, EOB).

### Por quê medir e portar?
Lab prova corretude; `projects/chris-compress` agrega LZ77 + estes blocos num pipeline completo.
