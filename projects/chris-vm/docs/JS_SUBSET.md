# JS subset v1 → CLVM (chris-vm)

Educational JavaScript subset that compiles to CLVM assembly (then `.clvm` via `assemble.py` or the direct emitter).

## Goals

- Integers (`i32` semantics on the VM)
- Locals (`let` / `const`)
- Arithmetic and comparisons (`+ - * / %` — `%` desaçucarado)
- `if` / `while`
- Top-level `function` + call / `return`
- Builtin `print(expr)`

## Non-goals (v1)

Strings, objects, arrays, closures, GC, `typeof`, `for`/`switch`, modules, recursion that needs dynamic frames, floats, bitwise ops. (Strings → FORMAT v2 / lab N4.)

## Grammar (informal)

```
program        := item*
item           := functionDecl | stmt
functionDecl   := 'function' Ident '(' [Ident (',' Ident)*] ')' block
block          := '{' stmt* '}'
stmt           := 'let' Ident '=' expr ';'
               | 'const' Ident '=' expr ';'
               | Ident '=' expr ';'
               | 'if' '(' expr ')' block ['else' block]
               | 'while' '(' expr ')' block
               | 'return' expr ';'
               | 'print' '(' expr ')' ';'
               | expr ';'
expr           := cmpExpr
cmpExpr        := addExpr (('==' | '!=' | '<' | '<=' | '>' | '>=') addExpr)*
addExpr        := mulExpr (('+' | '-') mulExpr)*
mulExpr        := unary (('*' | '/' | '%') unary)*
unary          := ('-' | '!') unary | primary
primary        := Number | Ident | Ident '(' [expr (',' expr)*] ')' | '(' expr ')'
```

## Mapping to CLVM

| JS | CLVM |
|----|------|
| number literal | `PUSH` |
| `+ - * /` | `ADD` `SUB` `MUL` `DIV` |
| `== <` (and derived) | `EQ` `LT` (+ helpers) |
| locals | `LOAD` / `STORE` (4-byte slots in 256 B mem) |
| `if` / `while` | labels + `JZ` / `JNZ` / `JMP` |
| `function` / call | `CALL` / `RET`; args on data stack |
| `print(x)` | evaluate `x` then `PRINT` |
| end of main | `HALT` |

## Runtime limits (enforced by compiler and/or VM)

| Limit | Value | Source |
|-------|------:|--------|
| Linear memory | 256 bytes | VM `kMemSize` |
| Local slots (4 B each) | 64 max total | `256 / 4` |
| Call stack depth | 256 | VM `kMaxCall` |
| Data stack | 1024 | VM `kMaxStack` |
| Interpreter steps | 1_000_000 | VM `kMaxSteps` |
| Nested recursion with overlapping frames | unsupported | static slot layout |

Slot layout: each function (and main) gets a contiguous, compile-time base offset. Nested calls to different functions are OK if totals ≤ 64 slots; deep recursion that re-enters the same function is **not** supported in v1.

## Examples

See `examples/js/add.js`, `loop.js`, `fn_add.js`.

## CLI

From `projects/chris-vm`:

```powershell
$env:PYTHONPATH = "tools"
python -m js2clvm examples/js/add.js -o out.asm
python -m js2clvm examples/js/add.js --dump-asm -o out.asm
python -m js2clvm examples/js/add.js --emit-clvm -o out.clvm
python tools/assemble.py out.asm out.clvm
python tools/verify_clvm.py out.clvm
python tools/disasm_clvm.py out.clvm
```

Exceeding `max_slots` (64) fails at compile time with `CodegenError`. Assigning to `const` also fails at compile time. VM still enforces mem OOB, call depth, and step limits at runtime.
