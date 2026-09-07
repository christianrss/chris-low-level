# Benchmark guiado — /proc task snapshot

## Protocolo

10 000 parses de linhas `stat` sintéticas.

```powershell
python days/2026-09-07/linux/proc_task_snapshot/benchmarks/bench.py
```

## Resultados observados

| Workload | Mediana (ms) |
|----------|-------------|
| 10000 parses | 13.587 |

Validação local 2026-09-07.
