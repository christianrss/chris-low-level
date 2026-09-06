# Testes guiados — Systems — DEFLATE blocks

### Caso 1: BitWriter round-trip nibble — `PEDAGOGY-TEST: COMP-DEFL-01`
### Caso 2: stored block encode/decode — `PEDAGOGY-TEST: COMP-DEFL-02` / `COMP-DEFL-03`
### Caso 3: fixed huffman literals round-trip — `PEDAGOGY-TEST: COMP-DEFL-04` / `COMP-DEFL-05`

## COMP-DEFL-01

BitWriter/BitReader LSB-first: escreva 0b1011 e 0b0001 (4 bits cada) → byte `0x1B`.

## COMP-DEFL-02

`encode_stored_block` emite BFINAL+BTYPE=00, LEN, NLEN, payload.

## COMP-DEFL-03

`decode_stored_blocks` reconstrói o payload original.

## COMP-DEFL-04

`encode_fixed_block` usa tabela Huffman fixa de literais.

## COMP-DEFL-05

`decode_fixed_block` round-trip da string `"RFC1951"`.
