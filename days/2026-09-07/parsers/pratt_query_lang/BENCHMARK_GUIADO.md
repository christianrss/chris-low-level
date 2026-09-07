# Benchmark guiado — Pratt query language

## Protocolo

5000 parses de queries com `AND`/`OR`/`field`.

```powershell
python days/2026-09-07/parsers/pratt_query_lang/benchmarks/bench.py
```

## Resultados observados

| Workload | Mediana (ms) |
|----------|-------------|
| 5000 parses | 42.252 |

Validação local 2026-09-07.
