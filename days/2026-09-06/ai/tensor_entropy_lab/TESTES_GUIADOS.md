# Testes guiados — Tensor entropy lab

## Por que testar estas métricas?

Entropia e razões de compressão “quase certas” (log natural, ratio invertido, último run perdido) passam visualmente e mentem em decisão de codec. Cada caso amarra um `TODO` a um `PEDAGOGY-TEST` em `starter/test_entropy_lab.py`.

## Caso 1 — Shannon uniforme (PEDAGOGY-TEST: AI-ENT-01)

**Arquivo:** `starter/test_entropy_lab.py` → `test_uniform_entropy`

1. `data = bytes([0, 1, 2, 3] * 25)` (N=100, 4 símbolos).
2. `h = shannon_entropy(data)`.
3. `abs(h - 2.0) < 1e-6`.

**Invariante:** \(H=\log_2 4=2\) bits/byte.

**Se falhar:** confira `math.log2` e que só itera `counts.values()`.

## Caso 2 — RLE repetitivo (PEDAGOGY-TEST: AI-ENT-02)

1. `tensor = [7]*1000 + [3]*500`.
2. `tensor_rle_encode` → exatamente `[(7,1000),(3,500)]`.
3. `compression_ratio_rle(tensor) < 0.01`.

**Invariante:** 2 pares × 8 B = 16; raw = 6000; ratio ≈ 0.00267.

**Se falhar:** append do último run; ou ratio sem helpers `*8`/`*4`.

## Caso 3 — gzip vs RLE (PEDAGOGY-TEST: AI-ENT-03)

1. `payload = b"LOWLEVEL" * 500`.
2. `gz_ratio = compression_ratio_gzip(payload)` → `< 0.2`.
3. `rle_ratio = compression_ratio_rle(list(payload))`.
4. `gz_ratio < rle_ratio`.

**Invariante:** DEFLATE vence o modelo RLE-int32 neste padrão repetitivo ASCII.

**Se falhar:** stub gzip; ou RLE quebrado (ratio RLE artificialmente baixo).

## Cobertura pedagógica auditada

- `AI-ENT-01` — Caso 1.
- `AI-ENT-02` — Caso 2.
- `AI-ENT-03` — Caso 3.

Arquivo: `starter/test_entropy_lab.py` (espelhado em `solutions/`).

## Como depurar

1. `NotImplementedError` → ID ainda stub.
2. H errado → REPL com `Counter` e soma manual.
3. pairs errados → trace `[7,7,3]`.
4. Caso 3 só gzip falha → `len(gzip.compress(payload))`.
