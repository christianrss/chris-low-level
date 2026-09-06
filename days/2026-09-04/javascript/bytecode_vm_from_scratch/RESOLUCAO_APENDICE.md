# Bytecode VM — apêndice da resolução guiada

> Continuação de `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`. Use depois de implementar os sete TODOs, ou quando o valor impresso / bytecode não bater.

## 1. Dump completo do programa demo

Fonte:

```js
let x = 10;
let y = 20;
print(x + y * 2);
```

Bytecode esperado (nomes/índices ilustrativos; ordem dos ops é o contrato):

```text
; let x = 10
PushConst 0      # constants[0] = 10
StoreGlobal 0    # names[0] = "x"

; let y = 20
PushConst 1      # 20
StoreGlobal 1    # "y"

; print(x + y * 2)
LoadGlobal 0     # x → stack [10]
LoadGlobal 1     # y → [10, 20]
PushConst 2      # 2  → [10, 20, 2]
Mul              #     → [10, 40]
Add              #     → [50]
Print            # output 50
Halt
```

Se `Mul` vier **depois** de `Add`, a precedência está invertida.

## 2. Contrastando com parênteses

`(x + y) * 2` deve emitir Add **antes** de Mul:

```text
LoadGlobal x
LoadGlobal y
Add
PushConst 2
Mul
Print
```

Use isso como teste mental (mesmo que o suite foque no demo sem parênteses extras no print).

## 3. Sessão de debug — valor 10 em vez de 50

Sintoma clássico do `D2-JS-VM-ADD` incompleto.

1. Breakpoint no `case Op::Add`.  
2. Inspecione `a` e `b` após os pops.  
3. Se `push_back(a)` sem `+ b`, o topo fica 10.  
4. Confirme que `Mul` já rodou (stack tinha dois valores antes do Add).

## 4. Sessão de debug — `unexpected token`

| Momento | Causa provável |
|---------|----------------|
| Em `let` | `D2-JS-LEX-IDENT` ainda devolve Identifier |
| Após `=` | `expression`/`term` não consumiram tokens; ou Number=0 mas ok |
| Em `print` | faltou `expect(RParen)` / Semicolon |

Imprima `current_.kind` e `current_.text` em `statement` e `expression`.

## 5. Sessão de debug — stack underflow

`Print` ou `StoreGlobal` sem expressão compilada → pop em pilha vazia.  
`Add` sem dois operandos → mesma falha. Verifique se `PREC-*` emite ops depois de dois factors/terms.

## 6. Trace de tokens de uma linha

`let x = 10;`

```text
Let | Identifier("x") | Equal | Number(10) | Semicolon
```

Se Number vier com value 0, volte a `D2-JS-LEX-NUMBER`.

## 7. Checklist pós-verde

- [ ] CLI imprime `50`
- [ ] `ctest` 100%
- [ ] Dump mental: Mul antes de Add no demo
- [ ] Keyword `letter` não vira `Let`
- [ ] Compare só marcadores `PEDAGOGY-SOLUTION` em `solutions/src/chris_js.cpp`

## 8. Extensões (fora do TODO)

AST explícito, `if`/`while`, call stack separada, disassembler — só depois do subset verde e do benchmark registrado.
