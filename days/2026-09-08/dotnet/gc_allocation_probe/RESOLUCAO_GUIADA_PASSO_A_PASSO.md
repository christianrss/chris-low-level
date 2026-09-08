# Resolução guiada passo a passo — GC allocation probe

Edite `starter/Chris.GcProbe/Probe.cs`.

### TODO D6-DN-ALLOC
`MeasureAllocated(Func<int> work)`:
```csharp
work(); // warm-up
long before=GC.GetAllocatedBytesForCurrentThread();
int checksum=work();
long after=GC.GetAllocatedBytesForCurrentThread();
return (after-before, checksum);
```

### TODO D6-DN-NEW
No caminho `BuildWithNew`, para cada iteração:
```csharp
var buffer=new byte[256];
buffer[0]=(byte)i;
checksum += buffer[0];
```

### TODO D6-DN-POOL
Rent uma vez por iteração dentro de try/finally:
```csharp
var buffer=ArrayPool<byte>.Shared.Rent(256);
try { var span=buffer.AsSpan(0,256); ... }
finally { ArrayPool<byte>.Shared.Return(buffer, clearArray:false); }
```
O teste exige checksum igual e alocações do caminho pool menores após warm-up, mas com tolerância para runtime.
Execute `dotnet run --project starter/Chris.GcProbe.Tests` se SDK existir. Se não existir, não declare execução.
