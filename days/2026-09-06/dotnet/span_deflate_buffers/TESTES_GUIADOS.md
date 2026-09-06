# Testes guiados — Span deflate buffers

## Por que testar stored blocks?

Header curto, BTYPE errado e LEN/NLEN mentiroso são falhas silenciosas em parsers. O `Main` em `starter/Program.cs` amarra round-trip e truncamento aos IDs `DN-SPAN-01..03`.

## Caso 1 — inflate stored (PEDAGOGY-TEST: DN-SPAN-01/02/03)

1. `payload = "LOWLEVEL"u8.ToArray()`.
2. `block = BuildStoredBlock(payload)` → `01 | LEN | NLEN | bytes`.
3. `InflateStored(block)` deve `SequenceEqual` o payload.

**Invariante:** plaintext idêntico; header `0x01`; LEN=8; NLEN=`0xFFF7`.

**Se falhar:** BTYPE mask, endian, offset ≠ 5, ou NLEN não validado / Slice errado.

## Caso 2 — truncado (PEDAGOGY-TEST: DN-SPAN-01)

1. `InflateStored(block.AsSpan(0, 3))`.
2. Deve lançar `InvalidDataException`.
3. Se não lançar, `Main` lança `"truncated accepted"`.

**Invariante:** `Length < 5` rejeitado antes de ler LEN/NLEN.

## Caso 3 — (manual) LEN/NLEN (PEDAGOGY-TEST: DN-SPAN-03)

1. Copie um bloco válido; faça `block[3] ^= 0xFF`.
2. `InflateStored` → `"len/nlen mismatch"`.

**Invariante:** XOR ≠ `0xFFFF` falha.

## Caso 4 — Span sem cópia extra de input

Observação pedagógica: API recebe `ReadOnlySpan<byte>`; truncamento usa `AsSpan(0,3)` sem `Array.Copy` do input. A única alocação necessária é o `byte[]` de saída.

## Cobertura pedagógica auditada

- `DN-SPAN-01` — header + truncamento curto.
- `DN-SPAN-02` — inflate/CopyTo.
- `DN-SPAN-03` — complemento LEN/NLEN.

## Como depurar

1. Hexdump dos 5 primeiros bytes do bloco.
2. Calcule `len` e `nlen` no papel para LEN=8.
3. Confirme `(header >> 1) & 3 == 0` para `0x01`.
