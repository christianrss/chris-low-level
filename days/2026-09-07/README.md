# Day 2026-09-07 — CLVM v2, input, multi-trilha

Dia completo (paridade com Dia 06): **CLVM v2 + drivers Linux + Rust/.NET + red team + quantum + AI + Node.js + gráficos** — sem alterar starters CLVM v1 dos Dias 01/04.

## Módulos (13) — ordem cognitiva

| # | Módulo | Fundamento a internalizar | Horas |
|---|--------|---------------------------|-------|
| N1 | `systems/clvm_js_codegen` | codegen LET/WHILE/CALL | 2–3 |
| N2 | `systems/clvm_bytecode_verifier` | stack-effect + branch bounds | 2–3 |
| N4 | `systems/clvm_v2_strings` | FORMAT v2 + PRINTS | 2–3 |
| N5 | `linux/hid_keyboard_boot` | HID boot → InputEvent → read() | 2–3 |
| N6 | `linux/ps2_mouse_input` | PS/2 mouse → eventos relativos | 2–3 |
| N7 | `rust/clvm_v2_verify` | parser/verifier CLVM v2 em Rust | 2–3 |
| N8 | `dotnet/input_event_span` | evdev layout + Span HID/PS2 | 2–3 |
| N9 | `graphics/artillery_trajectory_2d` | artilharia 2D CPU+GL+D3D11 | 3–4 |
| N10 | `graphics/raster_depth_parity` | Z-buffer CPU + paridade GL | 2–3 |
| N11 | `redteam/hid_report_fuzz` | fuzz HID malformado (parser N5) | 2 |
| N12 | `quantum/measurement_born` | medição, colapso, regra de Born | 2–3 |
| N13 | `ai/input_event_entropy` | entropia/RLE em stream InputEvent | 2 |
| N14 | `nodejs/input_event_transform` | Transform 24B + backpressure | 2 |

**Pré-estudo:** N0 `projects/chris-vm/docs/STUDY_CHECKLIST_N0.md` + N3 `systems/N3_SUBSET_MOD.md` (subset `%` ainda v1).

**Total:** ~32–40 h.

## Ordem sugerida por blocos

| Bloco | Módulos |
|-------|---------|
| Manhã CLVM | N0 → N1 → N2 → N3 → N4 |
| Tarde drivers | N5 → N6 |
| Noite Rust/.NET | N7 (após N2+N4) → N8 (após N5+N6) |
| Red team + quantum | N11 (após N5) → N12 (após Day 04 `statevector_intro`) |
| AI + Node input | N13 (após N8) → N14 (após Day 06 `gunzip_transform`) |
| GFX extra | N9 → N10 (após revisar Dia 01 `dual_backend_3d`) |

Mapa global: `TODO_MAP.md`. Trilhas: `docs/LEARNING_PATHS.md` §2, §3a, §5, §8–§10.

## Capstones

- [`projects/chris-vm/`](../../projects/chris-vm/) — ISA + js2clvm + v2 experimental
- [`projects/chris-driver-lab/`](../../projects/chris-driver-lab/) — fila de input
- [`projects/chris-binary-toolkit/`](../../projects/chris-binary-toolkit/) — triage + HID fuzz
- [`projects/chris-qsim/`](../../projects/chris-qsim/) — statevector + medição
- [`projects/chris-artillery-2d/`](../../projects/chris-artillery-2d/) — física 2D triple backend

## Como estudar

1. [`START_HERE.md`](START_HERE.md)
2. [`ATIVIDADES.md`](ATIVIDADES.md) — checkpoints conceituais antes de cada bloco
3. Por módulo: TEORIA → EXERCICIOS → starter → TESTES → RESOLUCAO (se travar)

## Validação

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-07
python scripts/run_day_tests.py --day 2026-09-07 --mode solutions
```

## Perguntas de síntese

1. Por que codegen, verifier e strings v2 são módulos separados do Dia 01?
2. Como um evento HID e um pacote PS/2 chegam ao mesmo layout em .NET?
3. O que um relatório HID malformado pode fazer que o parser legítimo não antevê?
4. Como a regra de Born conecta amplitudes do Day 04 à medição projetiva?
