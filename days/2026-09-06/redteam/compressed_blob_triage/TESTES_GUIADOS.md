# Testes guiados — Compressed blob triage

## Por que testar triage?

Magic errado roteia o decompressor errado; limites só no compressed ignoram zip bombs; regex fraca perde IOCs. Cada caso amarra um `TODO` a `PEDAGOGY-TEST` em `starter/test_blob_triage.py`.

## Caso 1 — magic gzip (PEDAGOGY-TEST: RT-COMP-01)

1. `payload = gzip.compress(b"hello triage")`.
2. `detect_compression_magic(payload) == "gzip"`.

**Invariante:** prefixo `1F 8B`.

**Se falhar:** ordem das checagens ou `len < 2`.

## Caso 2 — magic zlib (PEDAGOGY-TEST: RT-COMP-01)

1. `payload = zlib.compress(b"zlib header test")`.
2. Assert `payload[:2] == b"\x78\x9c"`.
3. `detect_compression_magic(payload) == "zlib"`.

**Invariante:** CMF/FLG default do `zlib.compress`.

**Se falhar:** FLG não inclui `0x9C`.

## Caso 3 — size limits (PEDAGOGY-TEST: RT-COMP-02)

1. `big = gzip.compress(b"x" * 200_000)`.
2. `validate_size_limits(big, 100_000, 50_000)` → `False`.
3. `small = gzip.compress(b"ok")` com limites 10_000 → `True`.

**Invariante:** uncompressed 200k estoura 50k mesmo se compressed couber.

**Se falhar:** só checou `len(data)`; ou não chamou `safe_inflate_preview`.

## Caso 4 — strings ASCII (PEDAGOGY-TEST: RT-COMP-03)

1. `raw = b"\x00SECRET_KEY=abc123\xff" + gzip.compress(b"noise")`.
2. `extract_ascii_strings(raw, min_len=4)`.
3. `"SECRET_KEY=abc123" in strings`.

**Invariante:** run imprimível ≥ 4 incluindo `=` e `_`.

## Cobertura pedagógica auditada

- `RT-COMP-01` — Casos 1–2.
- `RT-COMP-02` — Caso 3.
- `RT-COMP-03` — Caso 4.

## Como depurar

1. Magic: `print(payload[:4].hex())`.
2. Limites: imprima `len(big)` e `len(gzip.decompress(big))` separadamente.
3. Strings: teste o regex no REPL com o prefixo `\x00SECRET...`.
