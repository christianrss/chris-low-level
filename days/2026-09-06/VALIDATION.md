# VALIDATION — Day 06

## Gates

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-06
python scripts/run_day_tests.py --day 2026-09-06 --mode solutions
python scripts/run_day_tests.py --day 2026-09-06 --mode starter --expect-fail
```

## Expectativas

| Gate | Esperado |
|------|----------|
| pedagogy_check | PASS — 11 módulos, ~42 TODOs |
| solutions | PASS |
| starter | FAIL até TODOs |
| Anti-padding | zero `Nota pedagógica` gerada |

## Auditoria rápida anti-padding

```powershell
rg "Nota pedagógica" days/2026-09-06
rg "revise o TODO e escreva um parágrafo" days/2026-09-06
```

Ambos devem retornar vazio.
