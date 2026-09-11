# Benchmark guiado — Máscara causal de atenção (C)

## Hipótese

A métrica `1e7 chamadas causal_mask` permanece estável (±20%) em 3 corridas no mesmo hardware.

## Método

```powershell
ctest --test-dir days/2026-09-09/ai/attention_mask/solutions/build_ci -C Release
```

Repita 3 vezes; anote tempo de parede ou a métrica específica do lab.

## Resultados observados

não executado neste ambiente na geração do dia — registre aqui: 1e7 chamadas causal_mask.
