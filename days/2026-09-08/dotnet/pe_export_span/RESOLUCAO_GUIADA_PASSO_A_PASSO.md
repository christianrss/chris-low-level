# Resolução guiada — pe_export_span

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora | Substituir | Não mexer |
|---------|---------|-----------------|------------|-----------|
| `DN-PE-EXP-01` | `starter/PeExportSpan.cs` | `IsPeFile` | corpo sob `TODO [DN-PE-EXP-01]` | assinaturas e testes |
| `DN-PE-EXP-02` | `starter/PeExportSpan.cs` | `TryGetPeOffset` | corpo sob `TODO [DN-PE-EXP-02]` | assinaturas e testes |
| `DN-PE-EXP-03` | `starter/PeExportSpan.cs` | `TryReadExportRva` | corpo sob `TODO [DN-PE-EXP-03]` | assinaturas e testes |

## Baseline

```powershell
cd days/2026-09-08/dotnet/pe_export_span/starter
dotnet test
```

**Esperado antes dos TODOs:** FAIL (stub, NotImplemented, assert, ou retorno de erro).

Registre a mensagem de falha. Só avance quando souber qual TODO desbloqueia o Caso 1.

## DN-PE-EXP-01

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/PeExportSpan.cs` |
| Função / âncora | `IsPeFile` / comentário `TODO [DN-PE-EXP-01]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem IsPeFile, fixture MZ/PE é rejeitada.

### Algoritmo / trace

MZ + TryGetPeOffset + bytes PE\0\0.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```csharp
public static bool IsPeFile(ReadOnlySpan<byte> data)
    {
        // PEDAGOGY-SOLUTION: DN-PE-EXP-01
        if (data.Length < 0x40) return false;
        if (data[0] != (byte)'M' || data[1] != (byte)'Z') return false;
        if (!TryGetPeOffset(data, out int off)) return false;
        if (off + 4 > data.Length) return false;
        return data[off] == (byte)'P' && data[off + 1] == (byte)'E';
    }
```

### Por que funciona?

A rotina `IsPeFile` materializa o contrato de `DN-PE-EXP-01`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `DN-PE-EXP-01`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `DN-PE-EXP-01` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## DN-PE-EXP-02

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/PeExportSpan.cs` |
| Função / âncora | `TryGetPeOffset` / comentário `TODO [DN-PE-EXP-02]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem e_lfanew, o offset 0x80 não aparece.

### Algoritmo / trace

Read Int32 em 0x3C; valide bounds.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```csharp
public static bool TryGetPeOffset(ReadOnlySpan<byte> data, out int peOffset)
    {
        // PEDAGOGY-SOLUTION: DN-PE-EXP-02
        peOffset = 0;
        if (data.Length < 0x40) return false;
        peOffset = MemoryMarshal.Read<int>(data.Slice(0x3C, 4));
        return peOffset > 0 && peOffset + 4 <= data.Length;
    }
```

### Por que funciona?

A rotina `TryGetPeOffset` materializa o contrato de `DN-PE-EXP-02`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `DN-PE-EXP-02`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `DN-PE-EXP-02` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## DN-PE-EXP-03

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/PeExportSpan.cs` |
| Função / âncora | `TryReadExportRva` / comentário `TODO [DN-PE-EXP-03]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem data dir, export RVA 0x1000 não é lido.

### Algoritmo / trace

opt = pe+24; leia UInt32 em opt+0x78.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```csharp
public static bool TryReadExportRva(ReadOnlySpan<byte> data, out uint exportRva)
    {
        // PEDAGOGY-SOLUTION: DN-PE-EXP-03
        exportRva = 0;
        if (!IsPeFile(data) || !TryGetPeOffset(data, out int pe)) return false;
        int opt = pe + 4 + 20;
        if (opt + 0x78 + 8 > data.Length) return false;
        exportRva = MemoryMarshal.Read<uint>(data.Slice(opt + 0x78, 4));
        return true;
    }
```

### Por que funciona?

A rotina `TryReadExportRva` materializa o contrato de `DN-PE-EXP-03`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `DN-PE-EXP-03`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `DN-PE-EXP-03` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## Debug

| Sintoma | Causa provável | Correção |
|---------|----------------|----------|
| FAIL no Caso 1 | stub intacto / endian errado | releia o trace da TEORIA e o bloco do primeiro TODO |
| PASS parcial | size/estado desalinhado no TODO do meio | imprima pc/head/estado antes do assert |
| Crash / panic | bounds | valide Length/len antes de indexar |
| Diff de string | snprintf/format | compare caractere a caractere com o esperado |

## Relatório de resolução

| TODO | Horas | Maior bug | O que aprendia de novo |
|------|-------|-----------|------------------------|
| `DN-PE-EXP-01` |  |  |  |
| `DN-PE-EXP-02` |  |  |  |
| `DN-PE-EXP-03` |  |  |  |

Síntese (3–5 linhas): o que o wire-format/estado deste módulo força você a respeitar
que uma API de alto nível esconderia.
