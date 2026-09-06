## Mapa exato starter → resolução

| TODO ID | Starter |
|---------|--------|
| — | — |

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
## Relatório de resolução

- **TODOs concluídos:** (liste os IDs implementados)
- **Comandos de teste:**
  ```bash
  # cole aqui o comando exato usado
  ```
- **Saída esperada:** PASS nos testes do módulo
- **Invariantes verificadas:** (liste)
- **Edge cases testados:** (liste)
- **Benchmark:** hipótese + resultado ou declaração honesta de skip
- **Toolchain não executada:** (se aplicável)

### 4. Por que funciona

O stub no âncora TODO é substituído pelo comportamento testado.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.


## `CLR-IL-OPCODE-01`

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/Program.cs` |
| **Função / âncora** | `TODO [CLR-IL-OPCODE-01]` |
| **Substituir** | stub marcado por esse TODO |
| **Não mexer** | outros arquivos até este ID passar |

### Escreva o código

```text
# Implemente conforme starter/Program.cs e compare solutions/Program.cs
```

### Por que funciona

A edição no arquivo certo faz o `PEDAGOGY-TEST: CLR-IL-OPCODE-01` passar.
