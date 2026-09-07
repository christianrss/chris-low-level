# Testes guiados — agent FSM

## Automatizados

| TODO | Arquivo | Caso |
|------|---------|------|
| `D5-AGENT-TRANSITION` | `starter/test_agent_fsm.py` | transição inválida levanta `ValueError` |
| `D5-AGENT-VERIFY` | `starter/test_agent_fsm.py` | retry até `FAILED` quando verify falha |
| `D5-AGENT-REPLAY` | `starter/test_agent_fsm.py` | trace adulterado falha replay |

### Caso 1: happy path

`PERCEIVE → PLAN → ACT → OBSERVE → VERIFY → DONE` com `verification(True, ...)`.

### Caso 2: retry path

Primeira verify falha → `REVISE` → segunda verify passa → `DONE`.

### Caso manual — VISUAL-01 (headless)

Imprima `trace` após simulação: seq crescente, estados coerentes com `TRANSITIONS`.
