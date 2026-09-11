# START HERE — 2026-09-11

Ordem sugerida (linguagem + dependência conceitual):

1. `systems/clvm_reloc_apply` — patch u16 `10+5=15`, wrap `FFFF+1→0`.
2. `rust/clvm_reloc_verify` — mesma tabela, só bounds com `Result`.
3. `systems/bump_poison_arena` — poison `0xA5`, canário `0xC3`, used=9.
4. `linux/uevent_kv_parse` — `ACTION=add`, `DEVNAME=sda`.
5. `dotnet/pe_import_span` — import RVA `0x2000` (não o export do dia 08).
6. `tooling/coff_sym_name` — COFF short `main` len 4; long DWORD0=0.
7. `graphics/alpha_blend_scanline` — a=128 → r≈128 (headless).
8. `ai/rms_norm` — `[3,4]` → √12.5.
9. `quantum/phase_kickback` — CZ em `|11>`, H com P=0.5.
10. `parsers/ini_rd_lexer` — `[core]` + `name=`.
11. `nodejs/shared_atomics_ring` — CAP 4, 5º push false.
12. `redteam/import_name_triage` + `agent/tool_barrier_join` — Python.

Cada TEORIA traz o trace idêntico ao assert. Faça no papel antes do código.
