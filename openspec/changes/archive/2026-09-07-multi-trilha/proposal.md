# Proposal: Day 07 multi-trilha correction

## Problem

Day 2026-09-07 was built with narrow plans (CLVM + GFX) while user expectation was **full multi-trilha** parity with Day 06 (~13 modules, 7 trilhas).

`pedagogy_check_unified` passed per-module quality but did not validate day-level scope.

## Solution

Add four modules (N11–N14): red team, quantum, AI, Node.js. Sync infra. Introduce `day_contract_check` and OpenSpec governance.

## Reference day

`2026-09-06` — compression multi-trilha baseline.

## Success criteria

- 13 modules, 45 TODOs
- All tier-A tracks present per `tracks.yaml`
- README / ATIVIDADES / MANIFEST.modules aligned
- LEARNING_PATHS + module_project_map updated
