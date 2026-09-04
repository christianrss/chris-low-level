# Teoria passo a passo

Este laboratório não usa Node/V8 para executar a linguagem. Ele cria uma linguagem **JavaScript-like** mínima para enxergar o caminho escondido por um runtime real.

Programa de entrada:
```js
let x = 10;
let y = 20;
print(x + y * 2);
```

Pipeline:
```text
characters → lexer/tokens → recursive-descent parser → bytecode → operand stack VM → output
```

Precedência é resolvida separando `expression` (`+/-`), `term` (`*`) e `factor` (número, identificador, parênteses). O compilador emite bytecode diretamente; um AST explícito virá no próximo milestone.

A VM é stack-based: `PushConst 10`, `LoadGlobal y`, `PushConst 2`, `Mul`, `Add`, `Print`.
