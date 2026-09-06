# Exercícios — Systems — DEFLATE blocks

Cinco níveis alinhados aos TODOs auditáveis do módulo.

## Fácil

- **COMP-DEFL-01:** Implemente `BitWriter`/`BitReader` em `starter/bit_stream.cpp` com bits LSB-first, flush a 8 bits e `align_byte`.

## Médio

- **COMP-DEFL-02:** `encode_stored_block` — `BFINAL`/`BTYPE=00`, alinhamento, `LEN`/`NLEN`, payload.
- **COMP-DEFL-03:** `decode_stored_blocks` — validar `nlen == uint16_t(~len)` e remontar bytes.

## Difícil

- **COMP-DEFL-04:** `build_fixed_literal_tables` (RFC 1951 + `reverse_bits`) e `encode_fixed_block` com EOB 256.

## Expert

- **COMP-DEFL-05:** `decode_fixed_block` — decodificar Huffman fixo bit a bit até o símbolo 256; rejeitar length codes neste lab.
