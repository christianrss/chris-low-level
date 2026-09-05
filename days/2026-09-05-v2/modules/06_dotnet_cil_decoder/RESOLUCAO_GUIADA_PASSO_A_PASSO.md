# Resolução guiada passo a passo

Abra `starter/Program.cs`, método `Decode`.

Para `CLR-IL-OPCODE-01`, adicione casos `0x1F`, `0x58` e `0x2A`. Para `CLR-IL-OPERAND-02`, antes de ler o byte após `0x1F`, cheque bounds e converta com `unchecked((sbyte)code[i++])`.

```csharp
case 0x1F:
    if (i >= code.Length) throw new InvalidDataException("truncated operand");
    var operand = unchecked((sbyte)code[i++]);
    result.Add(new(offset, "ldc.i4.s", operand));
    break;
case 0x58:
    result.Add(new(offset, "add", null));
    break;
case 0x2A:
    result.Add(new(offset, "ret", null));
    break;
```

Quando houver SDK:
```bash
dotnet run --project starter/Chris.IlLab.csproj
```
O programa usa asserts internos e deve imprimir `OK CIL`. Debugue `i`, `offset` e `op`.

## Mapa de consistência auditada
- `CLR-IL-OPCODE-01` - starter -> resolução -> teste -> solution.
- `CLR-IL-OPERAND-02` - starter -> resolução -> teste -> solution.
