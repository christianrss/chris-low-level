# START HERE — Day 2026-09-07

Dia **tier-A (21 módulos)**: núcleo CLVM v2 + input multi-trilha + **complemento** de trilhas permanentes (ver [`AUTOMATION_COMPLEMENT.md`](AUTOMATION_COMPLEMENT.md)).

## Fluxo por módulo

1. `TEORIA_PASSO_A_PASSO.md` — trace no papel antes do código.
2. Checkpoint em [`ATIVIDADES.md`](ATIVIDADES.md).
3. `EXERCICIOS.md` → implemente `starter/` (`TODO [ID]`).
4. Testes (`PEDAGOGY-TEST: ID`); esperado FAIL até completar.
5. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` só ao travar (inclui `## Baseline`).
6. Compare `solutions/` após tentativa; `BENCHMARK_GUIADO.md` → **Resultados observados**.

## Ordem sugerida

| Bloco | Módulos |
|-------|---------|
| Manhã CLVM | N0 capstone → `clvm_js_codegen` → `clvm_bytecode_verifier` → N3 → `clvm_v2_strings` |
| Tarde drivers | `hid_keyboard_boot` → `ps2_mouse_input` → `proc_task_snapshot` |
| Noite Rust/.NET | `clvm_v2_verify` → `input_event_span` → `cil_cfg_verifier` |
| Red team + quantum | `hid_report_fuzz` → `elf_program_header_triage` → `measurement_born` |
| AI + Node | `input_event_entropy` → `kv_cache_ring` → `input_event_transform` → `libuv_phase_probe` |
| GFX | `artillery_trajectory_2d` → `raster_depth_parity` → `resource_state_tracker` |
| Parsers + agent | `pratt_query_lang` → `loop_state_machine` |

Mapa: `TODO_MAP.md` (69 TODOs). Trilhas: `docs/LEARNING_PATHS.md`.

## Validação

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-07
python scripts/day_contract_check.py --day 2026-09-07
python scripts/run_day_tests.py --day 2026-09-07 --mode solutions
```

Veja `VALIDATION.md` para skips (.NET SDK, kernel, Node) e benchmarks.
