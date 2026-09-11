# Proposal: Day 2026-09-11 — Relocação, ABI e verificação cruzada

## Problem

Após os dias 08–10 (decode → telemetry → capstone), falta um dia tier-A que treine **aplicação de relocações**, **limites de ABI/arena** e **verificação cruzada** (C ↔ Rust ↔ .NET ↔ Assembly) com paridade multi-trilha.

## Solution

Criar `days/2026-09-11/` com **13 módulos**, trilhas obrigatórias iguais ao dia 08/10, linguagens misturadas (C, C++, Python, Rust, Assembly, JavaScript, .NET, bytecode).

## Reference day

`days/2026-09-06` (infra) + `days/2026-09-08` (multi-lang) + gold pedagogy `days/2026-09-03/systems/clvm/`.

## Module matrix

| # | Path | Lang |
|---|------|------|
| 1 | systems/clvm_reloc_apply | C + bytecode |
| 2 | systems/bump_poison_arena | C++ |
| 3 | linux/uevent_kv_parse | C |
| 4 | rust/clvm_reloc_verify | Rust |
| 5 | dotnet/pe_import_span | .NET |
| 6 | graphics/alpha_blend_scanline | C++ headless |
| 7 | redteam/import_name_triage | Python |
| 8 | quantum/phase_kickback | C++ |
| 9 | ai/rms_norm | C |
| 10 | nodejs/shared_atomics_ring | JS |
| 11 | parsers/ini_rd_lexer | C |
| 12 | agent/tool_barrier_join | Python |
| 13 | tooling/coff_sym_name | Assembly |

## Success criteria

- `module_count == 13` e tracks em `tracks.yaml`
- `pedagogy_check_unified` + `day_contract_check` + `run_day_tests --mode solutions` PASS
- Pedagogia sem filler lazy; RESOLUCAO com placement + código completo por TODO
