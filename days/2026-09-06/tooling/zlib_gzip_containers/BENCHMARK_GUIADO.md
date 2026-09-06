# Benchmark guiado — zlib/gzip containers

**Pergunta:** qual o custo de wrap+unwrap zlib stored versus gzip stored no mesmo plaintext?

Protocolo:

1. Compile **Release** (`solutions/` ou starter completo).
2. Payload determinístico de **1 KiB** (ex.: bytes `i & 0xFF`).
3. 5 aquecimentos; ≥30 medições de `compress→decompress` wall time.
4. Registre mediana e min/max em ns ou MB/s.
5. Anote que stored não comprime — você mede empacotamento + checksum, não ratio.

**Experimento seguinte:** comparar Adler-32 vs CRC-32 só no plaintext (sem I/O de container) para isolar o checksum.

## Resultados observados

Ambiente de referência: preencha na sua máquina após o lab.

| Métrica | Valor referência | Notas |
|---------|------------------|-------|
| zlib 1 KiB round-trip median | ___ µs | stored + Adler |
| gzip 1 KiB round-trip median | ___ µs | stored + CRC |
| Adler-only 1 KiB | ___ ns | sem deflate |
| CRC-only 1 KiB | ___ ns | tabela quente |

Valores são ordem de grandeza — **rerode** e registre mediana após warm-up.
