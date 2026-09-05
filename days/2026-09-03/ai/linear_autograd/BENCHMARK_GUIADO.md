# Benchmark guiado - IA low-level

**Pergunta:** qual o custo do mesmo treinamento escalar em Python e C?

1. Use o mesmo dataset, número de épocas e algoritmo.
2. Não inclua compilação no tempo medido.
3. Faça aquecimento.
4. Repita a função Python várias vezes e meça `perf_counter_ns`.
5. Para C, rode o executável várias vezes, mas registre que o custo de processo contamina a comparação.
6. Em um experimento futuro, exponha o kernel C por FFI ou execute múltiplos treinos por processo.

O objetivo de hoje é aprender a identificar um benchmark imperfeito e documentar a limitação.

## Resultados observados

Ambiente de referência: Linux container, GCC 14.2, Python 3.13 (ver `benchmarks/results-2026-09-03.json`).

| Métrica | Valor referência | Notas |
|---------|------------------|-------|
| Python train step | ~0.51 ms | 50 runs median |

Valores são ordem de grandeza — **rerode na sua máquina** e registre mediana após warm-up.