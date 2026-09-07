# Benchmark guiado — KV cache ring

Hipótese: append e lookup individual são O(1); `window` é O(W).

## Protocolo

1. 5 warmups + 30 repetições.
2. Capacities 128 / 1024 / 8192; windows 16 / 128 / 1024.
3. Registre mediana em ms (Python puro — não GPU).

```powershell
python days/2026-09-07/ai/kv_cache_ring/benchmarks/bench.py
```

## Resultados observados

| Workload | Mediana (ms) | Ambiente |
|----------|-------------|----------|
| 1000 windows size 128 | 12.124 | validação local 2026-09-07 |

Valores locais do container de automação — não regra universal.
