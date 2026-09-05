# Resolução guiada passo a passo — PE/CLI metadata

## Mapa exato starter → resolução

- `D2-CLR-CLI-RVA` → `starter/src/Chris.DotNet.Pe/CliPeInspector.cs`, dentro de `Inspect`.
- `D2-CLR-METADATA-RVA` → `starter/src/Chris.DotNet.Pe/CliPeInspector.cs`, dentro de `Inspect`.

O parser de DOS/PE, `DataDirectory[14]` e a função `RvaToOffset` **já vêm implementados como scaffolding**. Seu trabalho é conectar dois RVAs ao helper existente e validar BSJB.

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
8. **CLI RVA → file offset** ← TODO 1;
9. metadata RVA → file offset ← TODO 2;
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

**Não confunda RVA com file offset.**

## 1. Entender a fixture de teste

O teste constrói imagem PE mínima em memória:

| Campo | Valor |
|-------|------:|
| Section VirtualAddress | 0x2000 |
| PointerToRawData | 0x200 |
| CLI Header RVA | 0x2100 |
| Metadata RVA | 0x2200 |

Cálculos esperados:

```text
cliOffset     = 0x200 + (0x2100 - 0x2000) = 0x300
metadataOffset = 0x200 + (0x2200 - 0x2000) = 0x400
```

No offset `0x400`, os quatro bytes devem ser `42 53 4A 42` (`BSJB`).

## 2. `D2-CLR-CLI-RVA`

Localize o comentário TODO logo após:

```csharp
var sectionTable = optional + optionalSize;
```

Substitua `var cliOffset = 0;` por:

```csharp
var cliOffset = RvaToOffset(image, cliRva, sectionTable, sectionCount);
```

Depois disso, `RequireRange(image, cliOffset, 16)` passa a apontar para bytes reais do CLI header — não para o início do arquivo.

Leia então:

```csharp
var metadataRva = ReadU32(image, cliOffset + 8);
var metadataSize = ReadU32(image, cliOffset + 12);
```

### Por que funciona?
`cliRva` é endereço virtual na imagem mapeada; o disco armazena bytes em `PointerToRawData + (rva - VirtualAddress)`. Sem `RvaToOffset`, você leria lixo do DOS header ou offset zero.

## 3. `D2-CLR-METADATA-RVA`

Substitua `var metadataOffset = 0;` por:

```csharp
var metadataOffset = RvaToOffset(image, metadataRva, sectionTable, sectionCount);
```

### Por que funciona?
O CLI header em `cliOffset+8` guarda o RVA do metadata root — segunda conversão pela mesma section table. Fixture espera offset `0x400` com assinatura `BSJB` (`0x424A5342`); confundir RVA com file offset falha essa checagem mesmo com RVA correto.

## 4. Verificação estática antes do teste

Checklist manual:

- [ ] `cliRva != 0` foi validado antes da conversão
- [ ] `sectionCount` veio do COFF header
- [ ] `RvaToOffset` lança se RVA cai fora de todas sections
- [ ] `metadataOffset` é usado no retorno `CliImageInfo`

Compare com `solutions/src/Chris.DotNet.Pe/CliPeInspector.cs` nos blocos `PEDAGOGY-SOLUTION`.

## 5. Teste

```bash
dotnet run --project starter/tests/Chris.DotNet.Pe.Tests
```

Saída esperada em ambiente com .NET 10 SDK:

```text
chris-dotnet-pe tests passed
```

## 6. Debugging

Breakpoint em `RvaToOffset`. Para cada section anote:

```text
i, virtualAddress, extent, rawPointer
```

Quando `rva = 0x2100`, a section com VA `0x2000` deve ser escolhida.

Se o retorno for `0x2100` (igual ao RVA), você esqueceu de chamar `RvaToOffset`.

Se `BSJB` falhar mas offset parece certo, inspecione bytes no hex editor — talvez `metadataRva` foi lido de `cliOffset` errado.

## 7. Erros observados em turmas anteriores

1. **Deixar `cliOffset = 0`** — lê metadata RVA do DOS header.
2. **Usar `cliRva` direto em `RequireRange`** — passa no range check por acidente em imagens grandes, falha em outras.
3. **Section extent = virtualSize apenas** — ignora `rawSize` maior (dados válidos no disco).
4. **Esquecer `checked`** — overflow silencioso em PE fuzzed.

## 8. Mapa de consistência auditada

- `D2-CLR-CLI-RVA` — starter → resolução → `PEDAGOGY-TEST` → `PEDAGOGY-SOLUTION`.
- `D2-CLR-METADATA-RVA` — starter → resolução → `PEDAGOGY-TEST` → `PEDAGOGY-SOLUTION`.

## Solução final comentada

Compare apenas os dois marcadores `PEDAGOGY-SOLUTION` em `solutions/src/Chris.DotNet.Pe/CliPeInspector.cs`. Toda infraestrutura necessária já existe no starter.

## Relatório de resolução

- **TODOs concluídos:** `D2-CLR-CLI-RVA`, `D2-CLR-METADATA-RVA`
- **Comandos de teste:**
  ```bash
  dotnet run --project starter/tests/Chris.DotNet.Pe.Tests
  ```
- **Saída esperada:** `chris-dotnet-pe tests passed`
- **Invariantes verificadas:** RVA→offset via section table; assinatura BSJB no metadata root; bounds check antes de cada leitura
- **Edge cases testados:** fixture sintética com single section; CLI directory ausente rejeitado pelo scaffolding
- **Benchmark:** hipótese — custo de `Inspect()` cresce linearmente com número de sections; ver `BENCHMARK_GUIADO.md`
- **Toolchain não executada:** SDK .NET ausente no container de auditoria — revisão estática aplicada; execute localmente com .NET 10 SDK
