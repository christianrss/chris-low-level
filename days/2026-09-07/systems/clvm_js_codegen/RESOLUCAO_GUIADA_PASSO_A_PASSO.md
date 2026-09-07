# Resolução guiada passo a passo — CLVM JS codegen

Trabalhe em `days/2026-09-07/systems/clvm_js_codegen/starter/`. Implemente os três TODOs em `starter/js2clvm/codegen.py` na ordem LET → WHILE → CALL.

## Mapa exato starter → resolução

| TODO ID | Arquivo starter | Função / âncora | O que substituir |
|---------|-----------------|-----------------|------------------|
| `CLVM-JS-LET-01` | `starter/js2clvm/codegen.py` | `_stmt` → ramo `LetStmt` | `raise CodegenError("TODO [CLVM-JS-LET-01]...")` |
| `CLVM-JS-WHILE-01` | `starter/js2clvm/codegen.py` | `_stmt` → ramo `WhileStmt` | `raise CodegenError("TODO [CLVM-JS-WHILE-01]...")` |
| `CLVM-JS-CALL-01` | `starter/js2clvm/codegen.py` | `generate` (prólogo) + `_expr` → `Call` | dois `raise CodegenError("TODO [CLVM-JS-CALL-01]...")` |

Ordem recomendada: LET-01 desbloqueia `add.js`; WHILE-01 desbloqueia `loop.js`; CALL-01 desbloqueia `fn_add.js`.

## Baseline

Antes de editar qualquer linha, confirme que o starter falha nos três casos por causa dos stubs:

```powershell
cd days/2026-09-07/systems/clvm_js_codegen/starter
python tests/integration_test.py
```

**Esperado:** saída de erro — `CodegenError` com mensagem `TODO [CLVM-JS-LET-01]` ao compilar `add.js`, ou falha equivalente nos outros exemplos. Isso prova que o ambiente Python, imports e caminhos estão corretos; o único bloqueio são os TODOs.

Depois de implementar os três IDs, rode o mesmo comando na pasta `solutions/` — aí o esperado é `clvm_js_codegen integration tests passed`.

## CLVM-JS-LET-01 — let / const → STORE

### Onde colocar (LET-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/js2clvm/codegen.py` |
| Função / âncora | `_stmt` — comentário `TODO [CLVM-JS-LET-01]` no ramo `isinstance(stmt, LetStmt)` |
| Substituir | o `raise CodegenError("TODO [CLVM-JS-LET-01]: implement let/const lowering")` |
| Não mexer | `parser.py`, `lexer.py`, `assemble.py`, ramo `AssignStmt` (já funciona) |

### O problema (LET-01)

`let a = 7` e `let b = 5` em `examples/js/add.js` precisam virar slots de memória com valores gravados. Sem LET-01, o codegen aborta antes de emitir qualquer instrução para declarações.

O `AssignStmt` adjacent no mesmo método já mostra o padrão de reatribuição (`_expr` → `PUSH addr` → `STORE`). Falta o passo de **alocar** o slot na primeira declaração.

### Algoritmo / trace (LET-01)

Para `let a = 7` com frame `__main__` (base=0):

| passo | ação | pilha após |
|-------|------|------------|
| 1 | `_expr(7)` emite `PUSH 7` | `[7]` |
| 2 | `alloc("a")` → slot 0, addr 0 | `[7]` |
| 3 | `PUSH 0` | `[7, 0]` |
| 4 | `STORE` grava mem[0]=7 | `[]` |

Para `let b = 5` em sequência: slot 1 em addr 4, mesma sequência. Leitura `a * b` usa `Name` → `PUSH addr; LOAD` (já implementado).

### Escreva o código COMPLETO (LET-01)

Substitua o corpo do ramo `LetStmt` por:

```python
self._expr(stmt.expr)
addr = self._current.alloc(stmt.name, const=stmt.const)
self._emit(f"PUSH {addr}")
self._emit("STORE")
```

### Por que funciona (LET-01)

A ordem espelha `mem_demo.asm` do Dia 04: valor na pilha, endereço empilhado por último, `STORE` consome endereço e depois valor. `alloc` reserva o índice local e marca `const` quando `stmt.const` é verdadeiro — reatribuições a `const` serão rejeitadas depois pelo ramo `AssignStmt`.

### Verifique (LET-01)

```powershell
cd starter
python -m js2clvm examples/js/add.js
```

**Esperado no asm de add.js:** duas sequências `PUSH <n>` + `PUSH <addr>` + `STORE`; `MUL` e `ADD` para `a * b + 3`; `PRINT` e `HALT`; header `# slots_used=2`.

Rode `python tests/integration_test.py` — o caso `add.js` deve passar; `loop.js` e `fn_add.js` ainda falham (WHILE e CALL pendentes).

### Debug (LET-01)

| Sintoma | Causa provável | Ação |
|---------|----------------|------|
| `undefined variable a` | `alloc` ausente ou depois de `addr` | confira ordem: `_expr` antes de `alloc` |
| asm sem `STORE` | raise TODO ainda presente | substitua o stub inteiro |
| `redeclaration of a` | `alloc` chamado duas vezes para o mesmo nome | `let` duplicado no fonte ou bug no frame |
| valor impresso errado | ordem invertida no `STORE` | valor deve estar abaixo do endereço |
| `too many locals` | `_count_lets` desincronizado | não altere `_count_lets`; só o corpo do `LetStmt` |

## CLVM-JS-WHILE-01 — while → labels + JZ/JMP

### Onde colocar (WHILE-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/js2clvm/codegen.py` |
| Função / âncora | `_stmt` — comentário `TODO [CLVM-JS-WHILE-01]` no ramo `isinstance(stmt, WhileStmt)` |
| Substituir | o `raise CodegenError("TODO [CLVM-JS-WHILE-01]: implement while lowering")` |
| Não mexer | ramo `IfStmt` (use como referência de labels), VM, assembler |

### O problema (WHILE-01)

`examples/js/loop.js` declara `let i = 0` e repete `print(i); i = i + 1` enquanto `i < 4`. Sem WHILE-01, o codegen não emite saltos. A VM não tem construto de laço — só `JZ`/`JMP` que você já usa em `if/else`.

### Algoritmo / trace (WHILE-01)

Estrutura asm alvo para `while (cond) { body }`:

| bloco | instruções emitidas |
|-------|---------------------|
| cabeçalho `_whileN:` | avaliar `cond` |
| saída condicional | `JZ _wendM` (sai se cond == 0) |
| corpo | statements do `while` |
| repetição | `JMP _whileN` |
| fim `_wendM:` | continuação do programa |

Na 4ª iteração de `loop.js` (i=3): `LT` produz 1, `JZ` não salta, `print` emite 3, `i=i+1` grava 4. Na 5ª avaliação (i=4): `LT` produz 0, `JZ` salta para `_wendM`, laço encerra.

### Escreva o código COMPLETO (WHILE-01)

Substitua o corpo do ramo `WhileStmt` por:

```python
head = self._label("while")
end = self._label("wend")
self._emit(f"{head}:")
self._expr(stmt.cond)
self._emit(f"JZ {end}")
for s in stmt.body:
    self._stmt(s)
self._emit(f"JMP {head}")
self._emit(f"{end}:")
```

### Por que funciona (WHILE-01)

`_label("while")` e `_label("wend")` geram nomes únicos (`_while1`, `_wend2`, …) — laços aninhados não colidem. `JZ` consome a condição; quando `i < 4` é falso, a pilha tinha `0` e o salto sai do laço. `JMP` incondicional volta ao cabeçalho sem deixar lixo na pilha.

O padrão é o mesmo do `max_loop.asm` do Dia 04, exceto que a condição vem de expressão arbitrária (`i < 4`) em vez de asm manual.

### Verifique (WHILE-01)

```powershell
python -m js2clvm examples/js/loop.js
```

**Esperado no asm de loop.js:** par de labels `_whileN:` e `_wendM:`; `JZ _wendM` logo após a condição; `JMP _whileN` ao final do corpo; `PRINT` dentro do corpo.

Rode `python tests/integration_test.py` — casos `add.js` e `loop.js` passam; `fn_add.js` ainda falha.

### Debug (WHILE-01)

| Sintoma | Causa provável | Ação |
|---------|----------------|------|
| laço infinito na VM | `JZ` aponta para dentro do corpo | destino do `JZ` deve ser `_wend`, não `_while` |
| laço nunca executa | `JMP` aponta para `_wend` | `JMP` deve voltar a `_while` |
| `stack underflow` em `JZ` | condição não emitida | chame `self._expr(stmt.cond)` antes do `JZ` |
| labels duplicados | `_label` não usado | nunca hardcode `_while1` — use `self._label()` |
| stdout vazio | corpo do while não emitido | confira o `for s in stmt.body` |

## CLVM-JS-CALL-01 — CALL + prólogo de parâmetros

### Onde colocar (CALL-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/js2clvm/codegen.py` |
| Prólogo (A) | `generate` — comentário `TODO [CLVM-JS-CALL-01]: prologue` no loop de funções |
| Call lowering (B) | `_expr` — comentário `TODO [CLVM-JS-CALL-01]` no ramo `isinstance(expr, Call)` |
| Substituir | o `for name in reversed(fn.params): raise ...` do prólogo **e** o `raise` do ramo `Call` |
| Não mexer | `main.cpp` da VM, `assemble.py`, cálculo de frames em `generate()` |

### O problema (CALL-01)

`examples/js/fn_add.js` declara `function add(a, b) { return a + b; }` e chama `print(add(3, 5))`. Duas peças faltam:

1. **Caller:** empilhar `3`, depois `5`, emitir `CALL add`.
2. **Callee:** ao entrar em `add:`, consumir `5` e `3` da pilha e gravar em slots locais com `STORE` (último param no topo).

Sem o prólogo, `LOAD a` e `LOAD b` dentro da função leem memória não inicializada. Sem o lowering de `Call`, nenhum `CALL add` aparece no asm.

### Algoritmo / trace (CALL-01)

**Caller** — `add(3, 5)`:

| passo | pilha (topo→) | instrução |
|-------|---------------|-----------|
| avaliar 3 | 3 | `PUSH 3` |
| avaliar 5 | 5, 3 | `PUSH 5` |
| chamar | (call stack + PC) | `CALL add` |

**Callee** — `reversed(["a","b"])` = `["b","a"]`:

| passo | pilha | ação |
|-------|-------|------|
| STORE b | 3 | `alloc(b); PUSH addr_b; STORE` → mem[addr_b]=5 |
| STORE a | | `alloc(a); PUSH addr_a; STORE` → mem[addr_a]=3 |
| return a+b | | `LOAD a; LOAD b; ADD; RET` → caller recebe 8 |

### Escreva o código COMPLETO (CALL-01)

**Parte A — prólogo em `generate()`** (substitua o `for` com `raise`):

```python
for name in reversed(fn.params):
    addr = self._current.alloc(name)
    self._emit(f"PUSH {addr}")
    self._emit("STORE")
```

**Parte B — lowering de `Call` em `_expr()`** (substitua o `raise`):

```python
if expr.callee not in self.fn_names:
    raise CodegenError(f"unknown function {expr.callee}")
fn = next(f for f in self.program.functions if f.name == expr.callee)
if len(expr.args) != len(fn.params):
    raise CodegenError(
        f"{expr.callee} expects {len(fn.params)} args, got {len(expr.args)}"
    )
for a in expr.args:
    self._expr(a)
self._emit(f"CALL {expr.callee}")
```

### Por que funciona (CALL-01)

A convenção de chamada é idêntica a `add2.asm` do Dia 04: caller empilha argumentos em ordem textual (último no topo); callee consome com `STORE` em ordem reversa dos nomes de parâmetro. `CALL` empurra o return-PC e salta; `RET` no `return a + b` devolve o resultado ao caller.

`alloc` no prólogo reserva slots 0..n-1 para parâmetros — os mesmos índices que `_count_lets` já contabilizou em `len(fn.params) + _count_lets(fn.body)`. Arity check em compile-time evita descompasso entre argumentos empilhados e `STORE` do prólogo.

### Verifique (CALL-01)

```powershell
python -m js2clvm examples/js/fn_add.js
```

**Esperado no asm de fn_add.js:** `PUSH 3; PUSH 5; CALL add; PRINT; HALT`; label `add:` com dois pares `PUSH <addr>; STORE` no prólogo; corpo com `ADD; RET`.

Teste completo:

```powershell
python tests/integration_test.py
```

**Esperado:** `clvm_js_codegen integration tests passed` (três casos: STORE/MUL, JZ/JMP, CALL add).

### Debug (CALL-01)

| Sintoma | Causa provável | Ação |
|---------|----------------|------|
| `CALL add` ausente | Parte B não implementada | implemente ramo `Call` em `_expr` |
| resultado 0 ou lixo | prólogo ausente ou sem `reversed` | Parte A: `for name in reversed(fn.params)` |
| `add expects 2 args, got 1` | arity check funcionando | corrija chamada no JS, não remova o check |
| `unknown function foo` | nome não está em `program.functions` | typo no JS ou função não declarada |
| `return stack underflow` | `RET` sem `CALL` correspondente | trace com `--trace` na VM |
| args trocados (ex.: 3 em vez de 8) | `reversed` omitido | primeiro STORE deve consumir último param |
| `undefined variable a` dentro de fn | `alloc` no prólogo antes do corpo | não use `addr` para params — use `alloc` |

## Relatório de resolução

Preencha após concluir os três TODOs:

| Campo | Valor |
|-------|-------|
| TODOs concluídos | CLVM-JS-LET-01 ☐ / WHILE-01 ☐ / CALL-01 ☐ |
| Baseline starter (FAIL esperado) | comando rodado: ________________ / erro visto: ________________ |
| Teste final starter (PASS) | `python tests/integration_test.py` → ________________ |
| Evidência `add.js` | stdout VM: 38 ☐ / asm contém `STORE`+`MUL` ☐ |
| Evidência `loop.js` | stdout VM: 0 1 2 3 ☐ / asm contém `JZ`+`JMP` ☐ |
| Evidência `fn_add.js` | stdout VM: 8 ☐ / asm contém `CALL add` ☐ |
| Depuração usada | dump asm / verify_clvm / trace VM: ________________ |
| Dúvidas abertas | ________________ |

Critério de aceite final: mensagem `clvm_js_codegen integration tests passed` com os três exemplos montando `.clvm` válido (verify sem erros).

## Debug — referência rápida entre os três TODOs

| TODO | Comando de inspeção | asm deve conter | stdout VM |
|------|---------------------|-----------------|-----------|
| LET-01 | `python -m js2clvm examples/js/add.js` | `STORE`, `MUL`, `ADD` | 38 |
| WHILE-01 | `python -m js2clvm examples/js/loop.js` | `_while`, `_wend`, `JZ`, `JMP` | 0 1 2 3 (linhas separadas) |
| CALL-01 | `python -m js2clvm examples/js/fn_add.js` | `CALL add`, `STORE`×2 no label `add:` | 8 |

Se um caso falha no `integration_test.py` mas o asm parece correto:

1. Salve o asm em arquivo temporário e rode `python assemble.py <asm> out.clvm`.
2. Passe `out.clvm` por `python verify_clvm.py out.clvm` — erros de montagem aparecem antes da VM.
3. Execute na VM do Dia 04 com `--trace` para ver pilha de dados e call stack no `CALL`/`RET`.

Ordem de implementação importa: não tente CALL-01 antes de LET-01 — `let` dentro de funções também depende de `STORE`.
