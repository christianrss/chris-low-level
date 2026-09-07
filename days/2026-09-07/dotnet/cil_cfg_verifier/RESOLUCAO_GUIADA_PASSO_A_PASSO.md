# Resolução guiada — CIL CFG verifier

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `D5-CIL-DECODE` | `starter/Chris.CilCfg/Verifier.cs` | `Verify` — loop decode |
| `D5-CIL-WORKLIST` | `starter/Chris.CilCfg/Verifier.cs` | `Verify` — propagação depth |
| `D5-CIL-MERGE` | `starter/Chris.CilCfg/Verifier.cs` | `Verify` — join compatibility |

Marcadores: `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` em `solutions/Chris.CilCfg/Verifier.cs`, testes em `starter/Chris.CilCfg.Tests/Program.cs`.

> Edite `starter/Chris.CilCfg/Verifier.cs`. Adicione `using` necessários no topo do arquivo.

## Baseline

```powershell
cd days/2026-09-07/dotnet/cil_cfg_verifier
dotnet run --project starter/Chris.CilCfg.Tests
```

**Esperado:** FAIL — `Verify` retorna 0; teste espera `2` no método válido.

---

## D5-CIL-DECODE — decode subset e successors

### O problema

Stub retorna `0` sem decodificar. Precisamos mapear cada offset de instrução a pops/pushes/successors antes de qualquer dataflow.

Stub:

```csharp
public static int Verify(byte[] code) {
 // TODO [D5-CIL-DECODE]: decode subset e successors.
 return 0;
}
```

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/Chris.CilCfg/Verifier.cs` |
| **Função / âncora** | `Verify` — comentário `TODO [D5-CIL-DECODE]` |
| **Substituir** | corpo que retorna 0 pelo decode completo |
| **Inserir** | `record Ins(...)` e usings `System`, `System.Collections.Generic` no topo |
| **Não mexer** | projeto de testes |

### Código — decode (worklist stub temporário return 0 após decode)

```csharp
record Ins(int Off, int Size, int Pops, int Pushes, int[] Succ);
var ins = new Dictionary<int, Ins>();
int ip = 0;
while (ip < code.Length) {
    int o = ip;
    byte op = code[ip++];
    int pops = 0, push = 0;
    int[] succ;
    if (op == 0x20) {
        if (ip + 4 > code.Length) throw new InvalidDataException();
        ip += 4; push = 1; succ = new[] { ip };
    } else if (op == 0x58) {
        pops = 2; push = 1; succ = new[] { ip };
    } else if (op == 0x2B || op == 0x2D) {
        if (ip >= code.Length) throw new InvalidDataException();
        sbyte d = unchecked((sbyte)code[ip++]);
        int t = ip + d;
        pops = op == 0x2D ? 1 : 0;
        succ = op == 0x2D ? new[] { t, ip } : new[] { t };
    } else if (op == 0x2A) {
        pops = 1; succ = Array.Empty<int>();
    } else throw new InvalidDataException($"opcode {op:X2}");
    ins[o] = new Ins(o, ip - o, pops, push, succ);
}
// worklist virá no próximo TODO — por ora return 0 falha teste ok
return 0;
```

### Por que funciona?

- `o` captura início da instrução; `ip` avança operandos — size = `ip - o`.
- `ldc.i4` exige 4 bytes após opcode; successor é fallthrough.
- Branch short: delta relativo a `ip` **depois** de consumir operando.
- `brtrue.s` tem dois successors; `br.s` só target.

### Verificação parcial

Inspecione `ins` com breakpoint após decode do array ok — deve haver 4 entradas nos offsets 0,6,12,13.

---

## D5-CIL-WORKLIST — propagar profundidade

### O problema

Decode sozinho não calcula stack. Teste válido exige retorno `2` (duas ldc empilhadas antes de add).

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/Chris.CilCfg/Verifier.cs` |
| **Função / âncora** | após loop decode — `TODO [D5-CIL-WORKLIST]` |
| **Substituir** | `return 0` temporário |
| **Inserir** | dicionário depth + Queue |

### Código — worklist (merge simplificado: sempre atribui)

```csharp
var depth = new Dictionary<int, int> { { 0, 0 } };
var q = new Queue<int>(); q.Enqueue(0);
int max = 0;
while (q.Count > 0) {
    int o = q.Dequeue();
    if (!ins.TryGetValue(o, out var x)) throw new InvalidDataException("target not instruction");
    int d = depth[o];
    if (d < x.Pops) throw new InvalidDataException("underflow");
    int od = d - x.Pops + x.Pushes;
    max = Math.Max(max, od);
    foreach (var s in x.Succ) {
        if (s == code.Length) throw new InvalidDataException("fallthrough past end");
        if (!ins.ContainsKey(s)) throw new InvalidDataException("target not instruction");
        if (!depth.ContainsKey(s)) { depth[s] = od; q.Enqueue(s); }
    }
}
return max;
```

### Por que funciona?

- Entrada em offset 0 com depth 0 modela método sem argumentos na stack de avaliação.
- `od = d - pops + pushes` é transfer function clássica de stack.
- Validar `ins.ContainsKey(s)` garante branch para início de instrução.

### Verificação parcial

Método ok deve retornar `2`. Método bad ainda pode passar até MERGE — próximo TODO.

---

## D5-CIL-MERGE — profundidade compatível em joins

### O problema

Sem merge check, caminhos conflitantes do `brtrue` podem sobrescrever depth silenciosamente. Teste `bad` espera `InvalidDataException`.

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/Chris.CilCfg/Verifier.cs` |
| **Função / âncora** | dentro do `foreach (var s in x.Succ)` — `TODO [D5-CIL-MERGE]` |
| **Substituir** | bloco `if (!depth.ContainsKey(s))` |
| **Não mexer** | lógica de decode |

### Código — merge

```csharp
        if (depth.TryGetValue(s, out int old)) {
            if (old != od) throw new InvalidDataException("incompatible stack depth at merge");
        } else {
            depth[s] = od;
            q.Enqueue(s);
        }
```

### Por que funciona?

- Primeira chegada registra profundidade exigida no join.
- Segunda chegada com valor diferente prova caminhos incompatíveis — IL rejeitado.
- Igualdade preservada permite loops no CFG (mesmo depth).

### Verificação final

```powershell
dotnet run --project starter/Chris.CilCfg.Tests
```

**Esperado:** `chris-cil-cfg tests passed`.

---

## Debug

| Sintoma | Causa | Correção |
|---------|-------|----------|
| `target not instruction` | delta branch errado | relativo a IP pós-operando |
| max=0 | decode vazio | loop while ip |
| bad passa | merge sobrescreve | compare old != od |
| underflow no ok | pops errados em add | pops=2 para 0x58 |

Watch: `o`, `d`, `x.Pops`, `x.Pushes`, `od`, `x.Succ`, `depth`.

---

## Relatório de resolução

1. **IP após `ldc.i4` no offset 0:** _____
2. **Profundidade antes de `add` no método ok:** _____
3. **Por que join exige mesma depth?** _____
4. **Opcode do branch condicional neste subset:** _____
5. **Erro observado no método bad:** _____
