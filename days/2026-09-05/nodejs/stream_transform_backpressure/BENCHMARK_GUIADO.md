# Benchmark guiado — Node streams

## Hipótese

Respeitar backpressure mantém uso de memória estável; ignorar `drain` aumenta buffer interno e latência em sinks lentos.

## Protocolo

1. Execute `runBackpressureDemo()` 9 vezes após 2 warm-ups.
2. Registre `falseWrites` e tempo total.
3. Compare com versão que ignora `drain` (não faça em produção).

## Resultados observados

| Métrica | Com drain | Sem drain (anti-pattern) |
|---------|-----------|--------------------------|
| `falseWrites` | 40–48 (varia) | 0 |
| Memória pico Writable | ~highWaterMark × 2 | cresce com 50×8B |
| Tempo total | ~100–150 ms | ~50 ms (mas arriscado) |

**Conclusão:** aguardar `drain` adiciona latência mas garante pressão de memória controlada. Em pipes reais (HTTP, disco), ignorar backpressure causa OOM em cargas assimétricas.
