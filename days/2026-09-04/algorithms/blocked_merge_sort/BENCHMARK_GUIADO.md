# Benchmark guiado — blocked_merge_sort

## Protocolo mínimo
- escreva hipótese antes de medir;
- build Release quando possível;
- warm-up antes das medições comparativas;
- pelo menos 5 repetições para comparação séria;
- registre CPU, SO, compilador, flags e input;
- guarde resultado bruto e mediana;
- não misture alteração de algoritmo com alteração de flags/hardware na mesma comparação.

O benchmark executável está em `starter/benchmarks/` e é habilitado por `-DCHRIS_BUILD_BENCHMARKS=ON`. A interpretação específica está em `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`.

## Resultados observados

n=65536, seed fixa, métricas do harness (`cmp` / `bread` / `bwrite`):

| tile_size | block_reads (ordem) | Observação |
|----------:|--------------------:|------------|
| 64 | alto | muitos tiles e mais passes de merge |
| 256 | médio | bom equilíbrio típico em lab |
| 1024 | menor I/O de tiles | fase 0 mais cara em comparisons (insertion) |
| 4096 | mínimo de tiles | insertion local O(t²) pesa no wall-clock |

Sorted vs reversed com o mesmo `tile_size` devem mostrar **I/O idêntico** (estrutura fixa) e comparisons da fase 0 diferentes. Mediana de ≥5 runs; registre compilador e flag `-O` / `/O2`.
