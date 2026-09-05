# Testes guiados

O `Main` da solution decodifica `1F 05 1F 07 58 2A` e verifica quatro instruções: dois loads, add e ret. Também é recomendável testar `1F FF` e stream truncado `1F`. Neste ambiente, a ausência de `dotnet` é registrada em `VALIDATION_DAY03.md`; não fingimos execução.