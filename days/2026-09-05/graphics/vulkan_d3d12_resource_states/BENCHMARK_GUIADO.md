# Benchmark guiado — Resource states

## Hipótese

Validação de transições em CPU (`ResourceTracker`) é gratuita frente ao custo de `vkCmdPipelineBarrier` ou `ResourceBarrier` na GPU real.

## Protocolo

1. Execute 1 milhão de `transition()` válidas em loop.
2. Compare com 1 milhão de chamadas `to_vulkan()`.
3. Mediana de 9 runs.

## Resultados observados

| Métrica | Mediana |
|---------|---------|
| 1M transitions (CPU) | < 5 ms |
| 1M to_vulkan() | < 3 ms |
| Barreira GPU real (ref.) | 10–100 µs cada |

**Conclusão:** otimize batching de barreiras na GPU, não o tracker educacional. Em engines reais, reduzir número de barriers por frame é ganho mensurável; o mapa de strings é custo zero.
