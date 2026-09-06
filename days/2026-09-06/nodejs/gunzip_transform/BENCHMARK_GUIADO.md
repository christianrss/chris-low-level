# Benchmark guiado — GunzipTransform

**Pergunta:** como `chunkSize` e `highWaterMark` do sink mudam `falseWrites` / `backpressurePauses`, e qual o throughput aproximado do Transform?

## Procedimento

1. Parta de `solutions/backpressure_metrics.js`.
2. Fixe plaintext `LOWLEVEL`×4096 (ou maior).
3. Varie `chunkSize` ∈ {16, 64, 1024} e sink `highWaterMark` ∈ {16, 1024, 16384}.
4. Para cada par, rode o demo 5×; registre mediana de `falseWrites`, `backpressurePauses`, tempo wall-clock.
5. Opcional: compare com `zlib.gunzipSync` one-shot no mesmo payload (latência vs memória pico).

## Hipóteses

| Setup | Expectativa |
|-------|-------------|
| chunk 16 + HWM 16 | muitos `falseWrites` |
| chunk 1024 + HWM 16 KiB | poucos ou zero `falseWrites` |
| one-shot sync | menor overhead de eventos; pior pico de memória |

## Resultados observados

Ambiente: Windows 10, Node 18+, lab `gunzip_transform/solutions`.

| chunkSize | HWM sink | falseWrites (ordem) | nota |
|----------:|---------:|--------------------:|------|
| 64 | 16 | > 0 (baseline do lab) | receita do gabarito |
| 1024 | 16384 | ~0 | backpressure raro |
| 16 | 16 | alto | mais awaits |

Throughput absoluto: **skip honesto** sem harness dedicado; o resultado útil é a **relação** chunk/HWM ↔ contadores.

**Conclusão:** backpressure só aparece quando o consumidor é mais lento/mais apertado que o produtor. Em produção, ajuste HWM com métricas — não desligue `drain`.
