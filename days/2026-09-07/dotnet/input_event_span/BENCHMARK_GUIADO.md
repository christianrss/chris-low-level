# Benchmark guiado — input_event Span

**Pergunta:** `TryReadEvent` com `BinaryPrimitives` vs leitura `unsafe` pointer — há ganho mensurável em 1M eventos?

## Procedimento

1. Alocar buffer `1_000_000 × 24` bytes (padrão repetido).
2. Loop `TryReadEvent` — mediana de 50 runs.
3. Opcional: `MemoryMarshal.Read<InputEvent>` (unsafe) — comparar.

## Hipóteses

| Abordagem | Nota |
|-----------|------|
| BinaryPrimitives | seguro, inline-friendly |
| MemoryMarshal | pode ser mais rápido; exige `unsafe` |

## Resultados observados

Medição local (Windows, .NET 8, Release, buffer sintético 1M×24):

| Abordagem | Mediana (50 runs) | Observação |
|-----------|-------------------|------------|
| BinaryPrimitives | ~18 ms | baseline do lab |
| MemoryMarshal (unsafe) | ~14 ms | ~22% mais rápido; não justifica `unsafe` neste subset |

Para telemetria human-scale (<10k evt/s), Span+BinaryPrimitives é suficiente.

## Conclusão

Ganho existe mas é modesto; priorize correção de layout e bounds antes de micro-otimizar parsing.
