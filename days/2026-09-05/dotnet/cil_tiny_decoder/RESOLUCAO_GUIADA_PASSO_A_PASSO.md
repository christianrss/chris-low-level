# Resolução guiada passo a passo — .NET — CIL Tiny Decoder

## Mapa exato starter → resolução

- `CLR-IL-OPCODE-01` → `starter/Program.cs` (`CilDecoder.Decode` — casos `0x1F`, `0x58`, `0x2A`)
- `CLR-IL-OPERAND-02` → `starter/Program.cs` (`CilDecoder.Decode` — leitura de `sbyte` após `0x1F` + rejeição de truncamento)

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST [ID]` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-05/dotnet/cil_tiny_decoder/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

## 0. Preparar o projeto

Na raiz do repositório:

```bash
dotnet run --project days/2026-09-05/dotnet/cil_tiny_decoder/starter/Chris.IlLab.csproj
```

O build deve funcionar. A execução **deve falhar** com `InvalidDataException` (opcode `0x1F` cai no `default` do `switch` vazio) ou `Exception: decode count`. Esse é o baseline.

## `CLR-IL-OPCODE-01` — reconhecer ldc.i4.s, add e ret

### Arquivo

Abra:

```text
starter/Program.cs
```

Localize o `switch (opcode)` dentro de `CilDecoder.Decode` e substitua o bloco `default` isolado por casos completos:

```csharp
switch (opcode)
{
case 0x1F:
    // operando preenchido no passo CLR-IL-OPERAND-02
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

### Por que funciona?

`0x58` e `0x2A` são opcodes de tamanho fixo (1 byte). O decoder registra o offset do opcode e avança `i` implicitamente na próxima iteração do `for`.

### Verificação manual

Após implementar só `add` e `ret` (sem `ldc` completo), o decode do buffer de teste ainda falha — falta o caso `0x1F`. Isso confirma que os três casos são necessários.

### Checkpoint

Você ainda não deve ver `OK CIL` até completar o operando de `ldc.i4.s`.

---

## `CLR-IL-OPERAND-02` — operando int8 após 0x1F

### Arquivo

No mesmo `switch`, complete o caso `0x1F`:

```csharp
case 0x1F:
    if (i >= code.Length)
    {
        throw new InvalidDataException("truncated operand");
    }
    result.Add(new(offset, "ldc.i4.s", unchecked((sbyte)code[i++])));
    break;
```

### Por que funciona?

`ldc.i4.s` exige exatamente 1 byte de operando logo após o opcode. `unchecked((sbyte)...)` reinterpreta o byte como signed (-128..127). A checagem `i >= code.Length` garante que `[0x1F]` sozinho lance exceção.

### Verificação manual

```text
Decode([0x1F, 0x05, 0x1F, 0x07, 0x58, 0x2A])
→ 4 instruções
→ [0].Operand == 5
→ [2].Name == "add"
→ [3].Name == "ret"

Decode([0x1F]) → InvalidDataException
```

### Checkpoint

```bash
dotnet run --project days/2026-09-05/dotnet/cil_tiny_decoder/starter/Chris.IlLab.csproj
```

Saída esperada:

```text
OK CIL
```

---

## Rode os testes novamente

O próprio `Program.Main` embute os asserts pedagógicos (não há projeto de teste separado). Confirme:

1. `instructions.Count == 4`
2. `instructions[0].Operand == 5`
3. `instructions[2].Name == "add"`
4. Buffer truncado `[0x1F]` lança `InvalidDataException`

## Como depurar se falhar

- `decode count`: `ldc.i4.s` não adiciona instrução ou operando lido errado — conte instruções no trace manual.
- `truncated accepted`: falta `if (i >= code.Length)` antes de ler operando.
- Operand negativo inesperado: você leu como `byte` em vez de `sbyte`.
- `unsupported opcode 0x1F`: caso `0x1F` ainda cai no `default`.

## Solução final comentada

Compare `starter/Program.cs` com `solutions/Program.cs`. Justifique: ordem de leitura, `unchecked` para signed, e separação entre opcodes com e sem operando.

## Relatório de resolução

| ID | Arquivo | Resultado esperado |
|----|---------|-------------------|
| CLR-IL-OPCODE-01 | `Program.cs` | `0x58`→`add`, `0x2A`→`ret`; desconhecido lança |
| CLR-IL-OPERAND-02 | `Program.cs` | `0x1F`+byte → `ldc.i4.s` com `sbyte`; truncado lança |

Critério de aceite: `dotnet run` imprime `OK CIL` sem exceção.

### Template do relatório

```
Aluno:
Módulo: .NET — CIL Tiny Decoder
Data:

1. TODOs: CLR-IL-OPCODE-01, CLR-IL-OPERAND-02
2. Primeira falha: [ex.: InvalidDataException em 0x1F]
3. Correção aplicada: [ex.: switch com casos + leitura sbyte]
4. Evidência: [colar saída OK CIL]
```
