# Resolucao guiada — gc_allocation_probe

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D6-DN-ALLOC` | `starter/Chris.GcProbe/Probe.cs` | `static` |
| `D6-DN-NEW` | `starter/Chris.GcProbe/Probe.cs` | `static` |
| `D6-DN-POOL` | `starter/Chris.GcProbe/Probe.cs` | `static` |


## Baseline

```powershell
cd days/2026-09-08/dotnet/gc_allocation_probe/starter
dotnet test
```

**Esperado antes dos TODOs:** FAIL.


## D6-DN-ALLOC

### Onde colocar (D6-DN-ALLOC)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/Chris.GcProbe/Probe.cs` |
| Funcao | `static` |
| Substituir | corpo sob `TODO [D6-DN-ALLOC]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-DN-ALLOC` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-DN-ALLOC` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```csharp
PEDAGOGY-SOLUTION: D6-DN-ALLOC
  work(); long before=GC.GetAllocatedBytesForCurrentThread(); int checksum=work(); long after=GC.GetAllocatedBytesForCurrentThread(); return(after-before,checksum);
 }
 public static int BuildWithNew(int iterations){
  // 
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-DN-ALLOC`.

### Verifique
Rode o baseline; o caminho de `D6-DN-ALLOC` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-DN-ALLOC` PASS
- [ ] Nao alterei o teste

## D6-DN-NEW

### Onde colocar (D6-DN-NEW)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/Chris.GcProbe/Probe.cs` |
| Funcao | `static` |
| Substituir | corpo sob `TODO [D6-DN-NEW]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-DN-NEW` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-DN-NEW` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```csharp
PEDAGOGY-SOLUTION: D6-DN-NEW
  int sum=0; for(int i=0;i<iterations;i++){var buffer=new byte[256];buffer[0]=(byte)i;sum+=buffer[0];}return sum;
 }
 public static int BuildWithPool(int iterations){
  // 
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-DN-NEW`.

### Verifique
Rode o baseline; o caminho de `D6-DN-NEW` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-DN-NEW` PASS
- [ ] Nao alterei o teste

## D6-DN-POOL

### Onde colocar (D6-DN-POOL)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/Chris.GcProbe/Probe.cs` |
| Funcao | `static` |
| Substituir | corpo sob `TODO [D6-DN-POOL]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-DN-POOL` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-DN-POOL` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```csharp
PEDAGOGY-SOLUTION: D6-DN-POOL
  int sum=0; for(int i=0;i<iterations;i++){var buffer=ArrayPool<byte>.Shared.Rent(256);try{var span=buffer.AsSpan(0,256);span[0]=(byte)i;sum+=span[0];}finally{ArrayPool<byte>.Shared.Return(buffer,false);}}return sum;
 }
}
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-DN-POOL`.

### Verifique
Rode o baseline; o caminho de `D6-DN-POOL` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-DN-POOL` PASS
- [ ] Nao alterei o teste

## Debug

| Sintoma | Causa | Correcao |
|---------|-------|----------|
| stub | corpo intacto | cole o bloco do TODO |
| off-by-one | size/indice | refaca o trace |
| 2o caso falha | estado residual | reset |

## Relatorio de resolucao

- TODOs concluidos:
- Comandos + saida:
- Invariantes:
- Edge cases:
- Benchmark: nao executado / preencher
