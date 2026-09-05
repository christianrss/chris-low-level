# Exercícios — Lexer, parser e VM JavaScript-like

## Fácil

- Tokenize manualmente `let x = 10;` e `print(42);` antes de codificar.
- **D2-JS-LEX-NUMBER:** consuma dígitos consecutivos e acumule valor Int64.

## Médio

- **D2-JS-LEX-IDENT:** mapeie `let` e `print` como keywords; demais identificadores ficam como `Identifier`.
- **D2-JS-STMT-LET:** compile `let id = expr;` emitindo `StoreGlobal`.
- **D2-JS-STMT-PRINT:** compile `print(expr);` emitindo `Print`.

## Difícil

- **D2-JS-PREC-MUL:** parse `factor ('*' factor)*` emitindo `Mul`.
- **D2-JS-PREC-ADD:** parse `term (('+'|'-') term)*` emitindo `Add`/`Sub`.
- **D2-JS-VM-ADD:** pop dois operandos, empilhe soma — trace pilha para `1+2*3`.

## Desafio

- Dump bytecode gerado para `print(x + y * 2)` e compare ordem com teoria.
- Adicione opcode `Sub` e teste `print(10 - 3 * 2)` esperando `4`.
