# Day 12 — Mini xdbg da CLVM

Um projeto depth-first (6–8 h): debugger **in-process** da imagem CLVM
v1 + ISA estendida. Hex dump, disasm, single-step, duas pilhas e RAM.
Sem GUI Win32.

## Projeto (1)

| # | Projeto | Fundamento | Horas |
|---|---------|------------|------:|
| 1 | `systems/clvm_xdbg` | views + step observável sobre a ISA Dia 04 | 6–8 |

## Como estudar

1. [`START_HERE.md`](START_HERE.md)
2. [`ATIVIDADES.md`](ATIVIDADES.md) e `ASSESSMENT.yaml`
3. No projeto: TEORIA → EXERCICIOS M1–M6 → `starter/src/session.cpp`

## Capstone

[`projects/chris-debugger`](../../projects/chris-debugger/) (views/step).
A ISA continua em [`projects/chris-vm`](../../projects/chris-vm/).

## Validação

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-12
python scripts/day_contract_check.py --day 2026-09-12
python scripts/run_day_tests.py --day 2026-09-12 --mode starter --expect-fail
python scripts/run_day_tests.py --day 2026-09-12 --mode solutions
python scripts/run_depth_mutants.py --day 2026-09-12
python scripts/cycle_contract_check.py --cycle depth-core-01
```
