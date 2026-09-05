# Benchmark guiado - CLVM

**Pergunta:** qual é o custo de interpretar uma pequena sequência de bytecode em um processo separado?

O benchmark de hoje é propositalmente simples e serve como baseline, não como medida definitiva do dispatch loop.

1. Compile Release.
2. Gere um programa determinístico.
3. Faça 5 execuções de aquecimento.
4. Faça pelo menos 30 execuções medidas.
5. Registre mediana e min/max.
6. Anote que criação de processo e I/O dominam programas muito curtos.

**Próximo experimento de pesquisa:** mover o benchmark para dentro do processo e comparar `switch`, computed-goto (quando disponível) e direct-threaded dispatch.

## Resultados observados

Ambiente de referência: Linux container, GCC 14.2, Python 3.13 (ver `benchmarks/results-2026-09-03.json`).

| Métrica | Valor referência | Notas |
|---------|------------------|-------|
| VM run median | ~1.18 ms | includes startup |

Valores são ordem de grandeza — **rerode na sua máquina** e registre mediana após warm-up.