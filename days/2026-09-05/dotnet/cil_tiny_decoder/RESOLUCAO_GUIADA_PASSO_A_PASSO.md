# Resolução guiada passo a passo — .NET/CLR: tiny CIL decoder

Abra `starter/Program.cs`, método `Decode`.

No switch do opcode, mapeie:
```csharp
case 0x1F: // ldc.i4.s
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
default:
    throw new InvalidDataException($"unsupported opcode 0x{op:X2}");
```
`CLR-IL-OPCODE-01` cobre o dispatch; `CLR-IL-OPERAND-02` cobre bounds/sinal do operand.

Quando houver SDK .NET:
```bash
dotnet run --project starter/Chris.IlLab.csproj
```
Esperado: três instruções para bytes `1F 05 1F 07 58 2A` na verdade quatro instruções: dois loads, add, ret. O programa faz asserts internos e imprime `OK CIL`.

Debug: acompanhe `i`, `offset`, `op`; um operand deve avançar `i` uma segunda vez.

## Mapa de consistência auditada
- `CLR-IL-OPCODE-01` — starter → resolução → teste → solution.
- `CLR-IL-OPERAND-02` — starter → resolução → teste → solution.
