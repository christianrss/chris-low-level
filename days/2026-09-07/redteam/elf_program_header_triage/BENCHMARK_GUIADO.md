# Benchmark guiado — ELF Program Header triage

## Protocolo

Parse repetido de fixture sintético com 128 entradas PHDR.

```powershell
python days/2026-09-07/redteam/elf_program_header_triage/benchmarks/bench.py
```

## Resultados observados

| Workload | Mediana (ms) |
|----------|-------------|
| 128 PHDR | 0.1285 |

Ambiente: validação local 2026-09-07.
