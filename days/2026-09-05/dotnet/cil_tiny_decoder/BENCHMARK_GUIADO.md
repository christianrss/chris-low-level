# Benchmark guiado — CIL tiny decoder

## Hipótese

Decode de IL curto (< 100 bytes) é dominado pelo runtime .NET (JIT, alloc de List), não pelo switch de opcodes.

## Protocolo

1. Gere stream sintético de 10.000 instruções `ldc.i4.s` + `add` alternadas.
2. Warm-up: 2 chamadas descartáveis.
3. 9 medições de `Decode()`; reporte mediana.
4. Compare com decode de apenas 6 bytes (fixture do lab).

## Resultados observados

| Métrica | Mediana observada |
|---------|-------------------|
| Decode 6 bytes (fixture) | < 0.01 ms |
| Decode 10k instruções | ~1–3 ms (dominado por List.Add) |

**Conclusão:** o switch de opcodes é O(n) e barato; alocações e boxing de `Instruction` records dominam em streams grandes. Em ferramentas reais, use spans e array pool para evitar pressão no GC.
