# Benchmark guiado — Telemetria de arena bump (C++)

## Hipótese

A métrica `1e6 alloc(8)+reset ciclos` permanece estável (±20%) em 3 corridas no mesmo hardware.

## Método

```powershell
ctest --test-dir days/2026-09-09/systems/arena_telemetry/solutions/build_ci -C Release
```

Repita 3 vezes; anote tempo de parede ou a métrica específica do lab.

## Resultados observados

não executado neste ambiente na geração do dia — registre aqui: 1e6 alloc(8)+reset ciclos.
