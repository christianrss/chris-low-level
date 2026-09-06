# Teoria passo a passo — Huffman entropy codec (CHHUF)

## 1. O que estamos construindo

Um codec de entropia Huffman: `BitWriter`/`BitReader` MSB-first, `build_huffman_codes`, `encode_huffman`, `decode_huffman`, container `CHHUF`. Códigos curtos para bytes frequentes; bitstream empacotado; decoder reconstrói a árvore a partir da tabela serializada (não reconta frequências).

TODOs: `COMP-HUF-01` (bit I/O), `COMP-HUF-02` (tabela), `COMP-HUF-03` (encode), `COMP-HUF-04` (decode).

## 2. Por que Huffman depois de RLE

RLE explora **repetição consecutiva**. Huffman explora **distribuição de símbolos** no bloco inteiro. Juntos (estilo DEFLATE: LZ + Huffman) cobrem os dois eixos clássicos de compressão lossless. Este lab isola só a camada de entropia + bit packing.

## 3. Bit I/O MSB-first (`COMP-HUF-01`)

### O quê
Empacotar/desempacotar bits dentro de bytes, bit mais significativo primeiro (bit 7 → bit 0).

### Como — BitWriter
Acumulador `acc_` e contador `bits_in_acc_`:
```text
acc = (acc << 1) | bit
bits_in_acc++
se bits_in_acc == 8: emitir acc; zerar
```
`write_bits(value, n)` emite do bit `n-1` até `0` (MSB do valor primeiro).  
`flush`: se sobram k bits, `acc <<= (8-k)` e emite (padding zeros à direita).

### Como — BitReader
Carrega um byte; lê o bit 7 (`current & 0x80`); depois `current <<= 1`. Sem bits → próximo byte; EOF → `false`.

### Por quê MSB-first
Convenção de tabelas Huffman canônicas e de DEFLATE/PNG: o primeiro bit do código é o de maior peso na árvore (esquerda=0 / direita=1 conforme a implementação).

### Trace manual — teste oficial

```text
write_bits(0b1011, 4)  → bits 1,0,1,1
flush                  → shift left 4 → byte 0b10110000 = 0xB0
read_bit ×4            → 1, 0, 1, 1
```

### Invariantes
- Após `flush`, nenhum bit fica só no acumulador.
- Reader e writer concordam na ordem MSB.
- `read_bit` retorna `false` só em underflow real.

### Bugs comuns
- Empilhar LSB-first (`acc |= bit << bits_in_acc`) → byte `0x0D` em vez de `0xB0`.
- Flush sem shift → bits “à direita” do byte, reader lê zeros primeiro.
- Esquecer `flush` antes de serializar o payload.

## 4. Árvore e tabela de códigos (`COMP-HUF-02`)

### O quê
Dado `freq[256]`, produzir `vector<HuffmanCodeEntry>` com `{symbol, bit_length, code}` onde `code` é alinhado à esquerda em 16 bits (MSB do código no bit 15).

### Como
1. Crie folhas para cada `freq[i] > 0`.
2. Priority queue por frequência crescente (min-heap via comparator `freq >`).
3. Caso especial: **um único símbolo** — envolva numa raiz com um filho (código de comprimento ≥ 1; lab usa depth mínimo 1).
4. Enquanto >1 nós: retire dois, crie pai com `freq = a+b`, reinserir.
5. DFS: esquerda = bit 0, direita = bit 1; em folha, `bit_length = depth` (ou 1 se depth 0), `code = prefix << (16 - bit_length)`.
6. Ordene a tabela por `symbol` (determinismo do container).

### Por quê
Códigos prefixos livres: nenhum código é prefixo de outro → decode guloso bit a bit sem ambiguidade.

### Trace manual — `AAAABB C` → freq A=3,B=2,C=1

Uma árvore possível (depende de empates na heap — o lab aceita qualquer árvore Huffman válida desde que encode/decode concordem):

```text
        (6)
       /   \
     (3)    A(3)
    /   \
  C(1)  B(2)
```

Exemplo de códigos (se esquerda=0, direita=1 e A for filho direito da raiz):

```text
A → 1     len=1
C → 00    len=2
B → 01    len=2
```

Em `HuffmanCodeEntry`, A com len=1: `code = 1 << 15 = 0x8000`.

### Invariantes
- Só símbolos com freq>0 entram na tabela.
- `bit_length ≥ 1` para toda entrada.
- Tabela não vazia se havia pelo menos um símbolo.
- `build_huffman_codes` retorna `false` se todas as freqs são 0.

### Bugs comuns
- Não tratar símbolo único → código de length 0 → encode escreve 0 bits.
- Esquecer `free_tree` → leak (lab pequeno, mas hábito ruim).
- Guardar `code` sem alinhamento à esquerda e depois shift errado no encode.

## 5. Container CHHUF — layout

```text
offset | tamanho | campo
-------|---------|------------------
0      | 5       | magic "CHHUF"
5      | 4       | orig_len u32 LE
9      | 2       | n_entries u16 LE
11     | 4*n     | entradas (sym, bit_len, code_hi, code_lo)
…      | resto   | bitstream (bytes do BitWriter após flush)
```

Cada entrada: `symbol` (u8), `bit_length` (u8), `code` u16 big-endian nos dois bytes (`code>>8`, `code&0xFF`) — porque o code já é MSB-aligned.

### O quê / Como / Por quê
O decoder não precisa do bloco original: a tabela carrega a árvore. `orig_len` limita quantos símbolos emitir (bits de padding no último byte não viram símbolos extras).

### Trace manual — header mínimo

Input 6 bytes `A A A B B C`:
```text
magic CHHUF
len = 06 00 00 00
n = número de símbolos distintos (3) → 03 00
3 entradas × 4 bytes
+ payload bit-packed
```

### Invariantes
- `input.size() >= 11` antes de ler tabela.
- `11 + 4*n ≤ input.size()` antes do bitstream.
- Magic exatamente 5 bytes `CHHUF`.

### Bugs comuns
- Confundir com CHRLE (RLE) — magics diferentes.
- Escrever `code` LE em vez da ordem hi/lo do gabarito.
- Incluir símbolos de freq 0 na tabela.

## 6. Encode (`COMP-HUF-03`)

### O quê
Contar frequências → `build_huffman_codes` → lookup[256] → escrever bits de cada byte de input → `flush` → montar header+tabela+payload.

### Como
```text
freq[b]++ para cada byte
table ← build_huffman_codes(freq)
lookup[sym] ← entry
para cada byte b: write_bits(code >> (16-len), len)
flush
serializar CHHUF + len + n + entries + writer.bytes()
```

### Por quê `code >> (16 - bit_length)`
O entry guarda o código alinhado ao bit 15; `write_bits` espera o valor nos `bit_length` bits baixos do argumento (e emite MSB-first desses bits).

### Trace manual — bits para AAAABB C com códigos A=1, B=01, C=00

```text
A A A B B C → 1 1 1 01 01 00
bits: 111010100
após flush → dois bytes (9 bits + padding)
```

### Invariantes
- `encode` falha se `build` falha (input vazio → false neste lab).
- Payload só após `flush`.

### Bugs comuns
- Escrever `e.code` com 16 bits em vez de `bit_length`.
- Esquecer flush → último símbolo incompleto no fio.
- Ordenar tabela diferente entre encode implícito e o que foi serializado (serialize a mesma `table` do build).

## 7. Decode (`COMP-HUF-04`)

### O quê
Validar magic; ler len e n; reconstruir trie a partir das entradas; `BitReader` no restante; caminhar até folha `len` vezes.

### Como — rebuild da árvore
Para cada entrada, para bit `b = 0 .. bit_len-1`:
```text
bit = (code >> (15-b)) & 1
seguir left(0)/right(1), criando nós sob demanda
na folha: nodes[node].symbol = sym
```

Decode de um símbolo: começar na raiz; enquanto `symbol < 0`, ler 1 bit e descer; emitir símbolo.

### Por quê árvore em vez de tabela invertida
Simples e robusta para códigos de comprimentos variados; casa com a ordem MSB dos bits no `code`.

### Trace manual — um símbolo

```text
code A = 0x8000, len=1
bit0 = (0x8000>>15)&1 = 1 → desce right → folha A
reader lê 1 → emite 'A'
```

### Invariantes
- Parar após exatamente `len` símbolos (ignorar padding).
- `read_bit` falhou no meio → `false`.
- Filho inexistente (`node < 0`) → `false`.
- Magic errado → `false` (teste oficial).

### Bugs comuns
- Usar `(code >> (bit_len-1-b))` misturando alinhamentos.
- Decodificar até EOF de bits em vez de `orig_len` → padding vira lixo.
- Não checar `p + n*4 > size`.

## 8. Fluxo completo

```text
input bytes
  → freq[]
  → build_huffman_codes          (COMP-HUF-02)
  → BitWriter + flush            (COMP-HUF-01)
  → CHHUF frame                  (COMP-HUF-03)
  → BitReader + trie walk        (COMP-HUF-04)
  → output bytes == input
```

## 9. Complexidade

| Fase | Custo |
|------|-------|
| Contagem | O(n) |
| Build heap | O(σ log σ), σ≤256 |
| Encode bits | O(n · L̄) |
| Decode | O(n · L̄) |
| Memória tabela | O(σ) |

## 10. Comparação com produção

| Este lab (CHHUF) | DEFLATE / zlib |
|------------------|----------------|
| Huffman por bloco, tabela explícita | códigos canônicos + alphabet packing |
| Árvore na decode | tabelas lookup / canonical |
| Magic próprio | zlib/gzip headers |
| Toy, sem LZ | LZ77 + Huffman |

O bit I/O MSB-first e a ideia de códigos prefixos transferem direto.

## 11. Passo a passo dos TODOs

1. `COMP-HUF-01` em `starter/bit_io.cpp` — writer, flush, reader.
2. `COMP-HUF-02` em `starter/huffman.cpp` — `build_huffman_codes`.
3. `COMP-HUF-03` — `encode_huffman`.
4. `COMP-HUF-04` — `decode_huffman`.
5. `ctest` até `OK huffman`.

## 12. Como saber se está correto

- Caso 1: `0b1011` + flush → `0xB0`; reader lê 1,0,1,1.
- Caso 2: `build_huffman_codes` em AAAABB C → tabela não vazia.
- Caso 3: encode retorna true e monta magic `CHHUF`.
- Caso 4: decode round-trip; magic `X…` → false.

## 13. Invariantes globais

- APIs: `build_huffman_codes`, `encode_huffman`, `decode_huffman`; magic `CHHUF`.
- Bit I/O MSB-first em `bit_io.cpp`.
- `HuffmanCodeEntry.code` alinhado à esquerda em 16 bits.
- Decode emite exatamente `orig_len` bytes ou falha.

## 14. Bugs comuns (checklist)

| Sintoma | Causa |
|---------|--------|
| `bytes()[0] != 0xB0` | LSB-first ou flush errado (`COMP-HUF-01`) |
| tabela vazia com input não vazio | heap/folhas (`COMP-HUF-02`) |
| encode false | build falhou / input vazio |
| round-trip quebra | shift `16-len` ou árvore decode (`COMP-HUF-03/04`) |
| aceita magic ruim | `memcmp` ausente |
| símbolos a mais no fim | decode até EOF em vez de `len` |

## 15. Por quê este módulo existe

Treinar o contrato **bits ↔ bytes** e a serialização de uma árvore de prefixos — o núcleo invisível detrás de zip, png IDAT e muitos codecs de mídia — com testes que falham de forma localizada por TODO.
