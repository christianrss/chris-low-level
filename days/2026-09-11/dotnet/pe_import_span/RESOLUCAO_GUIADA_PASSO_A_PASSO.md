# Resolução guiada — pe_import_span

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `DOTNET-IMP-01` | `starter/PeImportSpan.cs` | `IsPeFile` |
| `DOTNET-IMP-02` | `starter/PeImportSpan.cs` | `TryGetPeOffset` |
| `DOTNET-IMP-03` | `starter/PeImportSpan.cs` | `TryReadImportRva` |

## Baseline

```powershell
// contexto: substitua o corpo sob o TODO
dotnet test days/2026-09-11/dotnet/pe_import_span/starter/tests/Chris.PeLab.Tests.csproj
// fim do corpo; preserve a assinatura
```

**Esperado:** FAIL.

## DOTNET-IMP-01

### Onde colocar (DOTNET-IMP-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/PeImportSpan.cs` |
| Função | `IsPeFile` |
| Substituir | o corpo sob o comentário `TODO [DOTNET-IMP-01]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Precisa MZ+PE verdadeiros.

### Algoritmo / trace

Cheque MZ; pe offset; bytes PE.

### Escreva o código

```csharp
    if (data.Length < 0x40) return false;
    if (data[0] != (byte)'M' || data[1] != (byte)'Z') return false;
    if (!TryGetPeOffset(data, out int off)) return false;
    if (off + 4 > data.Length) return false;
    return data[off] == (byte)'P' && data[off + 1] == (byte)'E';
```

### Por que funciona?

Mesma validação do lab export.

### Verifique

IsPeFile(MinimalPe())==true.

### Código completo alinhado ao solutions/ (DOTNET-IMP-01)

```csharp
PEDAGOGY-SOLUTION: DOTNET-IMP-01
        if (data.Length < 0x40) return false;
        if (data[0] != (byte)'M' || data[1] != (byte)'Z') return false;
        if (!TryGetPeOffset(data, out int off)) return false;
        if (off + 4 > data.Length) return false;
        return data[off] == (byte)'P' && data[off + 1] == (byte)'E';
    }
    public static bool TryGetPeOffset(ReadOnlySpan<byte> data, out int peOffset)
    {
        // 
```

## DOTNET-IMP-02

### Onde colocar (DOTNET-IMP-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/PeImportSpan.cs` |
| Função | `TryGetPeOffset` |
| Substituir | o corpo sob o comentário `TODO [DOTNET-IMP-02]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

e_lfanew deve ser 0x80.

### Algoritmo / trace

MemoryMarshal.Read<int> em 0x3C.

### Escreva o código

```csharp
    peOffset = 0;
    if (data.Length < 0x40) return false;
    peOffset = MemoryMarshal.Read<int>(data.Slice(0x3C, 4));
    return peOffset > 0 && peOffset + 4 <= data.Length;
```

### Por que funciona?

Campo DOS clássico.

### Verifique

off==0x80.

### Código completo alinhado ao solutions/ (DOTNET-IMP-02)

```csharp
PEDAGOGY-SOLUTION: DOTNET-IMP-02
        peOffset = 0;
        if (data.Length < 0x40) return false;
        peOffset = MemoryMarshal.Read<int>(data.Slice(0x3C, 4));
        return peOffset > 0 && peOffset + 4 <= data.Length;
    }
    public static bool TryReadImportRva(ReadOnlySpan<byte> data, out uint importRva)
    {
        // 
```

## DOTNET-IMP-03

### Onde colocar (DOTNET-IMP-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/PeImportSpan.cs` |
| Função | `TryReadImportRva` |
| Substituir | o corpo sob o comentário `TODO [DOTNET-IMP-03]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Import RVA = 0x2000, não o export 0x1000 do dia 08.

### Algoritmo / trace

opt=pe+24; leia uint em opt+0x78+8.

### Escreva o código

```csharp
    importRva = 0;
    if (!IsPeFile(data) || !TryGetPeOffset(data, out int pe)) return false;
    int opt = pe + 4 + 20;
    if (opt + 0x78 + 16 > data.Length) return false;
    importRva = MemoryMarshal.Read<uint>(data.Slice(opt + 0x78 + 8, 4));
    return true;
```

### Por que funciona?

dir[1] = dir[0]+8 bytes.

### Verifique

rva==0x2000.

### Código completo alinhado ao solutions/ (DOTNET-IMP-03)

```csharp
PEDAGOGY-SOLUTION: DOTNET-IMP-03
        importRva = 0;
        if (!IsPeFile(data) || !TryGetPeOffset(data, out int pe)) return false;
        int opt = pe + 4 + 20; // optional header start
        // PE32+ magic 0x20B at opt+0; import dir is data directory[1] at opt+0x78+8
        if (opt + 0x78 + 16 > data.Length) return false;
        importRva = MemoryMarshal.Read<uint>(data.Slice(opt + 0x78 + 8, 4));
        return true;
    }
}
```

## Debug

| Sintoma | Correção |
|---------|----------|
| 0x1000 | leu export |

## Relatório de resolução

- TODOs: [ ]
