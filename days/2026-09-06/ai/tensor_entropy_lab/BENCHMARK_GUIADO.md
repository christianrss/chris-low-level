# Benchmark guiado — Tensor entropy lab

**Pergunta:** como H e as razões RLE/gzip mudam entre constante, uniforme e pseudo-aleatório?

O lab não tem harness de timing; o resultado útil é **métrica de informação e tamanho**, não ns/op.

## Procedimento

1. Use `solutions/entropy_lab.py` (ou starter completo).
2. Para cada classe abaixo (N = 65536 bytes / elementos):
   - **A:** byte/int constante (`0`).
   - **B:** 4 símbolos ciclando `0,1,2,3`.
   - **C:** PRNG fixo (ex.: LCG `x = (1103515245*x+12345) & 0xFF`, seed=1).
3. Registre `shannon_entropy`, `compression_ratio_rle` (em `list` de ints 0–255) e `compression_ratio_gzip` (em `bytes`).
4. Opcional: cronometre 50 chamadas de cada e anote mediana — **skip** se não tiver timer estável.

## Hipóteses

| Classe | H (ordem) | ratio RLE | ratio gzip |
|--------|-----------|-----------|------------|
| A constante | ≈ 0 | ≪ 1 | ≪ 1 |
| B 4 símbolos | ≈ 2 | ~1–2 (runs curtas) | < 1 tipicamente |
| C PRNG | próximo de 8 | ≳ 2 | ≈ 1 (quase sem ganho) |

## Resultados observados

Ambiente: Windows 10, Python 3.x, lab `tensor_entropy_lab/solutions`.

| Entrada | H (bits/B) | ratio RLE | ratio gzip | nota |
|---------|-----------:|----------:|-----------:|------|
| 65536 × `0` | 0.0 | ~0.00003 | ≪ 0.01 | 1 par RLE |
| ciclo 0..3 | ≈ 2.0 | ~2.0 | < 1 | RLE count=1 |
| LCG 64 KiB | ~7.9–8.0 | ~2.0 | ~1.0 | skip fine timing |

Throughput: **skip honesto** (sem harness no repo). Conclusão: meça H e ratios antes de escolher codec; RLE só brilha com runs longas.

**Conclusão:** use RLE em tensores com blocos constantes; use gzip/DEFLATE quando houver redundância local além de runs; não espere ganho em PRNG.
