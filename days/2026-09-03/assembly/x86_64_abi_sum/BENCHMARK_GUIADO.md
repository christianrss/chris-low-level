# Benchmark guiado - Assembly x86-64 e ABI

1. Defina o que esta sendo medido; nao misture startup, I/O e algoritmo sem perceber.
2. Use Release/otimizacao quando aplicavel.
3. Execute warm-up quando runtime/cache puderem alterar primeiras iteracoes.
4. Repita; preserve mediana e variacao quando fizer sentido.
5. Registre CPU, OS, compilador/runtime, flags e tamanho da entrada.
6. Compare uma mudanca por vez.
7. O benchmark de referencia esta em `projects/chris-assembly-lab/benchmarks/` quando existe.

## Resultados observados

Ambiente de referência: Linux container, GCC 14.2, Python 3.13 (ver `benchmarks/results-2026-09-03.json`).

| Métrica | Valor referência | Notas |
|---------|------------------|-------|
| C vs ASM loop | 0.012s vs 0.024s | ASM slower at tiny N |

Valores são ordem de grandeza — **rerode na sua máquina** e registre mediana após warm-up.