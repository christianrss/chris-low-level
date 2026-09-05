# Benchmark guiado — Bytecode branch VM

## Hipótese

Interpretação de bytecode puro é 10–100× mais lenta que JS nativo no V8 — mas para poucas instruções, o overhead é irrelevante.

## Protocolo

1. Programe loop de 1 milhão de iterações com `PUSH`/`JZ`/`JMP`.
2. Compare com equivalente em JS nativo (`for` loop).
3. 2 warm-ups + 9 medições; mediana.

## Resultados observados

| Métrica | Mediana |
|---------|---------|
| VM 6 instruções × 1 | < 0.01 ms |
| VM loop 100k steps | ~5–15 ms |
| JS nativo equivalente 100k | ~0.1 ms |

**Conclusão:** branches em VM educacional são corretos para aprender controle de fluxo; performance real exige JIT (como Ignition/TurboFan no V8). O custo por instrução inclui dispatch do `switch` e alocação de objetos `{op, arg}`.
