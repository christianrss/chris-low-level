# Resolução guiada — clvm_js_codegen

## Mapa exato starter → resolução

| ID | Arquivo | Âncora |
|----|---------|--------|
| `CLVM-JS-LET-01` | `starter/js2clvm/codegen.py` | `_stmt` / `LetStmt` |
| `CLVM-JS-WHILE-01` | idem | `_stmt` / `WhileStmt` |
| `CLVM-JS-CALL-01` | idem | `Call` + prólogo `generate` |

---

## CLVM-JS-LET-01

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/js2clvm/codegen.py` |
| **Função / âncora** | `_stmt` — `TODO [CLVM-JS-LET-01]` |
| **Substituir** | o `raise CodegenError("TODO [CLVM-JS-LET-01]...")` |
| **Não mexer** | `parser.py`, `lexer.py` |

### Escreva o código

```python
self._expr(stmt.expr)
addr = self._current.alloc(stmt.name, const=stmt.const)
self._emit(f"PUSH {addr}")
self._emit("STORE")
```

### Por que funciona

Mesma ordem que `mem_demo.asm` no Dia 04.

### Verifique

Espere asm com `STORE`. Depure com print do asm. Esperado: slots 0 e 4 para dois lets.

---

## CLVM-JS-WHILE-01

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/js2clvm/codegen.py` |
| **Função / âncora** | `WhileStmt` |
| **Substituir** | raise TODO WHILE |
| **Não mexer** | VM |

### Escreva o código

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

### Por que funciona

Mesmo padrão do countdown Dia 01.

### Verifique

Esperado: `JZ`/`JMP` no asm de `loop.js`. Depure labels únicos.

---

## CLVM-JS-CALL-01

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/js2clvm/codegen.py` |
| **Função / âncora** | prólogo + `_expr` Call |
| **Substituir** | raises CALL |
| **Não mexer** | `main.cpp` chris-vm |

### Escreva o código

Prólogo + CALL como em `solutions/js2clvm/codegen.py`.

### Por que funciona

Calling convention = `add2.asm`.

### Verifique

Esperado: `CALL add` em `fn_add.js`. Depure com disasm.

---

## Relatório de resolução

- TODOs concluídos: ___
- Testes starter (FAIL esperado) / solutions (PASS): ___
- Depuração usada: ___
- Dúvidas: ___
