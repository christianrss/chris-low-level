# Benchmark guiado — tensor_strides

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

Matriz 256×256, matmul i-k-j (Release):

| Ordem / config | Tempo relativo (mediana) | Observação |
|----------------|-------------------------|------------|
| i-k-j (lab) | 1.0× baseline | reutiliza `A[i,k]` no loop interno |
| i-j-k | 1.2–2.5× mais lento | pior locality em B |
| transpose view | ~0 custo | só metadados |

Confirme checksum do resultado antes de comparar tempos. Em matrizes pequenas, ruído domina — use n≥256 e ≥5 repetições.
