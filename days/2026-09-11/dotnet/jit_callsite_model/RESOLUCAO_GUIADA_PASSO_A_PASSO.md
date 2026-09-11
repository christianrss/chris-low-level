# Resolucao guiada — jit_callsite_model

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D9-DN-VIRT` | `starter/CallSite.cs` | `Dispatch` |
| `D9-DN-DEVIRT` | `starter/CallSite.cs` | `DevirtDog` |
| `D9-DN-TYPE` | `starter/CallSite.cs` | `IsExactDog` |


## Baseline

```powershell
cd days/2026-09-11/dotnet/jit_callsite_model/starter
dotnet test tests/Chris.JitLab.Tests.csproj
```

**Esperado antes dos TODOs:** FAIL.


## D9-DN-VIRT

### Onde colocar (D9-DN-VIRT)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/CallSite.cs` |
| Funcao | `Dispatch` |
| Substituir | corpo sob `TODO [D9-DN-VIRT]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-DN-VIRT` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-DN-VIRT`.

### Escreva o codigo

```csharp
        return a.Speak();
    }
    public static string DevirtDog(Dog d) {
        return d.Speak();
    }
    public static bool IsExactDog(Animal a) {
        return a.GetType() == typeof(Dog);
    }
```

### Por que funciona?
Materializa o contrato numerico de `D9-DN-VIRT`.

### Verifique
Baseline parcial; `D9-DN-VIRT` PASS.

### Checkpoint
- [ ] `D9-DN-VIRT` PASS

## D9-DN-DEVIRT

### Onde colocar (D9-DN-DEVIRT)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/CallSite.cs` |
| Funcao | `DevirtDog` |
| Substituir | corpo sob `TODO [D9-DN-DEVIRT]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-DN-DEVIRT` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-DN-DEVIRT`.

### Escreva o codigo

```csharp
        return d.Speak();
    }
    public static bool IsExactDog(Animal a) {
        return a.GetType() == typeof(Dog);
    }
}
```

### Por que funciona?
Materializa o contrato numerico de `D9-DN-DEVIRT`.

### Verifique
Baseline parcial; `D9-DN-DEVIRT` PASS.

### Checkpoint
- [ ] `D9-DN-DEVIRT` PASS

## D9-DN-TYPE

### Onde colocar (D9-DN-TYPE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/CallSite.cs` |
| Funcao | `IsExactDog` |
| Substituir | corpo sob `TODO [D9-DN-TYPE]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-DN-TYPE` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-DN-TYPE`.

### Escreva o codigo

```csharp
        return a.GetType() == typeof(Dog);
    }
}
```

### Por que funciona?
Materializa o contrato numerico de `D9-DN-TYPE`.

### Verifique
Baseline parcial; `D9-DN-TYPE` PASS.

### Checkpoint
- [ ] `D9-DN-TYPE` PASS

## Debug

| Sintoma | Causa | Correcao |
|---------|-------|----------|
| stub | corpo intacto | cole o bloco |
| off-by-one | size | refaca trace |

## Relatorio de resolucao

- TODOs:
- Saida:
- Invariantes:
- Benchmark: nao executado
