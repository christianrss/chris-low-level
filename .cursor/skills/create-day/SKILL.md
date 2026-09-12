---
name: create-day
description: >-
  Scaffold a depth-first learning day (days/YYYY-MM-DD) with one substantial
  project, OpenSpec alignment, cycle coverage, and executable quality gates.
  Legacy multi-track days remain supported but are not the model for new days.
---

# Create / expand learning day

## When to use

- New day under `days/YYYY-MM-DD/`
- Expanding tier-A day (missing red team, quantum, AI, Node, etc.)
- Syncing infra after adding modules

## Profiles

- New days after 2026-09-11: `depth_first`, exactly 1 project, 6–8 hours
- Code authenticity reference: `days/2026-09-03/graphics/dual_backend_3d`
- Thematic coherence reference: `days/2026-09-06`
- Do not copy either reference's module count
- Specs: `openspec/specs/day-contract/`, `openspec/specs/day-layout/`
- Template: `docs/templates/ATIVIDADES_DAY_TEMPLATE.md`, `docs/templates/DAY_CONTRACT_TEMPLATE.yaml`

## Checklist

### 0. Plan (OpenSpec)

- [ ] `/opsx:propose` or draft `openspec/changes/<slug>/proposal.md`
- [ ] Exactly one authentic project and honest 6–8 hour scope
- [ ] `primary_lane` and 7–10 day `cycle` selected
- [ ] `ASSESSMENT.yaml`: 6–10 milestones, student-owned files, behaviors and failures

### 1. Modules

- [ ] One project: 7 MD files + `starter/` + `solutions/` per `docs/PEDAGOGY_STANDARD.md`
- [ ] Starter contains infrastructure/contracts but no more than 15% of final core logic
- [ ] Expected authored delta is at least 250 substantive production lines
- [ ] `TODO [ID]`, `PEDAGOGY-TEST`, `PEDAGOGY-SOLUTION`, RESOLUCAO placement per TODO

### 2. Day infra (same module count everywhere)

- [ ] `README.md` — título, tabela N módulos, horas
- [ ] `START_HERE.md` — blocos por trilha (não template genérico)
- [ ] `ATIVIDADES.md` — checkpoints conceituais
- [ ] `TODO_MAP.md` — todos os TODO ids dos starters
- [ ] `VALIDATION.md` — tabela de módulos + gates
- [ ] `MANIFEST.json` via `python scripts/generate_day_scaffold.py --day DATE --manifest-only`

### 3. Portfolio wiring

- [ ] `docs/LEARNING_PATHS.md` — nova seção ou linha por módulo
- [ ] `scripts/module_project_map.py` — capstone `projects/chris-*`

### 4. Gates

```powershell
python scripts/pedagogy_check_unified.py --day YYYY-MM-DD
python scripts/day_contract_check.py --day YYYY-MM-DD
python scripts/run_day_tests.py --day YYYY-MM-DD --mode starter --expect-fail
python scripts/run_day_tests.py --day YYYY-MM-DD --mode solutions
python scripts/run_depth_mutants.py --day YYYY-MM-DD
python scripts/cycle_contract_check.py --cycle CYCLE_ID
```

### 5. Archive (OpenSpec)

- [ ] Move change to `openspec/changes/archive/YYYY-MM-DD-<slug>/`

## Anti-patterns

- Adding 13 track-parity modules to a new depth-first day
- Three-stub micro-labs presented as a project
- Generated theory/resolution written only to satisfy line thresholds
- `generate_day_scaffold.py` overwriting curated START_HERE
- `MANIFEST.modules` ≠ módulos no filesystem
