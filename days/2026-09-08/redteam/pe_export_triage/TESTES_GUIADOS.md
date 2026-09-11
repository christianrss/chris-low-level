# Testes guiados — pe_export_triage

Cada caso abaixo existe como `PEDAGOGY-TEST: ID` no código de teste do starter/solutions.

## Caso 1: MZ/PE

validate true no fixture.

**PEDAGOGY-TEST:** `RT-PE-EXP-01`

| Campo | Valor |
|-------|-------|
| ID | `RT-PE-EXP-01` |
| Aceite | assert/retorno descrito acima |

## Caso 2: count

len(names) após validate.

**PEDAGOGY-TEST:** `RT-PE-EXP-02`

| Campo | Valor |
|-------|-------|
| ID | `RT-PE-EXP-02` |
| Aceite | assert/retorno descrito acima |

## Caso 3: suspicious

VirtualAlloc flagado.

**PEDAGOGY-TEST:** `RT-PE-EXP-03`

| Campo | Valor |
|-------|-------|
| ID | `RT-PE-EXP-03` |
| Aceite | assert/retorno descrito acima |

## Caso 4: sem MZ

validate false; count -1.

**PEDAGOGY-TEST:** `RT-PE-EXP-01`

| Campo | Valor |
|-------|-------|
| ID | `RT-PE-EXP-01` |
| Aceite | assert/retorno descrito acima |

## Mapa ID → caso

| PEDAGOGY-TEST | Casos |
|---------------|-------|
| `RT-PE-EXP-01` | Caso 1, Caso 4 |
| `RT-PE-EXP-02` | Caso 2 |
| `RT-PE-EXP-03` | Caso 3 |
