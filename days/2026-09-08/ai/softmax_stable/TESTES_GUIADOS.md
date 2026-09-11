# Testes guiados — softmax_stable

Cada caso abaixo existe como `PEDAGOGY-TEST: ID` no código de teste do starter/solutions.

## Caso 1: softmax {1,2,3}

Σp=1; p2>p0.

**PEDAGOGY-TEST:** `AI-SOFTMAX-01`

| Campo | Valor |
|-------|-------|
| ID | `AI-SOFTMAX-01` |
| Aceite | assert/retorno descrito acima |

## Caso 2: log_softmax

out[2]>out[0].

**PEDAGOGY-TEST:** `AI-SOFTMAX-02`

| Campo | Valor |
|-------|-------|
| ID | `AI-SOFTMAX-02` |
| Aceite | assert/retorno descrito acima |

## Caso 3: CE target 2

CE ≈ -log_softmax[2].

**PEDAGOGY-TEST:** `AI-SOFTMAX-03`

| Campo | Valor |
|-------|-------|
| ID | `AI-SOFTMAX-03` |
| Aceite | assert/retorno descrito acima |

## Caso 4: n inválido

retorno -1.

**PEDAGOGY-TEST:** `AI-SOFTMAX-01`

| Campo | Valor |
|-------|-------|
| ID | `AI-SOFTMAX-01` |
| Aceite | assert/retorno descrito acima |

## Mapa ID → caso

| PEDAGOGY-TEST | Casos |
|---------------|-------|
| `AI-SOFTMAX-01` | Caso 1, Caso 4 |
| `AI-SOFTMAX-02` | Caso 2 |
| `AI-SOFTMAX-03` | Caso 3 |
