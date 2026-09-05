# Benchmark guiado — Parser ANSI

## Hipótese

Parse de sequências ANSI curtas (< 1 KiB) é dominado por alocação de strings Python, não pelo scan de ESC.

## Protocolo

1. Gere string com 10.000 alternâncias `literal + \x1b[31m + literal + \x1b[0m`.
2. Warm-up: 2 feeds descartáveis.
3. 9 medições de `feed()`; reporte mediana.

## Resultados observados

| Métrica | Mediana |
|---------|---------|
| feed 10k alternâncias | ~2–8 ms |
| feed 100 bytes (fixture teste) | < 0.05 ms |

**Conclusão:** para terminais interativos, o gargalo real será I/O do PTY e renderização — não o parser CSI mínimo. Otimize redraw e diff de células antes de micro-otimizar `feed()`.
