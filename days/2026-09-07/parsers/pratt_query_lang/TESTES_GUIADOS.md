# Testes guiados — Pratt query language

## Automatizados

| TODO | Arquivo | Caso |
|------|---------|------|
| `D5-PRATT-LEX` | `starter/test_query.py` | string não terminada → erro |
| `D5-PRATT-PARSE` | `starter/test_query.py` | precedência `AND` > `OR` |
| `D5-PRATT-FIELD` | `starter/test_query.py` | `word:val` → nó `field` |

### Caso 1: lexer

`"foo"` tokeniza como `VAL`; `AND` case-insensitive.

### Caso 2: parse

`a OR b AND c` agrupa como `or(a, and(b,c))`.

### Caso 3: field

`title:"hello"` produz `('field','title','hello')`.
