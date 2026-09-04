# Resolução guiada passo a passo

Abra `starter/src/Chris.DotNet.Pe/CliPeInspector.cs`.

## 1. Fácil — DOS e PE
Valide os dois primeiros bytes:
```csharp
if (image[0] != (byte)'M' || image[1] != (byte)'Z')
    throw new InvalidDataException("missing MZ signature");
```
Leia `e_lfanew` no offset `0x3C`:
```csharp
var peOffset = checked((int)ReadU32(image, 0x3C));
```
No offset resultante, confirme `PE\\0\\0`.

## 2. Médio — localizar DataDirectory[14]
Depois do COFF header, obtenha `SizeOfOptionalHeader` e leia o magic. Para PE32+ (`0x20B`), o array de data directories começa em `optional + 112`; para PE32 (`0x10B`), em `optional + 96`.

```csharp
var directoryStart = magic switch {
    0x10B => optional + 96,
    0x20B => optional + 112,
    _ => throw new InvalidDataException("unsupported PE optional-header magic")
};
var cliEntry = directoryStart + 14 * 8;
```
Cada entry tem RVA + Size, 4 bytes cada.

## 3. Difícil — RVA para offset
Localize `RvaToOffset`. Em cada section leia:
```csharp
var virtualSize = ReadU32(image, section + 8);
var virtualAddress = ReadU32(image, section + 12);
var rawSize = ReadU32(image, section + 16);
var rawPointer = ReadU32(image, section + 20);
var extent = Math.Max(virtualSize, rawSize);
```
Se o RVA estiver nessa faixa:
```csharp
return checked((int)(rawPointer + (rva - virtualAddress)));
```

## 4. CLI → Metadata
No CLI Header, metadata directory fica nos offsets +8/+12:
```csharp
var metadataRva = ReadU32(image, cliOffset + 8);
var metadataSize = ReadU32(image, cliOffset + 12);
```
Mapeie o RVA e valide:
```csharp
if (ReadU32(image, metadataOffset) != 0x424A5342)
    throw new InvalidDataException("metadata root does not start with BSJB");
```

## 5. Teste
```bash
dotnet run --project starter/tests/Chris.DotNet.Pe.Tests
```
Esperado:
```text
chris-dotnet-pe tests passed
```

## Debugging
Use uma fixture pequena. Pare em `RvaToOffset` e anote `rva`, `virtualAddress`, `rawPointer` e o offset calculado. Se você obtiver 0x2200 como offset de arquivo, confundiu RVA com file offset.

> O SDK .NET não está presente no container desta entrega; o parser foi revisado estaticamente e o projeto de teste foi incluído, mas não executado localmente.
