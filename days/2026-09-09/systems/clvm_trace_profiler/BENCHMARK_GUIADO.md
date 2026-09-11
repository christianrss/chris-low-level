# Benchmark guiado — Profiler de opcodes CLVM (C)

## Hipótese

A métrica `profile_code em 1e6 bytes sintéticos (ms)` permanece estável (±20%) em 3 corridas no mesmo hardware.

## Método

```powershell
ctest --test-dir days/2026-09-09/systems/clvm_trace_profiler/solutions/build_ci -C Release
```

Repita 3 vezes; anote tempo de parede ou a métrica específica do lab.

## Resultados observados

não executado neste ambiente na geração do dia — registre aqui: profile_code em 1e6 bytes sintéticos (ms).
