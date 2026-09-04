# Benchmark guiado — ELF64 parser

```bash
python projects/chris-binary-toolkit/benchmarks/elf64_benchmark.py
```

O benchmark usa o mesmo header sintético muitas vezes para isolar custo do parser. Ele não mede I/O de disco e não deve ser interpretado como throughput de um analisador ELF completo.
