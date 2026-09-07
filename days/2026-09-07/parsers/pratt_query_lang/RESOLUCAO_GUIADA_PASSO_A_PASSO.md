# RESOLUÇÃO GUIADA — Parsers / Pratt query lang

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `D5-PRATT-LEX` | `starter/query.py` | `lex` |
| `D5-PRATT-PARSE` | `starter/query.py` | `parse` → `expr` (infix) |
| `D5-PRATT-FIELD` | `starter/query.py` | ramo WORD em `expr` (prefix) |

Cada ID: `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` em `solutions/query.py`, `PEDAGOGY-TEST: ID` em `starter/test_query.py`.

> Edite apenas `starter/query.py` até os testes passarem.

## Baseline

```powershell
cd days/2026-09-07/parsers/pratt_query_lang/starter
python test_query.py
```

**Esperado:** FAIL — `lex` retorna `[]` ou `parse` retorna `None` / levanta erro.

---

## D5-PRATT-LEX — tokenização

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/query.py` |
| **Função / âncora** | `TODO [D5-PRATT-LEX]` em `lex` |
| **Substituir** | `return []` |
| **Não mexer** | `parse` neste passo |

### 1. O problema

Lexer vazio — `lex('lang:cpp')` não produz `COL` no índice 1.

### 2. Código completo

```python
def lex(s):
    out = []
    i = 0
    while i < len(s):
        if s[i].isspace():
            i += 1
            continue
        if s[i] in "():":
            out.append(({"(":"LP",")":"RP",":":"COL"}[s[i]], s[i]))
            i += 1
            continue
        if s[i] == '"':
            j = i + 1
            while j < len(s) and s[j] != '"':
                j += 1
            if j == len(s):
                raise ValueError("unterminated string")
            out.append(("VAL", s[i + 1 : j]))
            i = j + 1
            continue
        j = i
        while j < len(s) and not s[j].isspace() and s[j] not in "():":
            j += 1
        v = s[i:j]
        u = v.upper()
        out.append((u if u in ("AND", "OR", "NOT") else "WORD", v))
        i = j
    out.append(("EOF", ""))
    return out
```

### 3. Por que funciona?

- Delimitadores `():` viram tokens próprios — `:` não fica grudado em WORD.
- Scan de string isolado evita tratar espaço dentro de `"generated code"`.
- `EOF` artificial simplifica `peek()` no parser.

### 4. Verifique

```powershell
python -c "import sys;sys.path.insert(0,'.'); from query import lex; print(lex('lang:cpp'))"
```

**Esperado:** segundo token `('COL', ':')`. Teste completo ainda falha em parse.

---

## D5-PRATT-PARSE — Pratt com AND/OR

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/query.py` |
| **Função / âncora** | `TODO [D5-PRATT-PARSE]` dentro de `parse` |
| **Substituir** | stub `return None` e corpo de `expr` |
| **Não mexer** | `lex` já pronto |

### 1. O problema

Sem `expr`, `parse("a OR b AND c")` não produz árvore com AND mais forte que OR.

### 2. Código completo (estrutura `parse` + `expr`)

Implemente `parse` chamando `lex`, defina `peek`/`take`, e dentro de `parse`:

```python
def parse(s):
    toks = lex(s)
    pos = 0

    def peek():
        return toks[pos]

    def take():
        nonlocal pos
        t = toks[pos]
        pos += 1
        return t

    def expr(minbp=0):
        nonlocal pos
        typ, val = take()
        if typ == "NOT":
            left = ("not", expr(30))
        elif typ == "LP":
            left = expr(0)
            if take()[0] != "RP":
                raise ValueError("missing )")
        elif typ == "WORD":
            if peek()[0] == "COL":
                take()
                t, v = take()
                if t not in ("WORD", "VAL"):
                    raise ValueError("field value")
                left = ("field", val, v)
            else:
                left = ("text", val)
        elif typ == "VAL":
            left = ("text", val)
        else:
            raise ValueError("expected expression")
        while True:
            op = peek()[0]
            if op not in ("AND", "OR"):
                break
            lbp, rbp = (20, 21) if op == "AND" else (10, 11)
            if lbp < minbp:
                break
            take()
            right = expr(rbp)
            left = (op.lower(), left, right)
        return left

    tree = expr()
    if peek()[0] != "EOF":
        raise ValueError("trailing input")
    return tree
```

> O ramo `WORD`+`COL` acima já cobre `D5-PRATT-FIELD` — se preferir em dois commits mentais, deixe `("text", val)` primeiro e adicione field depois.

### 3. Por que funciona?

- `minbp` no loop infix implementa “pare quando operador é mais fraco que o contexto”.
- `rbp = lbp+1` força `AND` a agrupar `b` e `c` antes do `OR` externo.
- Checagem `EOF` rejeita lixo após expressão válida.

### 4. Verifique

```powershell
python test_query.py
```

**Esperado:** `chris-pratt-query tests passed` (lex + parse + field juntos).

---

## D5-PRATT-FIELD — `field:value`

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/query.py` |
| **Função / âncora** | `TODO [D5-PRATT-FIELD]` no ramo `WORD` de `expr` |
| **Substituir** | ramo que só faz `("text", val)` |
| **Inserir** | bloco `if peek()[0]=="COL": ... ("field", ...)` |

### 1. O problema

Sem lookahead, `lang:cpp` vira texto `lang` e tokens órfãos — teste de query com `lang:cpp AND NOT ...` falha.

### 2. Algoritmo

```text
após take WORD como val:
  se peek()==COL: take COL; take valor; left=("field",val,v)
  senão: left=("text",val)
```

### 3. Por que funciona?

- Um token de lookahead — padrão clássico LL(1) embutido no prefix Pratt.
- Valor `VAL` permite strings com espaço após `text:`.

### 4. Verifique

Confirme AST raiz `("and", ...)` no teste `D5-PRATT-FIELD`. Rode suite completa.

---

## Debug / depuração

| Sintoma | Correção |
|---------|----------|
| OR vence AND | troque `(10,11)` e `(20,21)` |
| `missing )` falso | verifique se `take()` consome RP |
| `trailing input` com query válida | falta consumir até EOF |
| field não forma | `peek` antes de decidir text vs field |

Imprima `(pos, peek(), minbp)` a cada volta do loop infix.

---

## Relatório de resolução

| Campo | Sua resposta |
|-------|----------------|
| Data | |
| Binding power que você invertiu (se houver) | |
| Query inválida que você testou manualmente | |
| `python test_query.py` | PASS / FAIL |
