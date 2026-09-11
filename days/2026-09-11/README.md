# Day 2026-09-11 — Relocação, ABI e verificação cruzada

Continua os dias 08–10 (toolchain → telemetria → capstone) com **aplicação de reloc**, **limites de ABI/arena** e **checagens cruzadas** (C ↔ Rust ↔ .NET ↔ Assembly).

| # | Módulo | Linguagem | Fundamento | Horas |
|---|--------|-----------|------------|-------|
| 1 | `systems/clvm_reloc_apply` | **C + bytecode** | patches u16 LE | 2–3 |
| 2 | `systems/bump_poison_arena` | **C++** | poison 0xA5 + canary | 2–3 |
| 3 | `linux/uevent_kv_parse` | **C** | KEY=value uevent | 2–3 |
| 4 | `rust/clvm_reloc_verify` | **Rust** | reloc bounds | 2–3 |
| 5 | `dotnet/pe_import_span` | **C#** | import RVA 0x2000 | 2–3 |
| 6 | `graphics/alpha_blend_scanline` | **C++** | src-over headless | 2–3 |
| 7 | `redteam/import_name_triage` | **Python** | suspicious imports | 2–3 |
| 8 | `quantum/phase_kickback` | **C++** | CZ kickback | 2–3 |
| 9 | `ai/rms_norm` | **C** | RMSNorm [3,4] | 2–3 |
| 10 | `nodejs/shared_atomics_ring` | **JS** | Atomics ring CAP 4 | 2–3 |
| 11 | `parsers/ini_rd_lexer` | **C** | INI section/key | 2–3 |
| 12 | `agent/tool_barrier_join` | **Python** | tool barrier | 2–3 |
| 13 | `tooling/coff_sym_name` | **Assembly** | COFF name field | 2–3 |

**Total:** ~28–36 h.

## Como estudar

1. [`START_HERE.md`](START_HERE.md)
2. [`ATIVIDADES.md`](ATIVIDADES.md)
3. Por módulo: TEORIA → EXERCICIOS → starter → TESTES → RESOLUCAO

## Validação

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-11
python scripts/day_contract_check.py --day 2026-09-11
python scripts/run_day_tests.py --day 2026-09-11 --mode solutions
```
