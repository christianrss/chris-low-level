# Learning paths

Capability: trilhas verticais multi-dia em `docs/LEARNING_PATHS.md`.

## Requirements

### Requirement: Vertical continuity

New modules SHALL extend an existing learning path section or add a new numbered section with mermaid flow and module table.

### Requirement: Capstone linkage

Each tier-A module SHALL map to a `projects/chris-*` entry in `scripts/module_project_map.py`.

#### Scenario: Day 07 HID fuzz

- **WHEN** `redteam/hid_report_fuzz` is added
- **THEN** `LEARNING_PATHS.md` §2 SHALL reference the module
- **AND** `module_project_map.py` SHALL map it to `projects/chris-binary-toolkit`

### Requirement: Cross-day references

Learning path entries SHALL use paths `YYYY-MM-DD/<trilha>/<modulo>` consistent with `days/` layout.
