# START HERE — Day 2026-09-07

Dia **multi-trilha completo**: CLVM v2, drivers Linux, Rust/.NET, red team, quantum, AI, Node.js e GFX — sem alterar starters CLVM v1 já resolvidos (Dias 01/04).

## Fluxo por módulo

1. `TEORIA_PASSO_A_PASSO.md` — trace no papel antes do código.
2. Checkpoint em [`ATIVIDADES.md`](ATIVIDADES.md).
3. `EXERCICIOS.md` → implemente `starter/` (`TODO [ID]`).
4. Testes (`PEDAGOGY-TEST: ID`); esperado FAIL até completar.
5. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` só ao travar (inclui `## Baseline`).
6. Compare `solutions/` após tentativa; `BENCHMARK_GUIADO.md` → **Resultados observados**.

## Ordem sugerida (N0–N14)

| Bloco | Módulos |
|-------|---------|
| Manhã CLVM | N0 capstone → `clvm_js_codegen` → `clvm_bytecode_verifier` → N3 subset → `clvm_v2_strings` |
| Tarde drivers | `hid_keyboard_boot` → `ps2_mouse_input` |
| Noite Rust/.NET | `clvm_v2_verify` → `input_event_span` |
| Red team + quantum | `hid_report_fuzz` → `measurement_born` |
| AI + Node | `input_event_entropy` → `input_event_transform` |
| GFX | `artillery_trajectory_2d` → `raster_depth_parity` |

Mapa: `TODO_MAP.md`. Trilhas: `docs/LEARNING_PATHS.md` §2, §3a, §5, §8–§10.

## Validação

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-07
python scripts/run_day_tests.py --day 2026-09-07 --mode solutions
```

Veja `VALIDATION.md` para skips (.NET SDK, kernel, Node).
