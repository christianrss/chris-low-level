# RESOLUÇÃO GUIADA — .NET / PE, CLI Header e metadata BSJB

## Mapa exato starter → resolução

| TODO ID | Starter | Função/área |
|---------|---------|-------------|
| `D2-CLR-CLI-RVA` | `starter/src/Chris.DotNet.Pe/CliPeInspector.cs` | `Inspect` — `cliOffset = RvaToOffset(...)` |
| `D2-CLR-METADATA-RVA` | `starter/src/Chris.DotNet.Pe/CliPeInspector.cs` | `Inspect` — `metadataOffset = RvaToOffset(...)` |

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-04/dotnet/clr_pe_cli_metadata/starter/`. `solutions/` é gabarito.

O parser DOS/PE, `DataDirectory[14]` e `RvaToOffset` **já vêm no scaffolding**. Seu trabalho é conectar dois RVAs ao helper e deixar a checagem `BSJB` ler bytes reais.

---

## Leitura guiada do scaffolding

Abra `starter/src/Chris.DotNet.Pe/CliPeInspector.cs`. Ordem real de `Inspect`:

1. `MZ` em `image[0..2]`;
2. `e_lfanew` em `0x3C`;
3. assinatura `PE\0\0`;
4. COFF + `SizeOfOptionalHeader`;
5. magic PE32 / PE32+;
6. `DataDirectory[14]` → `cliRva`, `cliSize`;
7. section table em `optional + optionalSize`;
8. **CLI RVA → file offset** ← TODO 1;
9. lê metadata RVA/size no CLI header;
10. **metadata RVA → file offset** ← TODO 2;
11. assinatura `BSJB` (`0x424A5342`).

### Helper `RvaToOffset` (já implementado — leia, não reescreva)

Para cada section de 40 bytes:

```csharp
var virtualSize = ReadU32(image, section + 8);
var virtualAddress = ReadU32(image, section + 12);
var rawSize = ReadU32(image, section + 16);
var rawPointer = ReadU32(image, section + 20);
var extent = Math.Max(virtualSize, rawSize);
```

Se `rva` ∈ `[virtualAddress, virtualAddress + extent)`:

```csharp
return checked((int)(rawPointer + (rva - virtualAddress)));
```

**RVA ≠ file offset.** Confundir os dois é o bug clássico deste lab.

---

## Fixture mental do teste

| Campo | Valor |
|-------|------:|
| Section `VirtualAddress` | `0x2000` |
| `PointerToRawData` | `0x200` |
| CLI Header RVA | `0x2100` |
| Metadata RVA | `0x2200` |

```text
cliOffset      = 0x200 + (0x2100 - 0x2000) = 0x300
metadataOffset = 0x200 + (0x2200 - 0x2000) = 0x400
```

No offset `0x400`, quatro bytes = `42 53 4A 42` (`BSJB`).

---

## Exercício Médio — `D2-CLR-CLI-RVA`

### 1. O problema

Após montar `sectionTable`, o starter faz:

```csharp
var cliOffset = 0;
RequireRange(image, cliOffset, 16);
var metadataRva = ReadU32(image, cliOffset + 8);
```

Com `cliOffset = 0` você lê “metadata RVA” a partir do DOS header — lixo que pode até passar em alguns tamanhos de imagem por acidente.

### 2. O algoritmo

```text
cliOffset = RvaToOffset(image, cliRva, sectionTable, sectionCount)
RequireRange(image, cliOffset, 16)     # já no starter
metadataRva  = ReadU32(image, cliOffset + 8)
metadataSize = ReadU32(image, cliOffset + 12)
```

Layout mínimo do CLI header usado aqui:

```text
+0  cb
+4  MajorRuntimeVersion
+6  MinorRuntimeVersion
+8  Metadata RVA      ← o que você precisa
+12 Metadata Size
```

### 3. Escreva o código

Substitua `var cliOffset = 0;` por:

```csharp
var cliOffset = RvaToOffset(image, cliRva, sectionTable, sectionCount);
```

As linhas `RequireRange` / `ReadU32` seguintes **já estão** no starter — não as remova.

### 4. Por que funciona

`cliRva` é endereço relativo à imagem **carregada**. No disco, a section começa em `PointerToRawData`. A fórmula `raw + (rva - VA)` mapeia o mesmo byte. Sem conversão, `RequireRange(image, 0, 16)` “funciona” mas aponta para `MZ`, não para o CLI header.

Trace da fixture: `rva=0x2100`, `VA=0x2000`, `raw=0x200` → offset `0x300`.

### 5. Verifique

Ainda sem o segundo TODO, `metadataOffset = 0` fará a checagem BSJB olhar o início do arquivo. Avance.

---

## Exercício Difícil — `D2-CLR-METADATA-RVA`

### 1. O problema

```csharp
var metadataOffset = 0;
RequireRange(image, metadataOffset, 4);
if (ReadU32(image, metadataOffset) != 0x424A5342) ...
```

Mesmo com `metadataRva` correto lido do CLI header, sem converter RVA→offset a assinatura nunca aparece onde você procura.

### 2. O algoritmo

```text
metadataOffset = RvaToOffset(image, metadataRva, sectionTable, sectionCount)
RequireRange(..., 4)
ReadU32 == 0x424A5342   # 'B','S','J','B' em LE como u32
return CliImageInfo(...)
```

### 3. Escreva o código

Substitua `var metadataOffset = 0;` por:

```csharp
var metadataOffset = RvaToOffset(image, metadataRva, sectionTable, sectionCount);
```

### 4. Por que funciona

Segunda conversão pela **mesma** section table. Fixture: `0x2200 → 0x400`. O uint32 `0x424A5342` é BSJB little-endian (`42 53 4A 42` na ordem de bytes do arquivo).

Erros de turma:

1. Deixar `cliOffset = 0` — metadata RVA lido do DOS stub.
2. Usar `cliRva` direto em `RequireRange` — range pode “passar” em imagens grandes.
3. `extent = virtualSize` só — ignora `rawSize` maior.
4. Esquecer `checked` no helper — overflow silencioso em PE fuzzed (o helper já usa `checked`).

### 5. Verifique

```bash
dotnet run --project starter/tests/Chris.DotNet.Pe.Tests
```

Esperado:

```text
chris-dotnet-pe tests passed
```

Checklist estático antes:

- [ ] `cliRva != 0` validado pelo scaffolding
- [ ] `sectionCount` veio do COFF
- [ ] `RvaToOffset` lança se RVA fora de todas sections
- [ ] `metadataOffset` entra no `CliImageInfo` retornado

---

## Debugging

Breakpoint em `RvaToOffset`. Para cada section anote:

```text
i, virtualAddress, extent, rawPointer
```

Quando `rva = 0x2100`, a section com VA `0x2000` deve ser escolhida.

| Sintoma | Causa |
|---------|-------|
| Retorno `== rva` (ex. `0x2100`) | esqueceu `RvaToOffset` |
| BSJB falha, offset “parece” certo | `metadataRva` veio de `cliOffset` errado |
| Falha só em PE32+ | directory start errado no scaffolding — não mexa; reporte |

Ambiente sem SDK: revisão estática vs `solutions/`; execute com .NET 10 SDK.

---

## Mapa de consistência auditada

- `D2-CLR-CLI-RVA` — starter → resolução → `PEDAGOGY-TEST` → `PEDAGOGY-SOLUTION`
- `D2-CLR-METADATA-RVA` — starter → resolução → `PEDAGOGY-TEST` → `PEDAGOGY-SOLUTION`

Compare apenas os dois marcadores em `solutions/src/Chris.DotNet.Pe/CliPeInspector.cs`.

---

## Relatório de resolução

### O que foi validado

- CLI RVA e metadata RVA convertidos via section table.
- Assinatura BSJB no metadata root.
- Bounds check antes de cada leitura (`RequireRange`).

### Armadilhas encontradas

- Tratar RVA como file offset.
- Ler campos do CLI a partir do offset 0.
- Assumir `virtualSize` sozinho como extent da section.

### Depuração e saída esperada

- **Depuração:** trace `RvaToOffset` com a tabela da fixture; hex em `0x400`.
- **Saída esperada:** `chris-dotnet-pe tests passed`.

### Próximo passo sugerido

Em `BENCHMARK_GUIADO.md`, meça `Inspect()` com 1/10/100 sections e teste a hipótese de custo linear da busca sequencial — só otimize depois de provar que importa.
