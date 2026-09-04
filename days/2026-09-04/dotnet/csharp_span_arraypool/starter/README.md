# chris-dotnet-bench

Laboratório cumulativo de C#/.NET voltado a APIs de baixo nível e performance de produção. O primeiro milestone implementa framing binário com `Span<byte>`, `BinaryPrimitives` e `ArrayPool<byte>` sem depender de pacotes externos.

## Milestone 1
- header de 8 bytes: `payload_length:int32 LE` + `message_type:int32 LE`;
- encode/decode por `Span`/`ReadOnlySpan`;
- owner de buffer alugado com `IDisposable`;
- self-tests sem framework externo;
- benchmark simples com `Stopwatch` e `GC.GetAllocatedBytesForCurrentThread`.

## Build

```bash
dotnet build
```

## Tests

```bash
dotnet run --project tests/Chris.DotNet.Bench.Tests
```

## Benchmark

```bash
dotnet run -c Release --project benchmarks/Chris.DotNet.Bench.Benchmarks
```

Este projeto usa apenas BCL. O alvo é `net10.0` para acompanhar a LTS atual; o código do milestone usa APIs maduras e fáceis de portar para versões anteriores.
