# Testes guiados — tool_protocol_fsm

Cada caso abaixo existe como `PEDAGOGY-TEST: ID` no código de teste do starter/solutions.

## Caso 1: call

IDLE→CALLING.

**PEDAGOGY-TEST:** `AGT-TOOL-01`

| Campo | Valor |
|-------|-------|
| ID | `AGT-TOOL-01` |
| Aceite | assert/retorno descrito acima |

## Caso 2: response ok

WAITING→DONE.

**PEDAGOGY-TEST:** `AGT-TOOL-02`

| Campo | Valor |
|-------|-------|
| ID | `AGT-TOOL-02` |
| Aceite | assert/retorno descrito acima |

## Caso 3: validate

nome vazio False.

**PEDAGOGY-TEST:** `AGT-TOOL-03`

| Campo | Valor |
|-------|-------|
| ID | `AGT-TOOL-03` |
| Aceite | assert/retorno descrito acima |

## Caso 4: aresta ilegal

ValueError; estado intacto.

**PEDAGOGY-TEST:** `AGT-TOOL-01`

| Campo | Valor |
|-------|-------|
| ID | `AGT-TOOL-01` |
| Aceite | assert/retorno descrito acima |

## Mapa ID → caso

| PEDAGOGY-TEST | Casos |
|---------------|-------|
| `AGT-TOOL-01` | Caso 1, Caso 4 |
| `AGT-TOOL-02` | Caso 2 |
| `AGT-TOOL-03` | Caso 3 |
