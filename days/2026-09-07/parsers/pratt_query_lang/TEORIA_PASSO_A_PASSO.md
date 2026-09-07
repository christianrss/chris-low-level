# Teoria passo a passo — Pratt parser para query lang (D5-PRATT)

## 1. O que estamos construindo

Um **lexer + Pratt parser** para queries estilo smart-grep:

```text
lang:cpp AND (symbol:alloc OR text:"arena")
```

Sem Lark, sem yacc — só Python com binding power, AST em tuplas e subset: `AND`, `OR`, `NOT`, parênteses, `field:value`, strings entre aspas.

TODOs: `D5-PRATT-LEX`, `D5-PRATT-PARSE`, `D5-PRATT-FIELD`.

## 2. Por que Pratt em vez de recursão ingênua

Gramáticas com precedência (`AND` > `OR`) e associatividade exigem ou tabelas LALR ou **Pratt parsing** (top-down operator precedence). Pratt separa claramente **prefix** (átomos, `NOT`, grupos) de **infix** (loop com `min_bp`). Para uma DSL de busca embutida em ferramenta, Pratt cabe em ~40 linhas e é fácil de auditar — o mesmo padrão usado em calculadoras e em parsers de filtros internos.

## 3. Lexer (`D5-PRATT-LEX`)

### O quê

`lex(s) → [(tipo, valor), ...]` com tipos: `WORD`, `VAL` (string), `COL`, `LP`, `RP`, `AND`, `OR`, `NOT`, `EOF`.

### Como

```text
i ← 0
enquanto i < len(s):
  pular whitespace
  se '(' ou ')' ou ':': emitir LP/RP/COL
  se '"': scan até próxima '"'; emitir VAL; erro se não fechar
  senão: scan identificador até whitespace ou delimitador
         se upper em {AND,OR,NOT}: keyword; senão WORD
emitir EOF
```

### Por quê

Tokenizar antes de parsear isola **sintaxe de caracteres** (aspas, `:`) da **sintaxe de operadores**. Sem lexer, `lang:cpp` vira três tokens ambíguos (`lang`, `:`, `cpp`) misturados com texto livre.

### Trace manual — `lang:cpp`

```text
pos 0: scan WORD "lang"
pos 4: ':' → COL
pos 5: scan WORD "cpp"
EOF
tokens: [("WORD","lang"),("COL",":"),("WORD","cpp"),("EOF","")]
```

### Invariantes

- Sempre termina com `EOF`.
- Keywords case-insensitive (`and` → `AND`).
- String sem `"` final → `ValueError`.

### Bugs comuns

| Sintoma | Causa |
|---------|-------|
| `COL` no meio de WORD | não parou scan em `:` |
| string vazia `""` | loop `j` não avança — OK, VAL="" |
| `AND` como identificador em `android` | só match exato após scan |

## 4. Pratt parser — precedência (`D5-PRATT-PARSE`)

### O quê

`parse(s)` chama `expr(min_bp=0)` que:
1. Lê **prefix** (NOT, `(`, WORD, VAL).
2. Loop **infix**: enquanto próximo operador tem `lbp >= min_bp`, consome operador e RHS com `expr(rbp)`.

Binding powers deste lab:

| Operador | lbp | rbp | Associação |
|----------|-----|-----|------------|
| OR | 10 | 11 | esquerda |
| AND | 20 | 21 | esquerda |
| NOT (prefix) | — | 30 | prefix alto |

### Como — estrutura `expr`

```text
prefix:
  NOT → ("not", expr(30))
  LP → expr(0); exige RP
  WORD → ver seção field (D5-PRATT-FIELD)
  VAL → ("text", val)

infix loop:
  peek AND/OR
  se lbp < min_bp: break
  take operador; right ← expr(rbp); left ← (op.lower(), left, right)
```

### Por quê

`a OR b AND c` deve parsear como `OR(a, AND(b,c))` porque AND tem binding maior. O par `(lbp, rbp)` com `rbp = lbp+1` força associatividade à esquerda e impede que OR “engula” o AND interno.

### Trace manual — `a OR b AND c`

```text
expr(0): prefix → ("text","a")
  peek OR, lbp=10 >= 0 → take OR, rhs expr(11):
    prefix → ("text","b")
    peek AND, lbp=20 >= 11 → take AND, rhs expr(21):
      prefix → ("text","c")
      peek EOF → break
    left = ("and", ("text","b"), ("text","c"))
  left = ("or", ("text","a"), ("and", ...))
```

### Diagrama — fluxo Pratt

```text
tokens ──► expr(min_bp)
              │
    ┌─────────┴─────────┐
    ▼                   ▼
 prefix            infix loop
 (NOT/LP/WORD)     AND/OR enquanto lbp≥min_bp
```

### Invariantes

- Entrada totalmente consumida: após `expr(0)`, `peek()==EOF`.
- `(` sem `)` → `ValueError`.
- AST = tuplas aninhadas, não objetos OO (suficiente para retrieval).

### Bugs comuns

- Inverter OR/AND binding → `AND` vence `OR` na árvore errada.
- RHS com `min_bp` em vez de `rbp` → associatividade quebrada.
- Aceitar `a b` sem operador — deve falhar no EOF com input sobrando ou no prefix.

## 5. Field syntax (`D5-PRATT-FIELD`)

### O quê

`lang:cpp` → `("field", "lang", "cpp")`. Texto livre `hello` → `("text", "hello")`. Valor pode ser string: `text:"generated code"`.

### Como

Após ler WORD no prefix:

```text
se peek() == COL:
  take COL
  take próximo token (WORD ou VAL) como valor
  left ← ("field", name, value)
senão:
  left ← ("text", name)
```

### Por quê

Um token de **lookahead** distingue filtro estruturado de palavra solta. É o mesmo padrão de Lucene/SQL `column = value` reduzido a dois tokens — sem isso, `lang:cpp` seria três nós sem semântica de campo.

### Trace manual — query mista

```text
parse('lang:cpp AND NOT text:"generated code"')
AST raiz: ("and",
  ("field","lang","cpp"),
  ("not", ("field","text","generated code")))
```

### Invariantes

- `field:` sem valor → `ValueError`.
- Valor após `:` deve ser WORD ou VAL, não `AND`.

## 6. AST como contrato de retrieval

| Nó | Formato | Uso futuro |
|----|---------|------------|
| texto | `("text", w)` | match full-text |
| campo | `("field", k, v)` | índice invertido por campo |
| bool | `("and"|"or", l, r)` | combinação |
| not | `("not", sub)` | negação |

## 7. Complexidade

| Fase | Tempo | Espaço |
|------|-------|--------|
| `lex` | O(n) | O(tokens) |
| `parse` | O(n) | O(altura AST) |

## 8. Comparação com produção

| Este lab | Elasticsearch / SQL |
|----------|---------------------|
| Tuplas Python | AST tipado + planner |
| 2 operadores bool | NOT, XOR, ranges |
| `field:value` | analyzers, fuzzy, boost |

O transferível é **precedência correta + campos**, não o formato de índice.

## 9. Entradas inválidas (rejeitar)

- `"unterminated`
- `a AND` (operador sem RHS)
- `(a OR b` sem `)`
- `field:` sem valor
- `a b` sem operador entre átomos

## 10. Passo a passo guiado (ordem dos TODOs)

1. `D5-PRATT-LEX` — `lex` em `starter/query.py`.
2. `D5-PRATT-PARSE` — `expr` + loop infix em `parse`.
3. `D5-PRATT-FIELD` — lookahead `COL` no prefix WORD.
4. `python starter/test_query.py` → `chris-pratt-query tests passed`.

## 11. Como saber se está correto

- `lex('lang:cpp')[1][0] == "COL"`.
- `parse("a OR b AND c") == ("or",("text","a"),("and",("text","b"),("text","c")))`.
- `parse('lang:cpp AND NOT text:"generated code"')[0] == "and"`.

## 12. Bugs comuns (checklist)

| Sintoma | Causa típica |
|---------|----------------|
| OR ganha de AND | binding invertido |
| `field` não forma | não consumiu COL/valor |
| trailing input | não checou EOF |
| NOT sem filho | prefix incompleto |

## 13. Por quê este módulo existe

Filtros de código e logs são **linguagens pequenas** com precedência real. Cada TODO protege uma camada que ferramentas como `ripgrep --type` e buscas em monorepo assumem: tokenização, árvore bool e campos nomeados.
