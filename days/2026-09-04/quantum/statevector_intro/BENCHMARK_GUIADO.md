# Benchmark guiado — statevector_intro

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

| Qubits | Amplitudes | Memória state (~) | Gates/s (H repetido) |
|-------:|-----------:|------------------:|---------------------:|
| 10 | 1 024 | 16 KiB | alto |
| 16 | 65 536 | 1 MiB | médio |
| 20 | 1 048 576 | 16 MiB | baixo |

Cada qubit adicional ~dobra memória e reduz gates/s — comportamento esperado O(2^n). Norma deve permanecer 1.0 após sequência de gates; desvio indica bug em H/CNOT, não ruído de benchmark.
