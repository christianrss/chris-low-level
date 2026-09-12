# Pedagogy

Capability: qualidade por módulo (referência executável: `scripts/pedagogy_check_unified.py`).

## Requirements

### Requirement: Theory depth

`TEORIA_PASSO_A_PASSO.md` SHALL have at least 120 substantive lines with diagrams or tables.

For `depth_first` days, fixed line counts SHALL be replaced by semantic
evidence declared in `ASSESSMENT.yaml`: concepts, invariants, one happy
trace, one failure trace, implementation anchors, and linked tests.

### Requirement: Resolution depth

`RESOLUCAO_GUIADA_PASSO_A_PASSO.md` SHALL include `## Baseline`, per-TODO **Onde colocar** blocks, and meet minimum line counts (80 simple / 100 complex modules).

### Requirement: Marker consistency

Every `TODO [ID]` in starter SHALL have matching `PEDAGOGY-TEST: ID` in tests and `PEDAGOGY-SOLUTION: ID` in solutions.

### Requirement: Depth-first authored work

A depth-first project SHALL require substantial authored work rather
than isolated return-value stubs.

#### Scenario: Near-empty starter

- **WHEN** comparing `student_owned` production files in starter and solution
- **THEN** the starter SHALL contain at most 15 percent of the completed logic
- **AND** the expected solution delta SHALL contain at least 250 substantive lines

#### Scenario: End-to-end milestones

- **WHEN** validating `ASSESSMENT.yaml`
- **THEN** it SHALL declare 6–10 ordered milestones
- **AND** at least 10 tested behaviors, 4 failure modes, and one end-to-end behavior
- **AND** every required concept SHALL link to a milestone and a tested behavior

#### Scenario: Tests reject plausible bugs

- **WHEN** validating a depth-first project
- **THEN** its assessment SHALL declare critical mutants
- **AND** the project test suite SHALL reject each declared mutant

### Requirement: Exact starter baseline

Depth-first starter execution SHALL distinguish `PASS`, `FAIL`, `SKIP`
and `NOT RUN`.

#### Scenario: Expected starter failures

- **WHEN** `run_day_tests --mode starter --expect-fail` runs
- **THEN** the observed failing modules SHALL exactly match the assessment
- **AND** an unexpectedly passing starter SHALL fail the gate
- **AND** missing toolchains or skipped tests SHALL fail the gate

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

