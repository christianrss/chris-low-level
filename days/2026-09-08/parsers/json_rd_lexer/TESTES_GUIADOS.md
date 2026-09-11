# Testes guiados — json_rd_lexer

Cada caso abaixo existe como `PEDAGOGY-TEST: ID` no código de teste do starter/solutions.

## Caso 1: skip_ws

cursor após espaços.

**PEDAGOGY-TEST:** `PAR-JSON-LEX-01`

| Campo | Valor |
|-------|-------|
| ID | `PAR-JSON-LEX-01` |
| Aceite | assert/retorno descrito acima |

## Caso 2: next_token

LBRACE etc.

**PEDAGOGY-TEST:** `PAR-JSON-LEX-02`

| Campo | Valor |
|-------|-------|
| ID | `PAR-JSON-LEX-02` |
| Aceite | assert/retorno descrito acima |

## Caso 3: lex_count

{"a":1} → 5.

**PEDAGOGY-TEST:** `PAR-JSON-LEX-03`

| Campo | Valor |
|-------|-------|
| ID | `PAR-JSON-LEX-03` |
| Aceite | assert/retorno descrito acima |

## Caso 4: string aberta

retorno -1.

**PEDAGOGY-TEST:** `PAR-JSON-LEX-02`

| Campo | Valor |
|-------|-------|
| ID | `PAR-JSON-LEX-02` |
| Aceite | assert/retorno descrito acima |

## Mapa ID → caso

| PEDAGOGY-TEST | Casos |
|---------------|-------|
| `PAR-JSON-LEX-01` | Caso 1 |
| `PAR-JSON-LEX-02` | Caso 2, Caso 4 |
| `PAR-JSON-LEX-03` | Caso 3 |
