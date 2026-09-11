# Testes guiados — pe_export_span

Cada caso abaixo existe como `PEDAGOGY-TEST: ID` no código de teste do starter/solutions.

## Caso 1: IsPeFile

MZ+PE em 0x80 → true.

**PEDAGOGY-TEST:** `DN-PE-EXP-01`

| Campo | Valor |
|-------|-------|
| ID | `DN-PE-EXP-01` |
| Aceite | assert/retorno descrito acima |

## Caso 2: e_lfanew

TryGetPeOffset → 0x80.

**PEDAGOGY-TEST:** `DN-PE-EXP-02`

| Campo | Valor |
|-------|-------|
| ID | `DN-PE-EXP-02` |
| Aceite | assert/retorno descrito acima |

## Caso 3: export RVA

→ 0x1000.

**PEDAGOGY-TEST:** `DN-PE-EXP-03`

| Campo | Valor |
|-------|-------|
| ID | `DN-PE-EXP-03` |
| Aceite | assert/retorno descrito acima |

## Caso 4: curto

buffer <0x40 → false.

**PEDAGOGY-TEST:** `DN-PE-EXP-01`

| Campo | Valor |
|-------|-------|
| ID | `DN-PE-EXP-01` |
| Aceite | assert/retorno descrito acima |

## Mapa ID → caso

| PEDAGOGY-TEST | Casos |
|---------------|-------|
| `DN-PE-EXP-01` | Caso 1, Caso 4 |
| `DN-PE-EXP-02` | Caso 2 |
| `DN-PE-EXP-03` | Caso 3 |
