# Testes guiados — wasm_section_header

Cada caso abaixo existe como `PEDAGOGY-TEST: ID` no código de teste do starter/solutions.

## Caso 1: magic

\0asm → 1.

**PEDAGOGY-TEST:** `TOOL-WASM-01`

| Campo | Valor |
|-------|-------|
| ID | `TOOL-WASM-01` |
| Aceite | assert/retorno descrito acima |

## Caso 2: version

dword 1 → 1.

**PEDAGOGY-TEST:** `TOOL-WASM-02`

| Campo | Valor |
|-------|-------|
| ID | `TOOL-WASM-02` |
| Aceite | assert/retorno descrito acima |

## Caso 3: section id 1/2

retorna 1 ou 2.

**PEDAGOGY-TEST:** `TOOL-WASM-03`

| Campo | Valor |
|-------|-------|
| ID | `TOOL-WASM-03` |
| Aceite | assert/retorno descrito acima |

## Caso 4: id 9

retorna 0.

**PEDAGOGY-TEST:** `TOOL-WASM-03`

| Campo | Valor |
|-------|-------|
| ID | `TOOL-WASM-03` |
| Aceite | assert/retorno descrito acima |

## Mapa ID → caso

| PEDAGOGY-TEST | Casos |
|---------------|-------|
| `TOOL-WASM-01` | Caso 1 |
| `TOOL-WASM-02` | Caso 2 |
| `TOOL-WASM-03` | Caso 3, Caso 4 |
