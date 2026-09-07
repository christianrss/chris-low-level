# Teoria — verifier CLVM (N2)

## 1. Por que este lab

Checksum (Dia 01) responde: *os bytes mudaram?* O verifier responde: *os bytes formam um programa bem formado?*

Dois tipos de confiança complementares:

| Camada | Pergunta | Falha típica |
|--------|----------|--------------|
| FNV-1a | Integridade do payload | arquivo corrompido, editado à mão |
| Verifier | Forma estrutural + pilha | opcode inválido, salto OOB, underflow |

Imagens `.clvm` geradas pelo N1 (js2clvm) devem passar aqui — fecha o ciclo **compile → validate**.

## 2. Pipeline do verifier

```text
.clvm (bytes)
   │
   ├─► header checks (magic, version, flags, entry, code_size, checksum)
   │
   ├─► linear decode (opcodes, operandos, boundaries)
   │
   ├─► branch bounds (alvo ∈ [0, len(code)])
   │
   └─► stack walk conservador (STACK_EFFECT) → VALID / INVALID
```

O verifier **não executa** PRINT, LOAD real ou efeitos de I/O. Simula apenas profundidade de pilha ao longo de um caminho.

## 3. Header v1 (recapitulação)

```text
offset | tam | campo
-------|-----|------
0x00   | 4   | magic "CLVM"
0x04   | 1   | version (= 1 neste lab)
0x05   | 1   | flags (= 0)
0x06   | 2   | entry (u16 LE, offset no bytecode)
0x08   | 4   | code_size (u32 LE)
0x0C   | 4   | checksum FNV-1a do bytecode
0x10   | N   | code[0..code_size-1]
```

`entry >= code_size` (com code_size > 0) → erro antes do walk.

## 4. Tabela STACK_EFFECT

Cada opcode mapeia para `(pops, pushes)` — quantos slots a pilha perde e ganha **ignorando** caminhos duplos de branches.

| Op | Nome | pops | pushes | Operandos |
|----|------|------|--------|-----------|
| 0x01 | PUSH | 0 | 1 | i32 LE (4 B) |
| 0x02 | ADD | 2 | 1 | — |
| 0x03 | SUB | 2 | 1 | — |
| 0x04 | MUL | 2 | 1 | — |
| 0x05 | DIV | 2 | 1 | — |
| 0x06 | DUP | 1 | 2 | — |
| 0x07 | PRINT | 1 | 0 | — |
| 0x08 | HALT | 0 | 0 | — |
| 0x09 | JMP | 0 | 0 | i16 rel (2 B) |
| 0x0A | JZ | 1 | 0 | i16 rel |
| 0x0B | CALL | 0 | 0 | i16 rel |
| 0x0C | RET | 0 | 0 | — |
| 0x0D | LOAD | 1 | 1 | — |
| 0x0E | STORE | 2 | 0 | — |
| 0x0F | POP | 1 | 0 | — |
| 0x10 | SWAP | 2 | 2 | — |
| 0x11 | NEG | 2 | 1 | — |
| 0x12 | NOT | 2 | 1 | — |
| 0x13 | JNZ | 1 | 0 | i16 rel |

Sincronize esta tabela com `FORMAT.md` / `verify_clvm.py`. Opcode desconhecido → `unknown opcode 0xXX at pc`.

## 5. Por que walk conservador?

Um CFG completo com merge de caminhos exige análise de fluxo mais pesada. O lab usa heurística educacional:

### Por quê não simular todos os caminhos de JZ?

Merge de caminhos taken/not-taken exige fixpoint em profundidade de pilha — custo de implementação desproporcional para N2. O fall-through conservador já pega underflow no codegen típico do js2clvm.

- **JMP / CALL**: segue o alvo do salto (não simula retorno de CALL).
- **JZ / JNZ**: segue apenas o fall-through (PC após operando).
- **HALT / RET**: encerra o caminho atual.
- Loop detectado (`pc in seen`) → para sem erro extra.

Underflow no caminho seguido já pega bugs graves do codegen (ex.: ADD sem dois operandos empilhados).

## 6. Codificação de branches

Conjunto `BRANCH = {0x09, 0x0A, 0x0B, 0x13}`.

```text
PC no opcode:     start
PC após opcode:   start + 1
rel lido em:      start + 1 .. start + 2  (i16 signed LE)
PC após operando: next_pc = start + 3
alvo absoluto:    target = next_pc + rel
```

Diagrama:

```text
  code[0] code[1] code[2] ...
           ^start   ^rel_lo ^rel_hi
                    |---- i16 ----|
                              next_pc = start+3
                              target = next_pc + rel
```

Validação: `0 <= target <= len(code)`. Note o `<= len(code)` — alvo no fim (após último byte) é permitido (PC de parada).

## 7. Passagem 1 — decode linear + boundaries

Varre `[0, len(code))` byte a byte:

1. Lê opcode em `pc`.
2. Se PUSH: exige 4 bytes seguintes; senão `truncated PUSH`.
3. Se BRANCH: exige 2 bytes; calcula `target`; valida bounds; adiciona `target` a `boundaries`.
4. Avança `pc` e registra cada fronteira de instrução em `boundaries`.

Esta passagem não simula pilha — só prova que cada instrução tem operandos completos e saltos apontam para dentro do buffer.

## 8. Passagem 2 — stack walk a partir de entry

Estado inicial: `depth = 0`, `pc = entry`, `seen = {}`, `steps = 0`.

Loop (até `steps >= 100000` ou fim):

```text
1. Se pc >= len(code) ou pc in seen → break
2. seen.add(pc); steps += 1
3. op = code[pc]; (pops, pushes) = STACK_EFFECT[op]
4. Se depth < pops → stack underflow at pc=... → break
5. depth = depth - pops + pushes
6. Se depth > 1024 → stack overflow → break
7. Avança pc conforme opcode (ver seção 9)
```

## 9. Regras de avanço no stack walk

| Opcode | Avanço de PC |
|--------|--------------|
| PUSH | +1 opcode, +4 operando → total +5 |
| BRANCH (geral) | +1 opcode, +2 operando |
| JMP (0x09) | `pc = target` (continue) |
| CALL (0x0B) | `pc = target` (continue) |
| JZ (0x0A), JNZ (0x13) | `pc = next_pc` (fall-through, continue) |
| HALT (0x08) | break |
| RET (0x0C) | break |
| demais | +1 |

## 10. Trace exemplo — PUSH + ADD + HALT

Bytecode hipotético a partir de entry=0:

```text
pc=0  op=0x01 PUSH   depth 0→1   (consome 4 B de operando)
pc=5  op=0x01 PUSH   depth 1→2
pc=10 op=0x02 ADD    pops=2 pushes=1 → depth 2→1
pc=11 op=0x08 HALT   depth 1→1, fim
```

Sem underflow: cada ADD viu pelo menos dois valores na pilha no caminho linear.

## 11. Trace exemplo — underflow

```text
pc=0  op=0x02 ADD    depth=0, pops=2 → ERRO stack underflow at pc=0
```

Codegen esqueceu PUSH — verifier pega antes de rodar na VM.

## 12. Trace exemplo — branch OOB

```text
pc=0  op=0x09 JMP rel=-999
      next_pc=3, target=-996 → ERRO branch target OOB from 0 -> -996
```

## 13. Trace exemplo — JMP seguido no walk

```text
entry=0:
  pc=0 JMP +5  → target=8
  pc=8 PUSH ... (continua no alvo, não executa bytes intermediários)
```

Bytes entre origem e alvo ainda foram validados na passagem 1 se alcançáveis por decode linear.

## 14. Limites documentados

| Limite | Valor | Motivo |
|--------|-------|--------|
| max depth | 1024 | evita loop artificial de DUP |
| max steps | 100000 | evita hang em ciclo de JMP |
| CFG merge | não | conservador por design |
| execução real | não | só forma + pilha |

## 15. Ligação Dia 01

`clvm_parse` / loader C = header + checksum. Verifier = **code shape** + pilha. Mesmo FNV; camadas diferentes.

## 16. Ligação js2clvm (N1)

Falha no verifier após assemble → bug no lowering ou no `assemble.py`, não no loader.

## 17. Fixtures e testes

```powershell
cd solutions   # ou starter após completar TODOs
python tests/integration_test.py
```

- `ok.clvm` → `VALID`
- `bad_checksum.clvm` → `checksum mismatch` (header pass, FNV fail)

Starter levanta `NotImplementedError` nos TODOs → `INVALID` até implementar.

## 18. Mensagens estáveis

Formato: `INVALID: <mensagem>` no stderr. Exemplos fixos para CI:

- `branch target OOB from {start} -> {target}`
- `stack underflow at pc={pc} op=0x{op:02x} depth={depth}`
- `truncated PUSH at {start}`
- `unknown opcode 0x{op:02x} at {pc}`

## 19. Diagrama — duas passagens

```text
        ┌─────────────────┐
        │  code bytes     │
        └────────┬────────┘
                 │
     ┌───────────▼───────────┐
     │ Passagem 1: linear    │
     │ - opcodes conhecidos  │
     │ - operandos completos │
     │ - branch OOB          │
     └───────────┬───────────┘
                 │
     ┌───────────▼───────────┐
     │ Passagem 2: stack     │
     │ - from entry          │
     │ - STACK_EFFECT        │
     │ - underflow/overflow  │
     └───────────┬───────────┘
                 │
            VALID / INVALID
```

## 20. Checklist mental

1. Header e checksum conferem antes do walk?
2. `target` usa `next_pc + rel`, não `start + rel`?
3. PUSH consome 4 bytes extras na contagem de PC?
4. JZ consome 1 slot da pilha no efeito `(1, 0)`?
5. CALL não empilha retorno neste verifier?

## 21. Erros comuns de implementação

- Esquecer `boundaries.add(target)` quando alvo válido.
- Usar `target < len(code)` estrito e rejeitar alvo no EOF.
- No stack walk, tratar JMP como fall-through (deve pular).
- Não incrementar `pc` após operando de PUSH na passagem 2.
- Confundir passagem 1 (decode completo) com passagem 2 (entry only).

## 22. Comparação com validador Rust

`rust-validator` no chris-vm repete FNV/header e pode estender regras. Este lab Python é a referência didática mínima.

## 23. Portfólio

Documente no relatório: quais caminhos o walk **não** une (JZ taken vs not-taken). Isso explica falsos negativos raros e falsos positivos conservadores.

## 24. Próximo lab

N3: operador `%%` no chris-vm. N4: CLVM v2 com string pool — **não quebre v1**.

## 25. Síntese

Verifier = integridade (FNV) + sintaxe (opcodes/operandos) + pilha conservadora. Você aprende a separar *bytes corretos* de *programa executável*.
