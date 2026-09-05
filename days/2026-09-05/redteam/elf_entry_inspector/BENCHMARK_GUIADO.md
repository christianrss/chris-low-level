# Benchmark guiado — ELF entry inspector

## Hipótese

Parse de 64 bytes de header ELF é O(1) e negligível frente a leitura de disco — mesmo para milhares de arquivos, o custo é dominado por I/O.

## Protocolo

1. Leia os primeiros 64 bytes de N binários (N=1000).
2. Chame `parse_elf64()` em loop.
3. Meça apenas o tempo de parsing (bytes já em memória).
4. 2 warm-ups + 9 repetições; reporte mediana.

## Resultados observados

| Métrica | Mediana observada |
|---------|-------------------|
| `parse_elf64` × 100.000 (in-memory) | < 50 ms total |
| Por chamada | < 0.5 µs |

**Conclusão:** otimizar o parser não é prioridade — otimizar leitura de disco (mmap, batch) é. Em pipelines de malware analysis com milhões de samples, o gargalo continua sendo storage e hash, não `struct.unpack`.
