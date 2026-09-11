# Testes guiados — clvm_peephole_opt

Cada caso abaixo existe como `PEDAGOGY-TEST: ID` no código de teste do starter/solutions.

## Caso 1: match PUSH0+ADD

Hex `01 00 00 00 00 02` → match=1.

**PEDAGOGY-TEST:** `CLVM-PEEP-01`

| Campo | Valor |
|-------|-------|
| ID | `CLVM-PEEP-01` |
| Aceite | assert/retorno descrito acima |

## Caso 2: fold 2+3

Emite `01 05 00 00 00`, out_len=5.

**PEDAGOGY-TEST:** `CLVM-PEEP-02`

| Campo | Valor |
|-------|-------|
| ID | `CLVM-PEEP-02` |
| Aceite | assert/retorno descrito acima |

## Caso 3: saved bytes

Padrão fold economiza 6.

**PEDAGOGY-TEST:** `CLVM-PEEP-03`

| Campo | Valor |
|-------|-------|
| ID | `CLVM-PEEP-03` |
| Aceite | assert/retorno descrito acima |

## Caso 4: não-match

PUSH 1+ADD não casa.

**PEDAGOGY-TEST:** `CLVM-PEEP-01`

| Campo | Valor |
|-------|-------|
| ID | `CLVM-PEEP-01` |
| Aceite | assert/retorno descrito acima |

## Mapa ID → caso

| PEDAGOGY-TEST | Casos |
|---------------|-------|
| `CLVM-PEEP-01` | Caso 1, Caso 4 |
| `CLVM-PEEP-02` | Caso 2 |
| `CLVM-PEEP-03` | Caso 3 |
