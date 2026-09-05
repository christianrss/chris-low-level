# Testes guiados — csharp_span_arraypool

Este arquivo é a ponte entre cada TODO real do `starter/` e a evidência que deve ficar verde. Não pule diretamente para `solutions/`.

## Baseline

A partir da pasta deste módulo:

```bash
dotnet run --project starter/tests/Chris.DotNet.Bench.Tests
```

**Antes de implementar:** não executado neste container porque o SDK .NET não está instalado; em máquina com .NET 10 o starter deve falhar nos asserts/contratos enquanto incompleto.

## Mapa TODO → teste

### `D2-CSHARP-WRITE-HEADER`
- Arquivo: `starter/src/Chris.DotNet.Buffers/FrameCodec.cs`
- Validação: round-trip grava `PayloadLength` e `MessageType` little-endian e rejeita destino curto.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-CSHARP-WRITE-HEADER`

### `D2-CSHARP-READ-HEADER`
- Arquivo: `starter/src/Chris.DotNet.Buffers/FrameCodec.cs`
- Validação: round-trip reconstrói exatamente `FrameHeader(1234,7)`.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-CSHARP-READ-HEADER`

### `D2-CSHARP-RENT-FRAME`
- Arquivo: `starter/src/Chris.DotNet.Buffers/FrameCodec.cs`
- Validação: frame contém header+payload; helper de ownership fornecido invalida `Memory` após Dispose.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-CSHARP-RENT-FRAME`

## Depois de concluir

Rode novamente o mesmo comando. Resultado esperado:

- `chris-dotnet-bench tests passed` em ambiente com .NET 10 SDK.
- Não remova/afrouxe asserts para “fazer passar”.
- Compare com `solutions/` somente depois de seu starter ficar verde.
- Acrescente pelo menos um edge case próprio e anote qual regressão ele detectaria.
