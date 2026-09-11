# Testes guiados — shader_stage_fsm

Cada caso abaixo existe como `PEDAGOGY-TEST: ID` no código de teste do starter/solutions.

## Caso VISUAL-01 — headless

FSM sem janela: trace de transições no stdout/assert. Não há pixel buffer neste módulo.

## Caso 1: can EDIT→COMPILE

retorna 1.

**PEDAGOGY-TEST:** `GFX-SHADER-FSM-01`

| Campo | Valor |
|-------|-------|
| ID | `GFX-SHADER-FSM-01` |
| Aceite | assert/retorno descrito acima |

## Caso 2: apply

estado avança; ilegal -1.

**PEDAGOGY-TEST:** `GFX-SHADER-FSM-02`

| Campo | Valor |
|-------|-------|
| ID | `GFX-SHADER-FSM-02` |
| Aceite | assert/retorno descrito acima |

## Caso 3: illegal EDIT→READY

retorna 1.

**PEDAGOGY-TEST:** `GFX-SHADER-FSM-03`

| Campo | Valor |
|-------|-------|
| ID | `GFX-SHADER-FSM-03` |
| Aceite | assert/retorno descrito acima |

## Caso 4: estado intacto

após aresta ilegal stage permanece.

**PEDAGOGY-TEST:** `GFX-SHADER-FSM-02`

| Campo | Valor |
|-------|-------|
| ID | `GFX-SHADER-FSM-02` |
| Aceite | assert/retorno descrito acima |

## Mapa ID → caso

| PEDAGOGY-TEST | Casos |
|---------------|-------|
| `GFX-SHADER-FSM-01` | Caso 1 |
| `GFX-SHADER-FSM-02` | Caso 2, Caso 4 |
| `GFX-SHADER-FSM-03` | Caso 3 |
