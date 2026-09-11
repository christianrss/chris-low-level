# Resolucao guiada — channel_backpressure

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D7-DN-CHANNEL` | `starter/Pipeline.cs` | `RunAsync` |
| `D7-DN-PRODUCER` | `starter/Pipeline.cs` | `RunAsync` |
| `D7-DN-CONSUMER` | `starter/Pipeline.cs` | `RunAsync` |


## Baseline

```powershell
cd days/2026-09-09/dotnet/channel_backpressure/starter
dotnet test tests/Chris.ChannelLab.Tests.csproj
```

**Esperado antes dos TODOs:** FAIL.


## D7-DN-CHANNEL

### Onde colocar (D7-DN-CHANNEL)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/Pipeline.cs` |
| Funcao | `RunAsync` |
| Substituir | corpo sob `TODO [D7-DN-CHANNEL]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-DN-CHANNEL` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```csharp
        var channel=Channel.CreateBounded<int>(new BoundedChannelOptions(capacity){FullMode=BoundedChannelFullMode.Wait,SingleWriter=true,SingleReader=true});
        int checksum=0, seen=0;
        var producer=Task.Run(async ()=>{
            try { for(int i=0;i<count;i++) await channel.Writer.WriteAsync(i); }
            finally { channel.Writer.Complete(); }
        });
        var consumer=Task.Run(async ()=>{
            await foreach(var item in channel.Reader.ReadAllAsync()){ checksum+=item; seen++; await Task.Yield(); }
```

### Por que funciona?
Materializa o contrato numerico de `D7-DN-CHANNEL`.

### Verifique
Baseline parcial; `D7-DN-CHANNEL` PASS.

### Checkpoint
- [ ] `D7-DN-CHANNEL` PASS

## D7-DN-PRODUCER

### Onde colocar (D7-DN-PRODUCER)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/Pipeline.cs` |
| Funcao | `RunAsync` |
| Substituir | corpo sob `TODO [D7-DN-PRODUCER]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-DN-PRODUCER` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```csharp
        var producer=Task.Run(async ()=>{
            try { for(int i=0;i<count;i++) await channel.Writer.WriteAsync(i); }
            finally { channel.Writer.Complete(); }
        });
        var consumer=Task.Run(async ()=>{
            await foreach(var item in channel.Reader.ReadAllAsync()){ checksum+=item; seen++; await Task.Yield(); }
        });
        await Task.WhenAll(producer,consumer);
```

### Por que funciona?
Materializa o contrato numerico de `D7-DN-PRODUCER`.

### Verifique
Baseline parcial; `D7-DN-PRODUCER` PASS.

### Checkpoint
- [ ] `D7-DN-PRODUCER` PASS

## D7-DN-CONSUMER

### Onde colocar (D7-DN-CONSUMER)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/Pipeline.cs` |
| Funcao | `RunAsync` |
| Substituir | corpo sob `TODO [D7-DN-CONSUMER]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-DN-CONSUMER` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```csharp
        var consumer=Task.Run(async ()=>{
            await foreach(var item in channel.Reader.ReadAllAsync()){ checksum+=item; seen++; await Task.Yield(); }
        });
        await Task.WhenAll(producer,consumer);
        return (checksum,seen);
    }
}
```

### Por que funciona?
Materializa o contrato numerico de `D7-DN-CONSUMER`.

### Verifique
Baseline parcial; `D7-DN-CONSUMER` PASS.

### Checkpoint
- [ ] `D7-DN-CONSUMER` PASS

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
