# Testes guiados — RLE byte codec

## Por que testar este codec?

RLE parece trivial, mas erros de magic, endianness, teto de run e truncamento produzem buffers que “quase” decodificam. Os casos abaixo amarram cada `TODO` a um `PEDAGOGY-TEST` em `starter/test_rle.cpp`.

## Caso 1 — zeros run (PEDAGOGY-TEST: COMP-RLE-01)

**Arquivo:** `starter/test_rle.cpp`

1. Crie `vector` de 10 bytes `0x00`.
2. Chame `encode_rle(in, enc)` — deve retornar `true`.
3. Chame `decode_rle(enc, dec)` — deve retornar `true`.
4. Verifique `dec == in`.

**Invariante:** header `CHRLE` + `0A 00 00 00` + par `0A 00`; round-trip idêntico.

**Se falhar:** confira magic 5 bytes, LE32 e cap 255 no encode; depois o decode.

## Caso 2 — ASCII sem repetição (PEDAGOGY-TEST: COMP-RLE-02)

1. Input `"ABCD"` (4 bytes distintos).
2. Encode + decode.
3. `dec == in`.

**Invariante:** quatro pares `01 41 01 42 01 43 01 44`; tamanho comprimido > original (expansão esperada).

**Se falhar:** encoder pulou count=1; ou decoder parou cedo.

## Caso 3 — magic corrompido (PEDAGOGY-TEST: COMP-RLE-03)

1. Encode um buffer válido.
2. `enc[0] = 'X'`.
3. `decode_rle` deve retornar `false`.

**Invariante:** `memcmp` com `CHRLE` rejeita antes de expandir.

**Nota de ID:** o marcador no teste é `COMP-RLE-03` para o caminho negativo de magic; a igualdade `out.size()==len` (mesmo TODO no starter) deve ser exercitada com o scratch de truncamento da resolução.

## Cobertura pedagógica auditada

- `COMP-RLE-01` — Caso 1 (encode no caminho do round-trip).
- `COMP-RLE-02` — Caso 2 (decode de runs literais).
- `COMP-RLE-03` — Caso 3 (rejeição) + contrato de tamanho no decoder.

Arquivo de teste automatizado: `starter/test_rle.cpp` (espelhado em `solutions/test_rle.cpp`).

## Como depurar

1. Falha em `encode_rle` → só `COMP-RLE-01`.
2. Encode ok, decode falha no round-trip → hexdump de `enc` vs tabela da teoria.
3. Round-trip ok, Caso 3 falha → magic não validado (`memcmp` ausente).
