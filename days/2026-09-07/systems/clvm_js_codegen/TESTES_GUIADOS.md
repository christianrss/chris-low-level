# Testes guiados — clvm_js_codegen

## CLVM-JS-LET-01

`add.js` → asm contém `STORE` e `MUL`; verify OK.

## CLVM-JS-WHILE-01

`loop.js` → `JZ`/`JMP`.

## CLVM-JS-CALL-01

`fn_add.js` → `CALL add`.

```powershell
cd solutions
python tests/integration_test.py
```

Esperado: `clvm_js_codegen integration tests passed`.
