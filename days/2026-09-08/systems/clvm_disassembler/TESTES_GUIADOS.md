# Testes guiados — clvm_disassembler

Cada caso abaixo existe como `PEDAGOGY-TEST: ID` no código de teste do starter/solutions.

## Caso 1: PUSH 42

Entrada `01 2A 00 00 00`. Esperado: line `PUSH 42`, size 5, retorno 0.

**PEDAGOGY-TEST:** `CLVM-DIS-01`

| Campo | Valor |
|-------|-------|
| ID | `CLVM-DIS-01` |
| Aceite | assert/retorno descrito acima |

## Caso 2: JMP 10

Entrada `09 0A 00`. Esperado: `JMP 10`, size 3.

**PEDAGOGY-TEST:** `CLVM-DIS-02`

| Campo | Valor |
|-------|-------|
| ID | `CLVM-DIS-02` |
| Aceite | assert/retorno descrito acima |

## Caso 3: programa 7 bytes

`01 2A 00 00 00 02 08` → 3 linhas PUSH/ADD/HALT.

**PEDAGOGY-TEST:** `CLVM-DIS-03`

| Campo | Valor |
|-------|-------|
| ID | `CLVM-DIS-03` |
| Aceite | assert/retorno descrito acima |

## Caso 4: opcode FF

Retorno < 0; sem listing parcial mentiroso.

**PEDAGOGY-TEST:** `CLVM-DIS-03`

| Campo | Valor |
|-------|-------|
| ID | `CLVM-DIS-03` |
| Aceite | assert/retorno descrito acima |

## Mapa ID → caso

| PEDAGOGY-TEST | Casos |
|---------------|-------|
| `CLVM-DIS-01` | Caso 1 |
| `CLVM-DIS-02` | Caso 2 |
| `CLVM-DIS-03` | Caso 3, Caso 4 |
