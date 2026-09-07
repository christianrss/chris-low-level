# Teoria passo a passo — CIL CFG stack verifier (D5-CIL)

## 1. O que estamos construindo

Um verificador estático **subset CIL** em C#: decodifica opcodes, constrói sucessores (CFG implícito), propaga **profundidade de stack** por worklist e rejeita merges incompatíveis. Retorna profundidade máxima observada. Sem Reflection.Emit completo — só cinco opcodes.

TODOs: `D5-CIL-DECODE`, `D5-CIL-WORKLIST`, `D5-CIL-MERGE`.

## 2. Por quê CFG + stack antes do CLR real

O runtime .NET exige IL **verificável**: stack depth e tipos consistentes em **todo** offset alcançável. Verificação linear (uma passagem) falha com branches — dois caminhos podem exigir profundidades diferentes no mesmo join. Worklist + merge é o núcleo de **dataflow analysis** que o PE verifier aplica antes de JIT.

## 3. Subset de opcodes

| Opcode | Hex | Pops | Push | Successors |
|--------|-----|------|------|------------|
| `ldc.i4` | 0x20 | 0 | 1 | fallthrough |
| `add` | 0x58 | 2 | 1 | fallthrough |
| `br.s` | 0x2B | 0 | 0 | target only |
| `brtrue.s` | 0x2D | 1 | 0 | target + fallthrough |
| `ret` | 0x2A | 1 | 0 | none (exit) |

`ldc.i4` consome **4 bytes** de immediate após o opcode (int32 little-endian).

## 4. Decode e CFG (`D5-CIL-DECODE`)

### O quê
Varredura linear: para cada offset `o` de início de instrução, registrar `(offset, size, pops, pushes, successors[])`.

### Como
```text
ip ← 0
enquanto ip < len(code):
  o ← ip; op ← code[ip++]
  decodificar operandos, pops/pushes, lista succ
  ins[o] ← registro
  (ip avança dentro do decode)
```

**Branch short** (`br.s`, `brtrue.s`): operando é **sbyte** relativo ao IP **após** o byte de deslocamento:
```text
delta ← (sbyte)code[ip]; ip++
target ← ip + delta
```

### Por quê
Offsets de instrução são chaves do dicionário — cair no meio de `ldc.i4` deve ser `target not instruction`. Relativo ao pós-operando segue ECMA-335; delta errado desloca todo o CFG.

### Trace manual — `ldc.i4 1; ldc.i4 2; add; ret`

```text
0: 20 01 00 00 00  → size 6, push 1, succ=[6]
6: 20 02 00 00 00  → size 6, push 1, succ=[12]
12: 58             → pops 2, push 1, succ=[13]
13: 2A             → pops 1, succ=[]
max depth: após segunda ldc depth=2; após add depth=1; ret ok
```

### Invariantes
- Todo byte coberto pertence a exatamente uma instrução ou é operand — não há “buracos” no método válido.
- `ret` tem successors vazio.
- IP nunca ultrapassa `code.Length` sem exceção.

### Bugs comuns
- Target relativo ao opcode em vez de ao pós-operando.
- Esquecer +4 bytes em `ldc.i4`.
- Registrar successor `code.Length` como válido (fallthrough past end).

## 5. Worklist de profundidade (`D5-CIL-WORKLIST`)

### O quê
A partir de offset 0 com depth 0, processar fila de offsets; calcular profundidade de saída e propagar.

### Como
```text
depth[0] ← 0; queue ← {0}
enquanto queue não vazia:
  o ← dequeue; x ← ins[o]; d ← depth[o]
  se d < x.Pops → underflow
  od ← d - x.Pops + x.Pushes
  para cada s em x.Succ: enfileirar s com depth od (merge no próximo TODO)
max ← max(max, od)
```

### Por quê
BFS/worklist explora todos os caminhos alcançáveis — necessário quando `brtrue` bifurca. Profundidade só de entrada 0 falha em joins posteriores.

### Trace manual — `brtrue.s` com stack 1

```text
depth no branch: 1 → pops 1 → od=0 para target e fallthrough
ambos successors devem receber depth 0 no merge
```

### Invariantes
- Só offsets presentes em `ins` entram na fila.
- Underflow é erro imediato — stack negativa é IL inválido.

### Bugs comuns
- Inicializar fila vazia ou depth vazio.
- Propagar `d` em vez de `od`.
- Não validar `ins.ContainsKey(s)` antes de merge.

## 6. Merge em join points (`D5-CIL-MERGE`)

### O quê
Se successor `s` já tem profundidade registrada, novo valor deve ser **igual**; senão `incompatible stack depth at merge`.

### Como
```text
se depth.TryGetValue(s, out old):
  se old != od: throw incompatible
senão:
  depth[s] ← od; enqueue(s)
```

Também rejeitar target que não é início de instrução.

### Por quê
No join, a próxima instrução espera stack com forma única. Profundidades diferentes implicam tipos/contagens distintas — IL não verificável. CLR real também rejeita; aqui só contamos slots.

### Trace manual — teste `bad` do lab

```text
ldc.i4 1; brtrue.s +5; ldc.i4 2; ret
branch to target depth 0 vs fallthrough path depth 1 → merge fail
```

### Invariantes
- Primeira visita define depth; segunda confirma igualdade.
- `max` reflete pico de stack ao longo de **todos** caminhos.

### Bugs comuns
- Sobrescrever `depth[s]` silenciosamente no merge.
- Aceitar target no meio de immediate.

## 7. Fluxo mental

```text
byte[] IL ──► DECODE ──► map offset → Ins
                    │
                    ▼
              WORKLIST depth@0
                    │
                    ▼
              MERGE em joins
                    │
                    ▼
              return max depth
```

## 8. Complexidade

| Fase | Tempo | Espaço |
|------|-------|--------|
| Decode | O(n) bytes | O(#instr) |
| Worklist | O(V+E) caminhos | O(#offsets) depth map |

## 9. Comparação com produção

| Este lab | PEVerifier / RyuJIT |
|----------|---------------------|
| `int depth` | tipo por slot na stack |
| 5 opcodes | ECMA completa + EH |
| throw InvalidDataException | relatório de verificação |

Transferível: **decode → propagate → merge**, não tabela de opcodes inteira.

## 10. Passo a passo guiado

1. `D5-CIL-DECODE` — dicionário `ins` com successors corretos.
2. `D5-CIL-WORKLIST` — fila e underflow.
3. `D5-CIL-MERGE` — compatibilidade em joins.
4. `dotnet run --project starter/Chris.CilCfg.Tests` → `chris-cil-cfg tests passed`.

## 11. Como saber se está correto

- Método ok: `ldc.i4 1; ldc.i4 2; add; ret` → max depth **2**.
- Método bad com merge conflitante → `InvalidDataException`.
- Target inválido → `target not instruction`.

## 12. Invariantes globais

- Assinatura `Verify(byte[] code) → int` inalterada.
- Opcodes fora do subset → `InvalidDataException`.

## 13. Por quê este módulo existe

Introduzir **análise de fluxo** verificável em IL real antes de decompilers e obfuscadores. Cada TODO isola falha que vira IL aparentemente válido mas injetável ou rejeitado pelo runtime por motivo opaco.
