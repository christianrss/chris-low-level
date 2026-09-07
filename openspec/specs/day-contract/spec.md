# Day contract

Capability: completude de um dia publicado (escopo multi-trilha + infra consistente).

## Requirements

### Requirement: Module count consistency

The system SHALL keep the same module count across README, ATIVIDADES, MANIFEST (if `modules` field present), and actual module folders.

#### Scenario: Count matches filesystem

- **WHEN** `day_contract_check` runs on a day
- **THEN** `len(find_modules(day))` SHALL equal the module count declared in README and ATIVIDADES
- **AND** if `MANIFEST.json` has a `modules` field, it SHALL match

### Requirement: Tier-A track coverage

For days listed in `tracks.yaml` under `tier_a`, the system SHALL include at least one module per `required_tracks` entry.

#### Scenario: Day 07 includes quantum and red team

- **WHEN** checking day `2026-09-07`
- **THEN** at least one module SHALL exist under `quantum/` and `redteam/`

### Requirement: Learning path wiring

Each module in a tier-A day SHALL be referenced in `docs/LEARNING_PATHS.md` or `scripts/module_project_map.py`.

#### Scenario: New module appears in portfolio map

- **WHEN** a module `days/2026-09-07/redteam/hid_report_fuzz` exists
- **THEN** `2026-09-07/redteam/hid_report_fuzz` SHALL appear in `module_project_map.py` or `LEARNING_PATHS.md`

### Requirement: Scaffold safeguard

The system SHALL NOT overwrite curated `START_HERE.md` or `TODO_MAP.md` via `generate_day_scaffold.py` unless `--overwrite-docs` is passed.

#### Scenario: Manifest-only regeneration

- **WHEN** regenerating inventory for an existing curated day
- **THEN** operators SHALL use `generate_day_scaffold.py --day DATE --manifest-only`

### Requirement: Anti false-done

Agents SHALL NOT mark a day complete when only `pedagogy_check_unified` passes; `day_contract_check` and `run_day_tests --mode solutions` MUST also pass.

#### Scenario: Day 07 narrow GFX plan

- **WHEN** a plan adds only GFX modules to a tier-A day missing red team / quantum / AI / Node
- **THEN** the agent SHALL expand scope per day-contract or obtain explicit user ACK before closing
