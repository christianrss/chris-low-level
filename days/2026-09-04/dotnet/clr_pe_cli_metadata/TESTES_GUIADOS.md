# Testes guiados — clr_pe_cli_metadata

Este arquivo é a ponte entre cada TODO real do `starter/` e a evidência que deve ficar verde. Não pule diretamente para `solutions/`.

## Baseline

A partir da pasta deste módulo:

```bash
dotnet run --project starter/tests/Chris.DotNet.Pe.Tests
```

**Antes de implementar:** não executado neste container porque o SDK .NET não está instalado; em máquina com .NET 10 o starter deve falhar no mapeamento RVA.

## Mapa TODO → teste

### `D2-CLR-CLI-RVA`
- Arquivo: `starter/src/Chris.DotNet.Pe/CliPeInspector.cs`
- Validação: CLI RVA `0x2100` deve mapear para file offset `0x300`.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-CLR-CLI-RVA`

### `D2-CLR-METADATA-RVA`
- Arquivo: `starter/src/Chris.DotNet.Pe/CliPeInspector.cs`
- Validação: metadata RVA `0x2200` deve mapear para `0x400` e conter `BSJB`.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-CLR-METADATA-RVA`

## Depois de concluir

Rode novamente o mesmo comando. Resultado esperado:

- `chris-dotnet-pe tests passed` em ambiente com .NET 10 SDK.
- Não remova/afrouxe asserts para “fazer passar”.
- Compare com `solutions/` somente depois de seu starter ficar verde.
- Acrescente pelo menos um edge case próprio e anote qual regressão ele detectaria.
