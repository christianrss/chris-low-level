# Benchmark guiado — ActivitySource e spans (.NET)

## Hipótese

A métrica `1e5 StartWorkSpan+Export` permanece estável (±20%) em 3 corridas no mesmo hardware.

## Método

```powershell
dotnet test days/2026-09-09/dotnet/activity_source_span/solutions
```

Repita 3 vezes; anote tempo de parede ou a métrica específica do lab.

## Resultados observados

não executado neste ambiente na geração do dia — registre aqui: 1e5 StartWorkSpan+Export.
