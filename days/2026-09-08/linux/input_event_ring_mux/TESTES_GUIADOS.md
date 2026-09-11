# Testes guiados — input_event_ring_mux

Cada caso abaixo existe como `PEDAGOGY-TEST: ID` no código de teste do starter/solutions.

## Caso 1: mux 10

mux_push source=1 value=10 → 0.

**PEDAGOGY-TEST:** `LIN-MUX-03`

| Campo | Valor |
|-------|-------|
| ID | `LIN-MUX-03` |
| Aceite | assert/retorno descrito acima |

## Caso 2: FIFO

pop 10 depois pop -3.

**PEDAGOGY-TEST:** `LIN-MUX-02`

| Campo | Valor |
|-------|-------|
| ID | `LIN-MUX-02` |
| Aceite | assert/retorno descrito acima |

## Caso 3: overflow

5º push com CAP=4 → -1.

**PEDAGOGY-TEST:** `LIN-MUX-01`

| Campo | Valor |
|-------|-------|
| ID | `LIN-MUX-01` |
| Aceite | assert/retorno descrito acima |

## Caso 4: vazio

pop em anel vazio → -1.

**PEDAGOGY-TEST:** `LIN-MUX-02`

| Campo | Valor |
|-------|-------|
| ID | `LIN-MUX-02` |
| Aceite | assert/retorno descrito acima |

## Mapa ID → caso

| PEDAGOGY-TEST | Casos |
|---------------|-------|
| `LIN-MUX-01` | Caso 3 |
| `LIN-MUX-02` | Caso 2, Caso 4 |
| `LIN-MUX-03` | Caso 1 |
