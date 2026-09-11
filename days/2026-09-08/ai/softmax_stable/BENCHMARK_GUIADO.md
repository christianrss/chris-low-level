# Benchmark guiado — softmax_stable

## Hipótese

A implementação correta é O(n) no tamanho da entrada (bytes, eventos ou estados visitados)
e não aloca além do buffer de saída.

## Medição

| Métrica | Como medir | Meta |
|---------|------------|------|
| Tempo Caso 1 | `Measure-Command` / timer do runner | estável ±20% |
| Tempo input ×10 | repetir fixture | ≈ linear |
| Starter incompleto | baseline | FAIL rápido |

## Procedimento

1. Rode solutions (PASS) e anote tempo wall-clock.
2. Rode starter incompleto (FAIL) — não otimize stubs.
3. Compare com o módulo-irmão se existir (C vs Rust, .NET vs Python).

## Resultados observados

| Run | Ambiente | Tempo / notas |
|-----|----------|---------------|
| 1 | _preencher_ | |
| 2 | _preencher_ | |
| 3 | _preencher_ | |

## Interpretação

Se ×10 input não ≈ ×10 tempo, procure trabalho quadratic (re-concat em loop,
walk `i++` ineficiente). Registre conclusões no Relatório de resolução.
