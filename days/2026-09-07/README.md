# Day 2026-09-07 — CLVM v2, input, multi-trilha + complemento

Dia **tier-A completo** (21 módulos): arco CLVM v2 + drivers Linux + Rust/.NET + red team + quantum + AI + Node.js + gráficos **e** complemento de trilhas permanentes (KV cache, ELF PHDR, CIL CFG, libuv, GPU states, `/proc`, Pratt parser, agent FSM) — sem alterar starters CLVM v1 dos Dias 01/04.

## Núcleo (13 módulos) — ordem cognitiva

| # | Módulo | Fundamento | Horas |
|---|--------|------------|-------|
| N1 | `systems/clvm_js_codegen` | codegen LET/WHILE/CALL | 2–3 |
| N2 | `systems/clvm_bytecode_verifier` | stack-effect + branch bounds | 2–3 |
| N4 | `systems/clvm_v2_strings` | FORMAT v2 + PRINTS | 2–3 |
| N5 | `linux/hid_keyboard_boot` | HID boot → InputEvent | 2–3 |
| N6 | `linux/ps2_mouse_input` | PS/2 → eventos relativos | 2–3 |
| N7 | `rust/clvm_v2_verify` | parser/verifier CLVM v2 Rust | 2–3 |
| N8 | `dotnet/input_event_span` | evdev + Span HID/PS2 | 2–3 |
| N9 | `graphics/artillery_trajectory_2d` | artilharia 2D CPU+GL+D3D11 | 3–4 |
| N10 | `graphics/raster_depth_parity` | Z-buffer CPU + paridade GL | 2–3 |
| N11 | `redteam/hid_report_fuzz` | fuzz HID malformado | 2 |
| N12 | `quantum/measurement_born` | medição + regra de Born | 2–3 |
| N13 | `ai/input_event_entropy` | entropia/RLE em InputEvent | 2 |
| N14 | `nodejs/input_event_transform` | Transform 24B + backpressure | 2 |

## Complemento (8 módulos) — trilhas permanentes

| # | Módulo | Fundamento | Horas |
|---|--------|------------|-------|
| C1 | `ai/kv_cache_ring` | KV cache circular + eviction | 2 |
| C2 | `redteam/elf_program_header_triage` | ELF64 Program Header triage | 2 |
| C3 | `dotnet/cil_cfg_verifier` | CFG CIL + stack depth | 2–3 |
| C4 | `nodejs/libuv_phase_probe` | fases libuv / nextTick / yield | 2 |
| C5 | `graphics/resource_state_tracker` | state tracker GPU (headless) | 2 |
| C6 | `linux/proc_task_snapshot` | `/proc/<pid>/stat` snapshot | 2 |
| C7 | `parsers/pratt_query_lang` | Pratt parser query language | 2 |
| C8 | `agent/loop_state_machine` | FSM perceive→verify→replay | 2 |

**Pré-estudo:** N0 `projects/chris-vm/docs/STUDY_CHECKLIST_N0.md` + N3 `systems/N3_SUBSET_MOD.md`.

**Total:** ~52–60 h.

Detalhes do complemento automatizado: [`AUTOMATION_COMPLEMENT.md`](AUTOMATION_COMPLEMENT.md).

## Ordem sugerida

| Bloco | Módulos |
|-------|---------|
| Manhã CLVM | N0 → N1 → N2 → N3 → N4 |
| Tarde drivers | N5 → N6 → C6 |
| Noite Rust/.NET | N7 → N8 → C3 |
| Red team + quantum | N11 → C2 → N12 |
| AI + Node | N13 → C1 → N14 → C4 |
| GFX | N9 → N10 → C5 |
| Parsers + agent | C7 → C8 |

Mapa: `TODO_MAP.md`. Trilhas: `docs/LEARNING_PATHS.md` §2, §3a, §5, §8–§12.

## Capstones

- [`projects/chris-vm/`](../../projects/chris-vm/) — ISA + js2clvm + v2
- [`projects/chris-driver-lab/`](../../projects/chris-driver-lab/) — fila de input
- [`projects/chris-binary-toolkit/`](../../projects/chris-binary-toolkit/) — triage ELF + HID fuzz
- [`projects/chris-top/`](../../projects/chris-top/) — proc snapshot (C6)
- [`projects/chris-qsim/`](../../projects/chris-qsim/) — medição quântica
- [`projects/chris-artillery-2d/`](../../projects/chris-artillery-2d/) — física 2D triple backend

## Validação

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-07
python scripts/day_contract_check.py --day 2026-09-07
python scripts/run_day_tests.py --day 2026-09-07 --mode solutions
```

Ver [`VALIDATION.md`](VALIDATION.md) — benchmarks em [`benchmarks/results-2026-09-07.json`](../../benchmarks/results-2026-09-07.json).
