# Testes guiados — duplex_event_pipe

Cada caso abaixo existe como `PEDAGOGY-TEST: ID` no código de teste do starter/solutions.

## Caso 1: 48 bytes

eventsWritten==2.

**PEDAGOGY-TEST:** `ND-DUPLEX-01`

| Campo | Valor |
|-------|-------|
| ID | `ND-DUPLEX-01` |
| Aceite | assert/retorno descrito acima |

## Caso 2: read frames

eventsRead acompanha.

**PEDAGOGY-TEST:** `ND-DUPLEX-02`

| Campo | Valor |
|-------|-------|
| ID | `ND-DUPLEX-02` |
| Aceite | assert/retorno descrito acima |

## Caso 3: metrics

objeto com ambos contadores.

**PEDAGOGY-TEST:** `ND-DUPLEX-03`

| Campo | Valor |
|-------|-------|
| ID | `ND-DUPLEX-03` |
| Aceite | assert/retorno descrito acima |

## Caso 4: residual 25

1 evento + 1 byte buffer.

**PEDAGOGY-TEST:** `ND-DUPLEX-01`

| Campo | Valor |
|-------|-------|
| ID | `ND-DUPLEX-01` |
| Aceite | assert/retorno descrito acima |

## Mapa ID → caso

| PEDAGOGY-TEST | Casos |
|---------------|-------|
| `ND-DUPLEX-01` | Caso 1, Caso 4 |
| `ND-DUPLEX-02` | Caso 2 |
| `ND-DUPLEX-03` | Caso 3 |
