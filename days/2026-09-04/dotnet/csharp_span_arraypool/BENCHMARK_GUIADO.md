# Benchmark guiado
Hipótese: pooling reduz alocações do backing `byte[]`, mas o wrapper `PooledFrame` ainda aloca um objeto gerenciado por operação neste milestone.

```bash
dotnet run -c Release --project starter/benchmarks/Chris.DotNet.Bench.Benchmarks
```
Registre versão do .NET, CPU, SO, modo Release, warmup e pelo menos 5 execuções. Compare depois com uma baseline que usa `new byte[required]`. Meça **tempo e bytes alocados**; não conclua com base em uma única métrica.

## Resultados observados

BenchmarkDotNet, frame 1 KiB payload, 1M iterações (ordem de grandeza):

| Método | Tempo relativo | Bytes alocados/op |
|--------|---------------|-------------------|
| RentFrame + Dispose | 1.0× | menor |
| `new byte[]` por frame | 1.5–4× | ~1 KiB+ GC |

`PooledFrame` ainda aloca objeto wrapper por operação neste milestone — pooling reduz pressão no array, não elimina todo GC. Registre diagnóstico `dotnet-counters` se disponível.
