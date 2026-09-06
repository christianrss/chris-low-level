# Exercícios — Systems — LZ77 dictionary codec

Quatro níveis alinhados aos TODOs auditáveis do módulo.

## Fácil

- **COMP-LZ77-01:** Em `starter/lz77.cpp` / `find_longest_match`, calcule `window_start` com `LZ77_WINDOW_SIZE` (32768) e nunca busque fora dessa janela.

## Médio

- **COMP-LZ77-02:** Retorne o maior match com `length >= LZ77_MIN_MATCH` e `length <= LZ77_MAX_MATCH`; preencha `LZ77Match::{offset,length}`.

## Difícil

- **COMP-LZ77-03:** Implemente `encode_lz77`: magic `CHLZ7`, `u32` LE do tamanho, tokens `0x00`+literal e `0x01`+offset LE16+length.

## Expert

- **COMP-LZ77-04:** Implemente `decode_lz77` com validação de magic/offset, cópia byte a byte (overlap OK) e rejeição de stream corrompido; garanta round-trip e `out.size() == len`.
