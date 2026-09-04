# Benchmark guiado
Hipótese: pooling reduz alocações do backing `byte[]`, mas o wrapper `PooledFrame` ainda aloca um objeto gerenciado por operação neste milestone.

```bash
dotnet run -c Release --project starter/benchmarks/Chris.DotNet.Bench.Benchmarks
```
Registre versão do .NET, CPU, SO, modo Release, warmup e pelo menos 5 execuções. Compare depois com uma baseline que usa `new byte[required]`. Meça **tempo e bytes alocados**; não conclua com base em uma única métrica.
