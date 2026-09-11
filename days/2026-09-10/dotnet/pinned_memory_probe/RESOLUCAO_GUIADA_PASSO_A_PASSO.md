# Resolucao guiada — pinned_memory_probe

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D8-DN-PIN` | `starter/Pinned.cs` | `SumPinned` |
| `D8-DN-LEN` | `starter/Pinned.cs` | `SumPinned` |
| `D8-DN-SUM` | `starter/Pinned.cs` | `SumPinned` |

## Baseline

```powershell
cd days/2026-09-10/dotnet/pinned_memory_probe/starter
dotnet test tests/Chris.PinnedLab.Tests.csproj
```

**Esperado antes dos TODOs:** FAIL.

## D8-DN-PIN

### Onde colocar (D8-DN-PIN)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/Pinned.cs` |
| Funcao | `SumPinned` |
| Substituir | corpo sob `TODO [D8-DN-PIN]` |
| Nao mexer | assinatura / testes |

### O problema
Sem pin, o GC pode mover o array enquanto o ponteiro e usado.

### Algoritmo / trace
1. `GCHandle.Alloc(data, Pinned)`.
2. Guarde o handle para `Free` no finally.
3. Nao some ainda — so estabilize a memoria.

### Escreva o codigo

```csharp
var handle = GCHandle.Alloc(data, GCHandleType.Pinned);
try {
    // next TODOs use handle / data
} finally {
    handle.Free();
}
```

### Por que funciona?
Pinned impede relocacao do objeto pelo GC durante o bloco.

### Verifique
Baseline parcial; `D8-DN-PIN` PASS.

### Checkpoint
- [ ] `D8-DN-PIN` PASS

## D8-DN-LEN

### Onde colocar (D8-DN-LEN)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/Pinned.cs` |
| Funcao | `SumPinned` |
| Substituir | corpo sob `TODO [D8-DN-LEN]` |
| Nao mexer | assinatura / testes |

### O problema
Sem `n = data.Length` o loop nao sabe o bound.

### Algoritmo / trace
1. Leia Length uma vez.
2. Use `n` no for (nao reconsultar Length a cada iteracao).
3. Confira com fixture `{1,2,3}` → n=3.

### Escreva o codigo

```csharp
int n = data.Length;
if (n < 0) {
    throw new InvalidOperationException("len");
}
```

### Por que funciona?
Fixa o bound antes da soma — contrato do assert de comprimento.

### Verifique
Baseline parcial; `D8-DN-LEN` PASS.

### Checkpoint
- [ ] `D8-DN-LEN` PASS

## D8-DN-SUM

### Onde colocar (D8-DN-SUM)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/Pinned.cs` |
| Funcao | `SumPinned` |
| Substituir | corpo sob `TODO [D8-DN-SUM]` |
| Nao mexer | assinatura / testes |

### O problema
Sem acumular bytes o teste espera soma errada.

### Algoritmo / trace
1. `s = 0`.
2. Para i em [0,n): `s += data[i]`.
3. Retorne s (ex.: 1+2+3=6).

### Escreva o codigo

```csharp
int s = 0;
for (int i = 0; i < n; i++) {
    s += data[i];
}
return s;
```

### Por que funciona?
Soma linear dos bytes no intervalo pinado.

### Verifique
Baseline completo; `D8-DN-SUM` PASS.

### Checkpoint
- [ ] `D8-DN-SUM` PASS

## Debug

| Sintoma | Causa | Correcao |
|---------|-------|----------|
| AccessViolation | Free cedo | Free so no finally |
| soma 0 | loop vazio | confira n |
| GC move | sem Alloc | PIN primeiro |

## Relatorio de resolucao

- TODOs concluidos:
- Comandos + saida:
- Invariantes: pin enquanto le
- Edge cases: array vazio
- Benchmark: nao executado
