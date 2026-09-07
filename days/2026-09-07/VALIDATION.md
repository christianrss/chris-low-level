# VALIDATION — Day 2026-09-07

## Gates

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-07
python scripts/day_contract_check.py --day 2026-09-07
python scripts/run_day_tests.py --day 2026-09-07 --mode solutions
python scripts/run_day_tests.py --day 2026-09-07 --mode starter --expect-fail
```

## Expectativas

| Gate | Esperado |
|------|----------|
| pedagogy_check | **PASS** — 21 módulos, 69 TODOs |
| day_contract | **PASS** — tier-A, tracks incl. parsers + agent |
| solutions | 21/21 PASS |
| starter | FAIL até TODOs |
| GFX visual | `artillery_*`, `depth_*` com janela; `resource_state_tracker` headless (exempt) |
| Benchmarks | [`benchmarks/results-2026-09-07.json`](../../benchmarks/results-2026-09-07.json) |

## Módulos (21)

| Trilha | Módulo | Runner |
|--------|--------|--------|
| CLVM | clvm_js_codegen, clvm_bytecode_verifier, clvm_v2_strings | ctest + python |
| Linux | hid_keyboard_boot, ps2_mouse_input, proc_task_snapshot | ctest / pytest |
| Rust | clvm_v2_verify | cargo test |
| .NET | input_event_span, cil_cfg_verifier | dotnet test |
| Red team | hid_report_fuzz, elf_program_header_triage | pytest |
| Quantum | measurement_born | ctest |
| AI | input_event_entropy, kv_cache_ring | pytest |
| Node.js | input_event_transform, libuv_phase_probe | node test.js |
| GFX | artillery_trajectory_2d, raster_depth_parity, resource_state_tracker | ctest |
| Parsers | pratt_query_lang | pytest |
| Agent | loop_state_machine | pytest |

## Skip matrix

| Módulo | Skip se |
|--------|---------|
| dotnet/* | sem .NET SDK 8 |
| linux/hid*, ps2* | sem CMake/MSVC ou GCC |
| graphics/artillery*, raster_depth* Win32 | não-Windows |
| nodejs/* | sem Node 18+ |

## Complemento automatizado

Ver [`AUTOMATION_COMPLEMENT.md`](AUTOMATION_COMPLEMENT.md). Integrado sem remover núcleo multi-trilha (13 módulos originais).
