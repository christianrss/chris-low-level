# Testes guiados — Gzip member parse

## Por que testar offsets?

Um parser que “aceita” magic mas erre FNAME desloca o DEFLATE e o CRC vira lixo. Os casos cobrem header, skip de nome e trailer.

## Caso 1 — header fixo (PEDAGOGY-TEST: RS-GZ-01)

1. `member = build_minimal_member(...)`.
2. `validate_fixed_header` → flags 0.
3. Magic corrompida → `BadMagic`.
4. Flags reservadas → `ReservedFlags`.
5. Slice curto → `Truncated`.

**Se falhar:** ordem das checagens ou máscara `0xE0`.

## Caso 2 — FNAME (PEDAGOGY-TEST: RS-GZ-02)

1. Monte header com `FLG_FNAME` + `file.txt\0`.
2. `deflate_payload_start` == índice após o NUL.

**Se falhar:** NUL não consumido; ou `validate_fixed_header` não chamado.

## Caso 3 — parse_member (PEDAGOGY-TEST: RS-GZ-03)

1. Member mínimo sem flags.
2. `deflate_start == 10`, `trailer_start == len-8`.
3. Slice DEFLATE == bytes opacos; CRC/ISIZE batem com helper.

**Se falhar:** trailer calculado do início (errado) em vez do fim.

## Cobertura pedagógica auditada

- `RS-GZ-01` — Caso 1.
- `RS-GZ-02` — Caso 2.
- `RS-GZ-03` — Caso 3.

## Como depurar

1. `cargo test caso_2 -- --nocapture`.
2. Imprima `data` em hex.
3. Confira `FLG_FNAME = 0x08`.
