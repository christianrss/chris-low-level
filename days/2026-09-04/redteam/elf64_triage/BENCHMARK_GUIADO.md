# Benchmark guiado — ELF64 triage

O benchmark mede a pipeline pedagógica em bytes já na memória: header → program headers → section headers → dynsym.

Execute pelo menos cinco vezes, registre Python, CPU e SO e use a mediana de `triages/s` (ou `headers/s` se rodar só o estágio Ehdr).

Não compare diretamente com `readelf` como se fizessem o mesmo trabalho; `readelf` analisa muito mais estruturas e faz I/O.

## Resultados observados

`python starter/benchmarks/elf64_benchmark.py`, fixture rico em memória:

| Métrica | Faixa típica |
|---------|-------------|
| triages/s (pipeline) | 40k–400k |
| µs/triage | 2.5–25 |
| headers/s (só Ehdr, se isolado) | 500k–2M |

Python puro, sem I/O de disco. Mediana de ≥5 runs. Strings permanecem em benchmark separado (`benchmarks/benchmark.py`); não misturar métricas.
