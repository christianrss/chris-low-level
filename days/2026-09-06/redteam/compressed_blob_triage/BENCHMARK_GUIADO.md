# Benchmark guiado — Compressed blob triage

**Pergunta:** quanto custa magic-only versus `validate_size_limits` (com inflate) em blobs repetitivos vs quase aleatórios?

## Procedimento

1. Use `solutions/blob_triage.py`.
2. Gere três blobs (~64 KiB plaintext):
   - **A:** `gzip.compress(b"A" * 65536)`.
   - **B:** `gzip.compress(os.urandom(65536))` (ou LCG).
   - **C:** buffer sem magic (64 KiB `0x00`) — ramo `unknown`.
3. Cronometre 1000× `detect_compression_magic` vs 100× `validate_size_limits(..., max_c=10**7, max_u=10**7)`.
4. Registre também `len(compressed)` e se validate retorna True com `max_u=1000` (deve falhar em A/B).

## Hipóteses

| Blobs | magic | validate |
|-------|-------|----------|
| A/B | O(1), µs | dominado pelo inflate |
| C unknown | O(1) | sem inflate (só len) |

## Resultados observados

Ambiente: Windows 10, Python 3.x, lab `compressed_blob_triage/solutions`.

| Caso | len(comp) | magic | validate (max_u alto) | validate (max_u=1000) |
|------|----------:|-------|------------------------|------------------------|
| A runs | pequeno | gzip | True | False |
| B random | ≈ plaintext | gzip | True | False |
| C zeros | 65536 | unknown | True se max_u≥65536 | depende |

Timing fino: **skip honesto** se o ambiente não tiver timer estável; o insight é qualitativo — **nunca confie só no tamanho compressed**.

**Conclusão:** magic é barato; validate com inflate é o custo real e o que impede zip bombs. Em produção, troque inflate one-shot por streaming com teto.
