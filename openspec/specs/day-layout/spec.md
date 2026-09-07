# Day layout

Capability: estrutura canônica de um dia de laboratório.

## Requirements

### Requirement: Day folder structure

The repository SHALL place each learning day under `days/YYYY-MM-DD/` with taxonomia `<trilha>/<modulo>/` (not `modules/NN_`).

#### Scenario: Required day-level files

- **WHEN** a day is published for study
- **THEN** the day folder SHALL contain `README.md`, `START_HERE.md`, `ATIVIDADES.md`, `TODO_MAP.md`, `VALIDATION.md`, and `MANIFEST.json`

### Requirement: Module package

Each module folder SHALL contain eight pedagogical Markdown files plus `starter/` and `solutions/`.

#### Scenario: Module artifacts

- **WHEN** a module is listed in the day's module count
- **THEN** it SHALL include `README.md`, `TEORIA_PASSO_A_PASSO.md`, `PESQUISA_GUIADA.md`, `EXERCICIOS.md`, `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`, `TESTES_GUIADOS.md`, `BENCHMARK_GUIADO.md`, `starter/`, and `solutions/`

### Requirement: Optional day contract override

A day MAY define `days/YYYY-MM-DD/day.contract.yaml` to override tier rules from `openspec/specs/day-contract/tracks.yaml`.
