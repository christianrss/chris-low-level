# chris-dotnet-pe
Parser educacional de PE/CLI escrito em C# sem usar Reflection para descobrir o layout. Milestone 1 valida DOS/PE, localiza o CLI data directory, converte RVA para file offset pelas section headers e valida a assinatura `BSJB` do metadata root.

```bash
dotnet build
dotnet run --project tests/Chris.DotNet.Pe.Tests
```

A fonte normativa principal para a parte CLI é ECMA-335, especialmente Partition II (metadata physical layout).
