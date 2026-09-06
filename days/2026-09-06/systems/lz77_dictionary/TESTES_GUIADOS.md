# Testes guiados — Systems — LZ77 dictionary

### Caso 1: janela 32 KB — `PEDAGOGY-TEST: COMP-LZ77-01`
### Caso 2: longest match — `PEDAGOGY-TEST: COMP-LZ77-02`
### Caso 3: encode tokens — `PEDAGOGY-TEST: COMP-LZ77-03`
### Caso 4: decode sliding window — `PEDAGOGY-TEST: COMP-LZ77-04`

## COMP-LZ77-01

Constantes: `LZ77_WINDOW_SIZE == 32768`, magic `CHLZ7`.

## COMP-LZ77-02

`find_longest_match` em frase repetida: `offset` e `length` válidos.

## COMP-LZ77-03

`encode_lz77` produz header + tokens; magic nos primeiros bytes.

## COMP-LZ77-04

`decode_lz77` round-trip; magic corrompida retorna `false`.
