# Resolução guiada passo a passo — PE/CLI metadata

## Mapa exato starter → resolução
- `D2-CLR-CLI-RVA` → `starter/src/Chris.DotNet.Pe/CliPeInspector.cs`, dentro de `Inspect`.
- `D2-CLR-METADATA-RVA` → `starter/src/Chris.DotNet.Pe/CliPeInspector.cs`, dentro de `Inspect`.

O parser de DOS/PE, `DataDirectory[14]` e a função `RvaToOffset` **já vêm implementados como scaffolding**. Hoje você deve entendê-los e então conectar dois RVAs reais ao helper. A versão anterior dava a impressão de que você precisava implementar blocos que já estavam prontos; isso foi corrigido.

## 0. Leitura guiada do scaffolding
Abra `starter/src/Chris.DotNet.Pe/CliPeInspector.cs`.

Siga a ordem real de `Inspect`:
1. `MZ` em `image[0..2]`;
2. `e_lfanew` em `0x3C`;
3. assinatura `PE\0\0`;
4. COFF header e `SizeOfOptionalHeader`;
5. magic PE32/PE32+;
6. `DataDirectory[14]` (CLI Header);
7. section table;
8. CLI RVA → file offset;
9. metadata RVA → file offset;
10. assinatura `BSJB`.

No helper `RvaToOffset`, cada section fornece:
```csharp
var virtualSize = ReadU32(image, section + 8);
var virtualAddress = ReadU32(image, section + 12);
var rawSize = ReadU32(image, section + 16);
var rawPointer = ReadU32(image, section + 20);
var extent = Math.Max(virtualSize, rawSize);
```
Se `rva` está dentro da section:
```csharp
return checked((int)(rawPointer + (rva - virtualAddress)));
```
Não confunda RVA com file offset.

## 1. `D2-CLR-CLI-RVA`
Logo depois de:
```csharp
var sectionTable = optional + optionalSize;
```
substitua o TODO por:
```csharp
var cliOffset = RvaToOffset(image, cliRva, sectionTable, sectionCount);
```
Com a fixture: section VA `0x2000`, raw `0x200`, CLI RVA `0x2100` → offset `0x300`.

## 2. `D2-CLR-METADATA-RVA`
Depois de ler `metadataRva`/`metadataSize`, substitua o segundo TODO por:
```csharp
var metadataOffset = RvaToOffset(image, metadataRva, sectionTable, sectionCount);
```
Fixture: metadata RVA `0x2200` → offset `0x400`, onde devem existir os bytes de `BSJB`.

## 3. Teste
```bash
dotnet run --project starter/tests/Chris.DotNet.Pe.Tests
```
Esperado em ambiente com .NET 10 SDK:
```text
chris-dotnet-pe tests passed
```

O SDK .NET não está instalado no container desta auditoria; portanto, esta entrega registra **revisão estática**, não execução local desses testes.

## Debugging
Breakpoint em `RvaToOffset`. Anote `rva`, `virtualAddress`, `rawPointer`, `extent` e o offset retornado. Para `0x2200`, obter `0x2200` como file offset significa que você pulou a tradução RVA→section→raw.

## Solução final comentada
Compare apenas os dois marcadores `PEDAGOGY-SOLUTION` em `solutions/src/Chris.DotNet.Pe/CliPeInspector.cs`. Toda a infraestrutura necessária para chegar a esses pontos já existe no starter e foi explicitamente identificada acima.
