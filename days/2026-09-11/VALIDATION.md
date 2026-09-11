# Validação — 2026-09-11

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-11
python scripts/day_contract_check.py --day 2026-09-11
python scripts/run_day_tests.py --day 2026-09-11 --mode solutions
```

| Módulo | Linguagem | Gate |
|--------|-----------|------|
| `systems/clvm_reloc_apply` | C + bytecode | gate |
| `systems/bump_poison_arena` | C++ | gate |
| `linux/uevent_kv_parse` | C | gate |
| `rust/clvm_reloc_verify` | Rust | gate |
| `dotnet/pe_import_span` | C# | gate |
| `graphics/alpha_blend_scanline` | C++ | gate |
| `redteam/import_name_triage` | Python | gate |
| `quantum/phase_kickback` | C++ | gate |
| `ai/rms_norm` | C | gate |
| `nodejs/shared_atomics_ring` | JS | gate |
| `parsers/ini_rd_lexer` | C | gate |
| `agent/tool_barrier_join` | Python | gate |
| `tooling/coff_sym_name` | Assembly | gate |
