# Benchmark guiado — agent loop FSM

## Protocolo

10 000 ciclos perceive→verify com replay.

```powershell
python days/2026-09-07/agent/loop_state_machine/benchmarks/bench.py
```

## Resultados observados

| Workload | Mediana (ms) |
|----------|-------------|
| 10000 loops | 11.556 |

Validação local 2026-09-07.
