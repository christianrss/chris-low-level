# Testes guiados — Huffman entropy codec

## Por que testar este codec?

Erros de ordem de bits, alinhamento de código ou padding no último byte quebram o round-trip de forma opaca. Cada caso abaixo mapeia um `PEDAGOGY-TEST` em `starter/test_huffman.cpp`.

## Caso 1 — bit writer MSB-first (PEDAGOGY-TEST: COMP-HUF-01)

1. `BitWriter w; w.write_bits(0b1011, 4); w.flush();`
2. `w.bytes().size() == 1` e `w.bytes()[0] == 0xB0`.
3. `BitReader` sobre esses bytes: quatro `read_bit` → true, false, true, true.

**Invariante:** nibble `1011` + padding vira `10110000`.

**Se falhar:** revise `write_bit` / `flush` em `starter/bit_io.cpp`.

## Caso 2 — build huffman table (PEDAGOGY-TEST: COMP-HUF-02)

1. Input `A,A,A,B,B,C`; conte `freq[256]`.
2. `build_huffman_codes(freq, table)` → `true`.
3. `!table.empty()`.

**Invariante:** três símbolos (ou mais se empates) com `bit_length ≥ 1`.

**Se falhar:** heap vazio, símbolo único sem wrap, ou `return false` residual.

## Caso 3 — encode (PEDAGOGY-TEST: COMP-HUF-03)

1. `encode_huffman(in, enc)` → `true`.
2. Implicitamente: magic/tabela/payload presentes para o Caso 4.

**Invariante:** `enc` começa com `CHHUF`; tamanho > 11.

**Se falhar:** `build` falhou, ou serialize incompleta.

## Caso 4 — decode + corrupt magic (PEDAGOGY-TEST: COMP-HUF-04)

1. `decode_huffman(enc, dec)` → `true` e `dec == in`.
2. Re-encode; `enc[0]='X'`; `decode_huffman` → `false`.

**Invariante:** trie+`BitReader` recuperam o plaintext; magic é gate obrigatório.

**Se falhar no round-trip:** mismatch MSB entre encode shift e decode `(code>>(15-b))`.  
**Se falhar no negativo:** `memcmp` ausente.

## Cobertura pedagógica auditada

- `COMP-HUF-01` — Caso 1  
- `COMP-HUF-02` — Caso 2  
- `COMP-HUF-03` — Caso 3  
- `COMP-HUF-04` — Caso 4  

Arquivo: `starter/test_huffman.cpp` (espelho em `solutions/test_huffman.cpp`).

## Como depurar

1. Isole bit I/O (Caso 1) antes da árvore.
2. Imprima `(symbol, bit_length, code)` após o build.
3. Hexdump dos primeiros 11 + `4*n` bytes do encode.
4. No decode, conte quantos bits foram lidos vs `sum(bit_length)` esperado.
