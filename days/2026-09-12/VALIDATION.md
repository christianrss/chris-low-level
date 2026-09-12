# Validação — 2026-09-12

| Item | Esperado |
|------|----------|
| Projeto | `systems/clvm_xdbg` |
| Perfil | `depth_first`, 6–8 h, lane `systems`, ciclo `depth-core-01` |
| Starter | Falha nos testes do shell (`--expect-fail`) |
| Solutions | CTest `xdbg_session` PASS |
| Mutantes | `MUTANT-NO-BOUNDS`, `MUTANT-OPSIZE` |
| Capstone | `projects/chris-debugger` (views/step); ISA em `projects/chris-vm` |

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-12
python scripts/day_contract_check.py --day 2026-09-12
python scripts/run_day_tests.py --day 2026-09-12 --mode starter --expect-fail
python scripts/run_day_tests.py --day 2026-09-12 --mode solutions
python scripts/run_depth_mutants.py --day 2026-09-12
python scripts/cycle_contract_check.py --cycle depth-core-01
```
