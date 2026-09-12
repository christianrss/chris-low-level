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

### Requirement: Depth-first future days

Days on or after the configured `depth_first_from` date SHALL use the
`depth_first` profile unless an explicit contract selects another
profile.

#### Scenario: One substantial project

- **WHEN** a future day uses `profile: depth_first`
- **THEN** it SHALL contain exactly one project module
- **AND** declare 6–8 planned hours
- **AND** reference one curriculum cycle and one primary lane
- **AND** include `ASSESSMENT.yaml` and `RUBRIC.md`

#### Scenario: Legacy days remain stable

- **WHEN** checking a day dated on or before `2026-09-11`
- **THEN** its existing tier-A or tier-B behavior SHALL remain unchanged
- **AND** depth-first requirements SHALL NOT be applied implicitly

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

### Requirement: Cycle coverage

Depth-first breadth SHALL be measured across a declared cycle of 7–10
days instead of requiring every track on every day.

#### Scenario: Planned cycle

- **WHEN** a cycle has status `planned` or `active`
- **THEN** its schedule SHALL contain 7–10 unique dates
- **AND** cover every `required_lane`
- **AND** every scheduled day SHALL have exactly one primary lane

#### Scenario: Completed cycle

- **WHEN** a cycle has status `complete`
- **THEN** every scheduled day SHALL exist
- **AND** each day contract SHALL reference that cycle and matching lane
- **AND** every project SHALL be wired to a learning path or portfolio project

### Requirement: Anti false-done

Agents SHALL NOT mark a day complete when only `pedagogy_check_unified` passes; `day_contract_check` and `run_day_tests --mode solutions` MUST also pass.

#### Scenario: Day 07 narrow GFX plan

- **WHEN** a plan adds only GFX modules to a tier-A day missing red team / quantum / AI / Node
- **THEN** the agent SHALL expand scope per day-contract or obtain explicit user ACK before closing
