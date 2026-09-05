# Testes guiados — bytecode_vm_from_scratch

Este arquivo é a ponte entre cada TODO real do `starter/` e a evidência que deve ficar verde. Não pule diretamente para `solutions/`.

## Baseline

A partir da pasta deste módulo:

```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

**Antes de implementar:** build passa; starter falha nos TODOs do lexer/compiler/VM.

## Mapa TODO → teste

### `D2-JS-LEX-NUMBER`
- Arquivo: `starter/src/chris_js.cpp`
- Validação: inteiros são tokenizados com valor correto.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-JS-LEX-NUMBER`

### `D2-JS-LEX-IDENT`
- Arquivo: `starter/src/chris_js.cpp`
- Validação: `let`/`print` viram keywords; demais nomes viram Identifier.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-JS-LEX-IDENT`

### `D2-JS-STMT-LET`
- Arquivo: `starter/src/chris_js.cpp`
- Validação: `let x = ...;` emite StoreGlobal.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-JS-STMT-LET`

### `D2-JS-STMT-PRINT`
- Arquivo: `starter/src/chris_js.cpp`
- Validação: `print(...);` emite Print.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-JS-STMT-PRINT`

### `D2-JS-PREC-ADD`
- Arquivo: `starter/src/chris_js.cpp`
- Validação: `+/-` são compilados acima de terms.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-JS-PREC-ADD`

### `D2-JS-PREC-MUL`
- Arquivo: `starter/src/chris_js.cpp`
- Validação: `*` tem precedência maior que `+/-`.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-JS-PREC-MUL`

### `D2-JS-VM-ADD`
- Arquivo: `starter/src/chris_js.cpp`
- Validação: VM faz `a+b` mantendo ordem correta de pops.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-JS-VM-ADD`

## Depois de concluir

Rode novamente o mesmo comando. Resultado esperado:

- `chris-js tests passed` e CLI imprime `50`.
- Não remova/afrouxe asserts para “fazer passar”.
- Compare com `solutions/` somente depois de seu starter ficar verde.
- Acrescente pelo menos um edge case próprio e anote qual regressão ele detectaria.
