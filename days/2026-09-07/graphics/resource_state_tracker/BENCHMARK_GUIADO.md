# Benchmark guiado — resource state tracker

Lab headless — simula batch de barriers (sem janela Win32).

## Protocolo

1M transições register/transition/flush no harness C++.

```powershell
cmake -S days/2026-09-07/graphics/resource_state_tracker/solutions -B build-gfx-state
cmake --build build-gfx-state --config Release
ctest --test-dir build-gfx-state -C Release
```

## Resultados observados

| Workload | Tempo (ms) | Repetições |
|----------|-----------|------------|
| 1M transitions | 18.179 | 1 |

Validação local 2026-09-07.
