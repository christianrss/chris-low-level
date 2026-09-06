# Teoria passo a passo — Lexer, parser, bytecode e VM JavaScript-like

## 1. O problema de produção

Engines reais escondem parse → AST → bytecode → JIT → GC. Este lab encolhe o pipeline a um subset C++ (`let`, `print`, inteiros, `+ - *`) para tornar invariantes de lexer, precedência e stack **operacionais**.

### O quê

Sete TODOs: lex number/ident+keywords; statements `let`/`print`; precedência `expression`/`term`; opcode `Add` na stack VM.

### Como

Lexer consome dígitos/idents; compiler recursive-descent emite `Op` sem AST; VM interpreta pilha (`pop b`, `pop a`, `push a+b`).

### Por quê

Keyword como Ident quebra statements. Precedência invertida gera `(x+y)*2`. `Add` que só empilha `a` imprime 10 em vez de 50 — bug silencioso se o teste não cobrir aritmética.

## 2. Programa-alvo

```js
let x = 10;
let y = 20;
print(x + y * 2);
```

Saída: **50** (`*` antes de `+`).

## 3. Pipeline

```text
source → Lexer → Tokens → Compiler (RD) → Bytecode → Stack VM → stdout
```

## 4. Lexer

| Token | Regra |
|-------|-------|
| Number | dígitos → Int64 acumulado |
| Ident | alnum/`_`; `let`/`print` → keywords |
| Símbolos | `= + - * ( ) ;` |
| EOF | fim |

Whitespace ignorado. `=` é token (`Kind::Equal`).

## 5. Gramática e precedência

```text
statement := letStmt | printStmt
letStmt   := 'let' ident '=' expression ';'
printStmt := 'print' '(' expression ')' ';'
expression:= term (('+'|'-') term)*
term      := factor ('*' factor)*
factor    := number | ident | '(' expression ')'
```

`term` mais profundo → `*` amarra primeiro.

## 6. Bytecode típico de `print(x + y * 2)`

```text
LoadGlobal x
LoadGlobal y
PushConst 2
Mul
Add
Print
```

## 7. Stack (topo à direita)

```text
… Mul → [10, 40]
… Add → [50]
… Print → stdout 50
```

Invariante: binário remove 2, empilha 1.

## 8. Opcodes

| Op | Efeito |
|----|--------|
| PushConst / LoadGlobal / StoreGlobal | push / push / pop→global |
| Add/Sub/Mul | pop b, pop a, push a⊕b |
| Print | pop → output |
| Halt | fim |

## 9. Bugs clássicos

1. Number com valor 0 (não acumular dígitos).
2. `let` como Identifier.
3. Emitir Print antes da expressão.
4. `expression` tratar `*` (precedência invertida).
5. Add empilhar só `a`.

## 10. Globals e índices

`name_index` linear em `program_.names`: primeiro `let x` aloca slot; usos posteriores reutilizam. Sem escopos aninhados neste milestone.

## 11. Vs V8 (qualitativo)

| Lab | Engine real |
|-----|-------------|
| bytecode interpretado | Ignition → TurboFan |
| int64 only | tagged / heap numbers |
| globals flat | lexical envs, closures |
| sem GC | GC geracional |

## 12. Debugging guiado

1. Dump tokens antes do parse.
2. Dump bytecode com índices.
3. Trace VM: após cada op, stack + IP.
4. Compare `1+2*3` vs `(1+2)*3` no papel.

## 13. Benchmark

Release: tempo compile+exec vs linhas. Hipótese: lexer/parser dominam inputs pequenos; VM se bytecode crescer. Sem JIT — resultados estáveis. Registre mediana.

## 14. Segurança

Não é sandbox. Não exponha a rede. Extensões: limite tamanho de source, profundidade de parse, altura da pilha.

## 15. Perguntas

1. Por que `term` chama `factor`?
2. Bytecode de `2+3*4` vs `(2+3)*4`?
3. Stack se Add não remover dois?
4. Keywords no lexer ou no parser?

## Fundamentos adicionais (reforço Dia 01)

### O quê

A VM interpreta bytecode gerado pelo frontend: lexer, parser, codegen e loop de dispatch.

### Como

Trabalhe com um exemplo numérico no papel antes de editar o starter: anote entradas, estado intermediário e saída esperada.

### Por quê

Sem o modelo mental no papel, o código vira tentativa-e-erro e os testes não ensinam o invariante.

### Por quê comparar com produção

Implementações reais (libc, kernels, VMs, GPUs) usam as mesmas ideias com mais camadas; este lab isola o núcleo.

### Por quê falhar de propósito no starter

O starter compila e o teste falha até o TODO existir — isso prova que o harness mede o comportamento certo.

### Trace manual

`	ext
entrada -> transformação -> invariante -> saída
` 

### Bugs comuns (módulo)

| Sintoma | Causa | Depuração |
|---------|-------|-----------|
| Teste falha após 'implementar' | Off-by-one / endian | Trace byte a byte |
| PASS sem entender | Copiou gabarito | Refaça o paper-trace |

