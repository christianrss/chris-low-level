# Benchmark guiado - Drivers: descriptor rings

1. Defina o que esta sendo medido; nao misture startup, I/O e algoritmo sem perceber.
2. Use Release/otimizacao quando aplicavel.
3. Execute warm-up quando runtime/cache puderem alterar primeiras iteracoes.
4. Repita; preserve mediana e variacao quando fizer sentido.
5. Registre CPU, OS, compilador/runtime, flags e tamanho da entrada.
6. Compare uma mudanca por vez.
7. O benchmark de referencia esta em `projects/chris-driver-lab/benchmarks/` quando existe.

## Resultados observados

Ambiente de referência: Linux container, GCC 14.2, Python 3.13 (ver `benchmarks/results-2026-09-03.json`).

| Métrica | Valor referência | Notas |
|---------|------------------|-------|
| Descriptors/s | ~104M | 2M completed |

Valores são ordem de grandeza — **rerode na sua máquina** e registre mediana após warm-up.