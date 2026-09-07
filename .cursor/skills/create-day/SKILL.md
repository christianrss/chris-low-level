---
name: create-day
description: >-
  Scaffold or expand a learning day (days/YYYY-MM-DD) with multi-trilha parity,
  OpenSpec alignment, and day_contract gates. Use when creating a new day, adding
  modules to an existing day, or fixing day completeness (README/MANIFEST/trilhas).
---

# Create / expand learning day

## When to use

- New day under `days/YYYY-MM-DD/`
- Expanding tier-A day (missing red team, quantum, AI, Node, etc.)
- Syncing infra after adding modules

## Reference

- Baseline: `days/2026-09-06` (13 modules, 7 trilhas)
- Specs: `openspec/specs/day-contract/`, `openspec/specs/day-layout/`
- Template: `docs/templates/ATIVIDADES_DAY_TEMPLATE.md`, `docs/templates/DAY_CONTRACT_TEMPLATE.yaml`

## Checklist

### 0. Plan (OpenSpec)

- [ ] `/opsx:propose` or draft `openspec/changes/<slug>/proposal.md`
- [ ] `module_count` target and `required_tracks` from `tracks.yaml` or `day.contract.yaml`
- [ ] User ACK if plan is narrower than day-contract spec

### 1. Modules

- [ ] Each module: 7 MD files + `starter/` + `solutions/` per `docs/PEDAGOGY_STANDARD.md`
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
python scripts/run_day_tests.py --day YYYY-MM-DD --mode solutions
```

### 5. Archive (OpenSpec)

- [ ] Move change to `openspec/changes/archive/YYYY-MM-DD-<slug>/`

## Anti-patterns

- GFX-only or CLVM-only plan on tier-A day without other trilhas
- `generate_day_scaffold.py` overwriting curated START_HERE
- `MANIFEST.modules` ≠ módulos no filesystem
