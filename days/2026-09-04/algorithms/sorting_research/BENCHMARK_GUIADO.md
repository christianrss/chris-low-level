# Benchmark guiado — sorting_research

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

n=65536, seed fixa, comparações reportadas pelo benchmark:

| Distribuição | Merge comparisons | Quick comparisons | Quick degradado? |
|--------------|------------------:|------------------:|:----------------:|
| random | ~1.1M | ~1.0–1.3M | não |
| sorted | ~1.1M | >>10M | **sim** |
| reversed | ~1.1M | >>10M | **sim** |
| duplicates | ~1.1M | menor que sorted | parcial |

Tempos wall-clock seguem tendência similar, mas comparisons isolam o efeito do pivot. Mediana de ≥5 runs; registre compilador e `-O` flag.
