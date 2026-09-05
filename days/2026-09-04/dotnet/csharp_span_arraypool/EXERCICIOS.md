# Exercícios — Span, ArrayPool e frame binário

## Fácil

- **D2-CSHARP-WRITE-HEADER:** implemente `WriteHeader` em `FrameCodec.cs` escrevendo `PayloadLength` e `MessageType` em little-endian.
- No papel, encode manualmente header com `PayloadLength=100` e `MessageType=7`; confira bytes `64 00 00 00 07 00 00 00`.

## Médio

- **D2-CSHARP-READ-HEADER:** implemente `ReadHeader` decodificando os dois campos sem alocar arrays novos.
- Explique por que `Span<byte>` é `ref struct` e o impacto em métodos `async`.

## Difícil

- **D2-CSHARP-RENT-FRAME:** implemente `RentFrame` com `ArrayPool`, header + cópia de payload e transferência via `PooledFrame`.
- Leia `PooledFrame.Dispose` no starter e explique o papel de `Interlocked.Exchange`.

## Desafio

- Rode `dotnet run -c Release --project starter/benchmarks/Chris.DotNet.Bench.Benchmarks` e compare com baseline `new byte[]`.
- Proponha extensão com checksum CRC32 após o header sem quebrar alinhamento de 8 bytes.
