# Resolução guiada — chris-vm / js2clvm

Leitura **código a código** do pipeline JS → CLVM. Não há stubs vazios aqui: o objetivo é entender *onde* cada ideia mora e *o que* alterar se você estender o subset.

Pré-requisito: Dia 01 + Dia 04 feitos (ou solutions lidas).

---

## Mapa exato: pasta → papel

| Caminho | Papel |
|---------|--------|
| `examples/js/*.js` | programas golden |
| `tools/js2clvm/lexer.py` | tokens |
| `tools/js2clvm/parser.py` + `ast_nodes.py` | AST |
| `tools/js2clvm/codegen.py` | AST → texto `.asm` |
| `tools/js2clvm/cli.py` | CLI / `--emit-clvm` |
| `tools/assemble.py` | `.asm` → `.clvm` |
| `tools/disasm_clvm.py` / `verify_clvm.py` | inspeção |
| `src/main.cpp` | execução |

---

## Passo 0 — rode um golden antes de ler código

### Onde colocar

| | |
|--|--|
| **Arquivo** | terminal em `projects/chris-vm` |
| **Função / âncora** | CLI `js2clvm` |
| **Inserir** | nada — só executar |
| **Não mexer** | ISA / `main.cpp` neste passo |

### Comandos

```powershell
$env:PYTHONPATH = "tools"
python -m js2clvm examples/js/add.js --dump-asm -o out.asm
python -m js2clvm examples/js/add.js --emit-clvm -o out.clvm
# depois: build/Release/clvm.exe out.clvm  → deve imprimir 38
```

### Por que funciona

`add.js` usa só `let` + aritmética + `print`. O codegen emite `STORE`/`LOAD` nos slots 0 e 4 e termina com `HALT` — o mesmo vocabulário do Dia 01.

### Verifique

Stdout `38`. `python tools/disasm_clvm.py out.clvm` mostra `PUSH`/`STORE`/`LOAD`/`MUL`/`ADD`/`PRINT`/`HALT`.

---

## Passo 1 — do `.js` ao asm de `let`

### Onde colocar

| | |
|--|--|
| **Arquivo** | `examples/js/add.js` (ler) → saída em `codegen.py` |
| **Função / âncora** | `Codegen._stmt` ramo `LetStmt` |
| **Substituir** | nada na 1ª leitura; se mudar o layout de slots, é aqui |
| **Não mexer** | `assemble.py` |

### Código (ideia do lowering)

Fonte:

```javascript
let a = 7;
let b = 5;
print(a * b + 3);
```

Asm gerado (resumo):

```asm
PUSH 7
PUSH 0
STORE
PUSH 5
PUSH 4
STORE
PUSH 0
LOAD
PUSH 4
LOAD
MUL
PUSH 3
ADD
PRINT
HALT
```

Trecho correspondente em codegen:

```python
# LetStmt: avalia expr, depois STORE no endereço do slot
self._expr(stmt.expr)
addr = self._current.alloc(stmt.name, const=stmt.const)
self._emit(f"PUSH {addr}")
self._emit("STORE")
```

### Por que funciona

`STORE` espera `value addr --` (addr no topo) — igual ao `mem_demo.asm` do Dia 04. Endereços são bytes: slot `i` → `base + i*4`.

### Verifique

`--dump-asm` e confira que `a` → `0`, `b` → `4` quando o main começa na base 0.

---

## Passo 2 — lexer e parser

### Onde colocar

| | |
|--|--|
| **Arquivo** | `tools/js2clvm/lexer.py`, `parser.py`, `ast_nodes.py` |
| **Função / âncora** | `Lexer.next`, `Parser.parse` / `_stmt` |
| **Inserir** | novo keyword → `KEYWORDS` no lexer + ramo no parser + nó em `ast_nodes` |
| **Não mexer** | `codegen.py` até o AST existir |

### O que ler

1. `KEYWORDS` — `let`, `function`, `while`, `print`, …
2. `Parser._function` — `function nome(params) { … }`
3. `ast_nodes.Program` — `functions` + `main`

### Por que funciona

Separar lexer/parser/codegen deixa o lowering testável: o mesmo AST pode um dia emitir outra ISA (retarget), sem reescrever o parser.

### Verifique

Erro de sintaxe proposital (`let = 1;`) deve falhar no parser com mensagem de linha/coluna, antes do codegen.

---

## Passo 3 — `while` e comparações

### Onde colocar

| | |
|--|--|
| **Arquivo** | `tools/js2clvm/codegen.py` |
| **Função / âncora** | `_stmt` → `WhileStmt`; `_binop` → `"<"` / `"=="` |
| **Substituir** | lógica de labels se mudar convenção de nomes |
| **Não mexer** | VM (`JZ` já existe desde Dia 01) |

### Código (padrão)

```python
head = self._label("while")
end = self._label("wend")
self._emit(f"{head}:")
self._expr(stmt.cond)
self._emit(f"JZ {end}")
# body…
self._emit(f"JMP {head}")
self._emit(f"{end}:")
```

`i < 4` vira `LOAD` / `PUSH 4` / `LT`.

### Por que funciona

Condicao na pilha + `JZ` = mesmo modelo do `countdown.asm`. Labels únicos (`_while1`) evitam colisão entre loops.

### Verifique

`examples/js/loop.js` → stdout `0\n1\n2\n3`.

---

## Passo 4 — `function` / `CALL` / `RET`

### Onde colocar

| | |
|--|--|
| **Arquivo** | `codegen.py` (`generate` prólogo da função + `Call` em `_expr`) |
| **Função / âncora** | loop `for name in reversed(fn.params)`; `CALL {name}` |
| **Não mexer** | semântica de `CALL` em `src/main.cpp` (Dia 04) |

### Código (prólogo)

Args já estão na pilha (último no topo). O codegen faz, para cada param da direita para a esquerda:

```python
addr = self._current.alloc(name)
self._emit(f"PUSH {addr}")
self._emit("STORE")
```

Chamada:

```python
for a in expr.args:
    self._expr(a)
self._emit(f"CALL {expr.callee}")
```

### Por que funciona

Igual ao `add2.asm` do Dia 04: `CALL` empurra return-PC; `RET` restaura. Locais da função ficam numa **base de slots distinta** da do main (alocação estática no início de `generate`).

### Verifique

`examples/js/fn_add.js` → `8`. Use `disasm_clvm.py` e ache o `CALL` relativo.

---

## Passo 5 — assembler, verify, disasm

### Onde colocar

| | |
|--|--|
| **Arquivo** | `tools/assemble.py`, `verify_clvm.py`, `disasm_clvm.py`, `js2clvm/cli.py` |
| **Função / âncora** | `assemble()`; `cli._write_clvm`; `verify()` |
| **Inserir** | novo opcode → `OPS`/`BRANCH` no assemble **e** tabelas do disasm/verify |
| **Não mexer** | header magic `CLVM` / FNV (contrato Dia 01) |

### Fluxo `--emit-clvm`

```python
code = assemble.assemble(asm_text)
checksum = assemble.fnv1a32(code)
header = b"CLVM" + bytes([1, 0]) + struct.pack("<HII", 0, len(code), checksum)
out.write_bytes(header + code)
```

### Por que funciona

Um único emitter de bytes (`assemble.py`) evita divergência entre “asm no disco” e “emit direto”.

### Verifique

```powershell
python tools/verify_clvm.py out.clvm   # VALID
python tools/disasm_clvm.py out.clvm
```

---

## Passo 6 — integração automatizada

### Onde colocar

| | |
|--|--|
| **Arquivo** | `tests/integration_test.py` |
| **Função / âncora** | `js_run` + asserts dos três goldens |
| **Inserir** | novo `.js` golden → bloco `js_run` + stdout esperado |
| **Não mexer** | testes asm (`arithmetic`, `add2`, …) |

### Verifique

```powershell
ctest --test-dir build_ci -C Release --output-on-failure
```

---

## Checklist final (objetivo da trilha)

- [ ] Explico header FNV sem olhar (Dia 01)
- [ ] Explico CALL/STORE ordem (Dia 04)
- [ ] Gero asm de `add.js` e reconheço cada opcode
- [ ] Sei onde adicionar um operador novo (lexer → parser → `_binop`)
- [ ] `fn_add.js` roda e o disasm mostra `CALL`/`RET`
- [ ] Distingo chris-vm (CLVM) de chris-js (ISA própria)

Quando todos os itens passam, a trilha Dia 01 → JS→CLVM está fechada no nível educacional v1.
