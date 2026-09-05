# Benchmark guiado — ELF64 triage

O benchmark mede somente parsing de header ELF64 em bytes já na memória.

Execute pelo menos cinco vezes, registre Python, CPU e SO e use a mediana de `headers/s`.

Não compare diretamente com `readelf` como se fizessem o mesmo trabalho; `readelf` analisa muito mais estruturas.

## Resultados observados

`python starter/benchmarks/elf64_benchmark.py`, fixture em memória:

| Métrica | Faixa típica |
|---------|-------------|
| headers/s | 500k–2M |
| µs/header | 0.5–2.0 |

Python puro, sem I/O de disco — mede apenas `parse_elf64_header`. Strings benchmark separado; não misturar métricas. Mediana de ≥5 runs.
