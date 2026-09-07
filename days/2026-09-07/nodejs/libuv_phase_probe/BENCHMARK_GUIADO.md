# Benchmark guiado — libuv phase probe

## Protocolo

10 000 iterações de `boundedNextTick` e medição de ordem de fases em `probe()`.

```powershell
node days/2026-09-07/nodejs/libuv_phase_probe/benchmarks/bench.js
```

## Resultados observados

| Workload | Mediana (ms) |
|----------|-------------|
| 10000 nextTick | 0.62 |

Node v22.16.0, validação local 2026-09-07.
