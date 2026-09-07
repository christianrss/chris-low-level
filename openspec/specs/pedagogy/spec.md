# Pedagogy

Capability: qualidade por módulo (referência executável: `scripts/pedagogy_check_unified.py`).

## Requirements

### Requirement: Theory depth

`TEORIA_PASSO_A_PASSO.md` SHALL have at least 120 substantive lines with diagrams or tables.

### Requirement: Resolution depth

`RESOLUCAO_GUIADA_PASSO_A_PASSO.md` SHALL include `## Baseline`, per-TODO **Onde colocar** blocks, and meet minimum line counts (80 simple / 100 complex modules).

### Requirement: Marker consistency

Every `TODO [ID]` in starter SHALL have matching `PEDAGOGY-TEST: ID` in tests and `PEDAGOGY-SOLUTION: ID` in solutions.

### Requirement: Anti-padding

The system SHALL reject generated padding such as `Nota pedagógica N` or empty delegation to solutions.

### Requirement: GFX visual solutions

For Win32 graphics modules, `solutions/` executables SHALL render in a window (see `openspec/specs/gfx-visual/spec.md`). Enforced by `check_gfx_visual_solutions()`.

#### Scenario: No MessageBox demo stubs

- **WHEN** a GFX solution `main.cpp` has `wWinMain` but no `StretchDIBits` / `SwapBuffers` / DXGI `Present`
- **THEN** `pedagogy_check` SHALL fail

#### Scenario: Unified checker

- **WHEN** `python scripts/pedagogy_check_unified.py --day DATE` runs
- **THEN** all module-level requirements above SHALL be enforced

