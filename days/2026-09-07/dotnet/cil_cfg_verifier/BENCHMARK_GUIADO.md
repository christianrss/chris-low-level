# Benchmark guiado — CIL CFG verifier

## Protocolo

Verificar métodos CIL sintéticos com branches e merges; medir tempo de `Verify`.

```powershell
dotnet run --project days/2026-09-07/dotnet/cil_cfg_verifier/benchmarks/Bench.csproj
```

## Resultados observados

| Workload | Status |
|----------|--------|
| CFG worklist típico | Não executado — SDK `dotnet` ausente no CI Linux; código revisado estruturalmente |

Reexecutar no Windows com SDK instalado.
