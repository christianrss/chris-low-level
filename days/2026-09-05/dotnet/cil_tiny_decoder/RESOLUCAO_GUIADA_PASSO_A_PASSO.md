# RESOLUÇÃO GUIADA — .NET / CIL Tiny Decoder

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `CLR-IL-OPCODE-01` | `starter/Program.cs` | `CilDecoder.Decode` — casos `0x1F`, `0x58`, `0x2A` |
| `CLR-IL-OPERAND-02` | `starter/Program.cs` | operando `sbyte` após `0x1F` + truncamento |

Cada ID existe como `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` / `PEDAGOGY-TEST [ID]` no mesmo `Program.cs` (asserts em `Main`).

> Trabalhe em `days/2026-09-05/dotnet/cil_tiny_decoder/starter/`. `solutions/` é gabarito — consulte só depois da tentativa.

> Não comece copiando `solutions/`. Rode `dotnet run` após cada caso do switch.

---

## CLR-IL-OPCODE-01 — reconhecer opcodes

### 1. O problema (starter stub)

```csharp
// TODO [CLR-IL-OPCODE-01]: reconhecer ldc.i4.s, add e ret
// TODO [CLR-IL-OPERAND-02]: consumir int8 assinado após 0x1F
switch (opcode)
{
default:
    throw new InvalidDataException($"unsupported opcode 0x{opcode:X2}");
}
```

Bytecode do `Main`: `1F 05 1F 07 58 2A`. Com switch vazio, `0x1F` cai no `default` → `InvalidDataException`.

### 2. O algoritmo

```text
para cada byte opcode em code[i++]:
  0x58 → emitir Instruction(offset, "add", null)
  0x2A → emitir Instruction(offset, "ret", null)
  0x1F → (CLR-IL-OPERAND-02) ler sbyte e emitir "ldc.i4.s"
  outro → InvalidDataException
```

Tabela ECMA-335 (lab):

| Opcode | Nome | Tamanho |
|--------|------|---------|
| `0x1F` | `ldc.i4.s` | 1 + 1 (int8) |
| `0x58` | `add` | 1 |
| `0x2A` | `ret` | 1 |

### 3. Código completo (opcodes fixos + esqueleto ldc)

No `switch` de `CilDecoder.Decode` em `starter/Program.cs`:

```csharp
switch (opcode)
{
case 0x1F:
    // completar em CLR-IL-OPERAND-02
    if (i >= code.Length)
    {
        throw new InvalidDataException("truncated operand");
    }
    result.Add(new(offset, "ldc.i4.s", unchecked((sbyte)code[i++])));
    break;
case 0x58:
    result.Add(new(offset, "add", null));
    break;
case 0x2A:
    result.Add(new(offset, "ret", null));
    break;
default:
    throw new InvalidDataException($"unsupported opcode 0x{opcode:X2}");
}
```

(Implementar `0x1F` junto fecha os dois TODOs de uma vez — o starter marca ambos no mesmo switch.)

### 4. Por que funciona?

- `offset = i` **antes** do `code[i++]`: a instrução reporta o PC do opcode, não do operando.
- `add`/`ret` não consomem bytes extras; o `for` avança só pelo opcode.
- Opcode desconhecido continua no `default` — contrato defensivo do decoder.

### 5. Verificação parcial

```bash
dotnet run --project days/2026-09-05/dotnet/cil_tiny_decoder/starter/Chris.IlLab.csproj
```

Com `0x58`/`0x2A` só: ainda falha em `0x1F`. Com os três casos + operando: deve imprimir `OK CIL`.

---

## CLR-IL-OPERAND-02 — int8 assinado e truncamento

### 1. O problema

`ldc.i4.s` precisa de exatamente um byte após `0x1F`. Buffer `[0x1F]` sozinho deve lançar `InvalidDataException` (`truncated accepted` no `Main` se aceitar).

### 2. O algoritmo

```text
após ler opcode 0x1F:
  se i ≥ code.Length → InvalidDataException("truncated operand")
  operand ← (sbyte)code[i++]   // reinterpretar byte como signed
  emitir Instruction(offset, "ldc.i4.s", operand)
```

### 3. Código completo (caso `0x1F`)

```csharp
case 0x1F:
    if (i >= code.Length)
    {
        throw new InvalidDataException("truncated operand");
    }
    result.Add(new(offset, "ldc.i4.s", unchecked((sbyte)code[i++])));
    break;
```

### 4. Por que funciona?

- `i >= code.Length` após consumir o opcode: não há operando → falha explícita.
- `unchecked((sbyte)…)`: byte `0x05` → 5; byte `0xFF` → −1 (ECMA signed).
- `i++` no operando: o próximo opcode começa no byte seguinte (`0x58` após o segundo ldc).

### 5. Verificação

```bash
dotnet run --project days/2026-09-05/dotnet/cil_tiny_decoder/starter/Chris.IlLab.csproj
```

Saída esperada:

```text
OK CIL
```

Trace manual:

```text
1F 05 → ldc.i4.s 5   (offset 0)
1F 07 → ldc.i4.s 7   (offset 2)
58    → add          (offset 4)
2A    → ret          (offset 5)
Count = 4; [0].Operand = 5; [2].Name = "add"; [3].Name = "ret"
Decode([0x1F]) → InvalidDataException
```

Debug: se `Operand` for 5 mas Count ≠ 4, um caso não adiciona `Instruction`. Se truncado passa: falta o `if (i >= code.Length)`.

---

## Mapa de consistência auditada

- `CLR-IL-OPCODE-01` — `starter/Program.cs` → `solutions/Program.cs`.
- `CLR-IL-OPERAND-02` — `starter/Program.cs` → `solutions/Program.cs`.

## Relatório de resolução

### O que foi validado

- TODOs `CLR-IL-OPCODE-01` e `CLR-IL-OPERAND-02` no switch de `CilDecoder.Decode`.
- Asserts embutidos em `Main` (`PEDAGOGY-TEST`): 4 instruções, operando 5, `add`/`ret`, truncado rejeitado.
- Starter falha com `unsupported opcode 0x1F` até os casos existirem.

### Armadilhas encontradas

- Ler operando como `byte`/`int` sem cast `sbyte`.
- Esquecer checagem de truncamento.
- Usar `offset` depois de `i++` no opcode (offset errado).

### Depuração e saída esperada

- **Depuração:** imprima `offset`, `opcode:X2` e `result.Count` a cada iteração.
- **Saída esperada:** `OK CIL`.

### Próximo passo sugerido

Refazer o decoder sem a resolução. Depois meça throughput de decode em `BENCHMARK_GUIADO.md`.
