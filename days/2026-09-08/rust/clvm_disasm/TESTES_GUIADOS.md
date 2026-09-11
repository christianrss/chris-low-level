# Testes guiados — clvm_disasm

Cada caso abaixo existe como `PEDAGOGY-TEST: ID` no código de teste do starter/solutions.

## Caso 1: opcode_name

HALT/ADD Some; 0xFF None.

**PEDAGOGY-TEST:** `CLVM-RS-DIS-01`

| Campo | Valor |
|-------|-------|
| ID | `CLVM-RS-DIS-01` |
| Aceite | assert/retorno descrito acima |

## Caso 2: sizes

PUSH=5 JMP=3 ADD=1.

**PEDAGOGY-TEST:** `CLVM-RS-DIS-02`

| Campo | Valor |
|-------|-------|
| ID | `CLVM-RS-DIS-02` |
| Aceite | assert/retorno descrito acima |

## Caso 3: listing

PUSH 42 + HALT Ok.

**PEDAGOGY-TEST:** `CLVM-RS-DIS-03`

| Campo | Valor |
|-------|-------|
| ID | `CLVM-RS-DIS-03` |
| Aceite | assert/retorno descrito acima |

## Caso 4: truncated

PUSH incompleto → Err.

**PEDAGOGY-TEST:** `CLVM-RS-DIS-03`

| Campo | Valor |
|-------|-------|
| ID | `CLVM-RS-DIS-03` |
| Aceite | assert/retorno descrito acima |

## Mapa ID → caso

| PEDAGOGY-TEST | Casos |
|---------------|-------|
| `CLVM-RS-DIS-01` | Caso 1 |
| `CLVM-RS-DIS-02` | Caso 2 |
| `CLVM-RS-DIS-03` | Caso 3, Caso 4 |
