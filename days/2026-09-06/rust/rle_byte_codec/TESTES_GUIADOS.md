# Testes guiados — CHRLE em Rust

## Por que testar encode e decode juntos?

RLE “quase certo” passa em um sentido e quebra no outro (endian, magic, LengthMismatch). `tests/rle_tests.rs` amarra layout, round-trip e rejeição aos IDs `RS-RLE-01..03`.

## Caso 1 — encode dez zeros (PEDAGOGY-TEST: RS-RLE-01)

1. `input = [0u8; 10]`.
2. `enc = encode(&input)`.
3. `enc[0..5] == b"CHRLE"`.
4. LE32 em `[5..9] == 10`.
5. `enc[9]==10`, `enc[10]==0`.

**Invariante:** um único run cobre o payload.

**Se falhar:** magic errada; length BE; ou loop de runs não rodou.

## Caso 2 — decode ABCD (PEDAGOGY-TEST: RS-RLE-02)

1. `input = b"ABCD"`.
2. `decode(&encode(&input)).unwrap() == input`.

**Invariante:** quatro runs de count=1.

**Se falhar:** decode não lê pares; ou LengthMismatch precoce.

## Caso 3 — round-trip + bad magic (PEDAGOGY-TEST: RS-RLE-03)

1. `round_trip_ok(b"AAAAABBBCC") == true`.
2. Flip `enc[0]='X'` → `Err(BadMagic)`.
3. Slice de 4 bytes → `Err(Truncated)`.

**Invariante:** erros tipados, sem panic.

**Se falhar:** stub ainda retorna `false` / `Truncated` genérico.

## Cobertura pedagógica auditada

- `RS-RLE-01` — Caso 1.
- `RS-RLE-02` — Caso 2.
- `RS-RLE-03` — Caso 3.

## Como depurar

1. `cargo test caso_1 -- --nocapture`.
2. Imprima `enc` em hex (`{:02x?}`).
3. Confira endian com `u32::from_le_bytes`.
