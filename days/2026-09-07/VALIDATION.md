# VALIDATION — Day 2026-09-07

## Gates

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-07
python scripts/run_day_tests.py --day 2026-09-07 --mode solutions
python scripts/run_day_tests.py --day 2026-09-07 --mode starter --expect-fail
```

## Expectativas

| Gate | Esperado |
|------|----------|
| pedagogy_check | **PASS** — 13 módulos, 45 TODOs |
| solutions | PASS (ctest / cargo test / dotnet test / pytest / node) |
| starter | FAIL até TODOs |
| GFX | `docs/COMPARISON.md` + VISUAL-01 nos módulos `graphics/*`; **smoke visual Windows** (opcional CI): `artillery_sw`, `artillery_gl`, `artillery_d3d`, `depth_sw`, `depth_gl` abrem janela com pixels |
| Anti-padding | zero `Nota pedagógica` gerada |

## Módulos

| Trilha | Módulo | Runner |
|--------|--------|--------|
| CLVM | clvm_js_codegen, clvm_bytecode_verifier, clvm_v2_strings | ctest + python |
| Linux | hid_keyboard_boot, ps2_mouse_input | ctest |
| Rust | clvm_v2_verify | cargo test |
| .NET | input_event_span | dotnet test |
| Red team | hid_report_fuzz | pytest |
| Quantum | measurement_born | ctest |
| AI | input_event_entropy | pytest |
| Node.js | input_event_transform | node test.js |
| GFX N9 | artillery_trajectory_2d | ctest (+ Win32 demos opcionais) |
| GFX N10 | raster_depth_parity | ctest (+ depth_gl opcional) |

## Skip matrix

| Módulo | Skip se |
|--------|---------|
| dotnet/input_event_span | sem .NET SDK 8 |
| linux/* | sem CMake/MSVC ou GCC |
| nodejs/input_event_transform | sem Node 18+ |
| graphics/* Win32 demos | não-Windows |

## Auditoria anti-padding

```powershell
rg "Nota pedagógica \d" days/2026-09-07
```

Deve retornar vazio.
