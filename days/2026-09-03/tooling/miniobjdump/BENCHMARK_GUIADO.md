# Benchmark guiado - MiniObjdump

**Pergunta:** qual é o custo de abrir, validar e inspecionar um binário pequeno?

Faça 5 aquecimentos e 30 repetições. Registre tempo por execução e tamanho do arquivo. Como o programa imprime muito texto, documente que terminal/stdout influencia a medida. Um próximo benchmark deve separar parse/decode da renderização textual.

## Resultados observados

Ambiente de referência: Linux container, GCC 14.2, Python 3.13 (ver `benchmarks/results-2026-09-03.json`).

| Métrica | Valor referência | Notas |
|---------|------------------|-------|
| Disasm median | ~1.28 ms | includes startup |

Valores são ordem de grandeza — **rerode na sua máquina** e registre mediana após warm-up.