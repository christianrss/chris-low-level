# Benchmark guiado - extrator de strings

**Pergunta:** como o throughput do scanner muda com o tamanho do buffer?

Gere buffers determinísticos de 1 MiB, 8 MiB e 32 MiB contendo sequências ASCII em posições conhecidas. Meça apenas `extract_ascii_strings()`. Registre MB/s e confirme que a quantidade de strings encontrada permanece correta.

Depois use `cProfile` ou um profiler Python para descobrir onde o tempo é gasto antes de otimizar.

## Resultados observados

Ambiente de referência: Linux container, GCC 14.2, Python 3.13 (ver `benchmarks/results-2026-09-03.json`).

| Métrica | Valor referência | Notas |
|---------|------------------|-------|
| Scan 1–8 MiB | ~16.3 MiB/s | binary toolkit |

Valores são ordem de grandeza — **rerode na sua máquina** e registre mediana após warm-up.