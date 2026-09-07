# ATIVIDADES — 2026-09-07 (21 módulos)

**Dia:** 13 núcleo + 8 complemento | **~52–60 h**  
**Regra:** checkpoint conceitual antes de cada bloco. Gates ao final.

---

## Preparação (30 min)

- [ ] `START_HERE.md`, `README.md`, `AUTOMATION_COMPLEMENT.md`, `TODO_MAP.md`
- [ ] Baseline:

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-07
```

---

## Bloco 1 — CLVM (6–8 h)

| Módulo | TODOs |
|--------|-------|
| `systems/clvm_js_codegen` | CLVM-JS-* |
| `systems/clvm_bytecode_verifier` | CLVM-VFY-* |
| `systems/clvm_v2_strings` | CLVM-V2-* |

**Checkpoint:** stack-effect de `CALL`; header v2 com pool de strings.

---

## Bloco 2 — Input Linux (4–6 h)

| Módulo | TODOs |
|--------|-------|
| `linux/hid_keyboard_boot` | HID-KBD-* |
| `linux/ps2_mouse_input` | PS2-MOUSE-* |
| `linux/proc_task_snapshot` | D5-PROC-* |

**Checkpoint:** hex de `input_event` 24B; parse de uma linha `/proc/pid/stat`.

---

## Bloco 3 — Rust + .NET (5–7 h)

| Módulo | TODOs |
|--------|-------|
| `rust/clvm_v2_verify` | CLVM-RS-* |
| `dotnet/input_event_span` | DN-INPUT-* |
| `dotnet/cil_cfg_verifier` | D5-CIL-* |

**Checkpoint:** por que `Span` evita cópia; merge de stack depth em join de CFG.

---

## Bloco 4 — Red team + quantum (5–6 h)

| Módulo | TODOs |
|--------|-------|
| `redteam/hid_report_fuzz` | RT-HID-* |
| `redteam/elf_program_header_triage` | D5-ELF-* |
| `quantum/measurement_born` | Q-MEAS-*, Q-BORN-* |

**Checkpoint:** 3 inputs maliciosos HID; P(|0⟩) após H no papel; offsets PHDR em fixture sintético.

---

## Bloco 5 — AI + Node (6–8 h)

| Módulo | TODOs |
|--------|-------|
| `ai/input_event_entropy` | AI-EVT-* |
| `ai/kv_cache_ring` | D5-KV-* |
| `nodejs/input_event_transform` | ND-INPUT-* |
| `nodejs/libuv_phase_probe` | D5-NODE-* |

**Checkpoint:** entropia de stream curto; ordem nextTick vs promise vs immediate.

---

## Bloco 6 — GFX (6–8 h)

| Módulo | TODOs |
|--------|-------|
| `graphics/artillery_trajectory_2d` | GFX-ART-* |
| `graphics/raster_depth_parity` | GFX-DEPTH-* |
| `graphics/resource_state_tracker` | D5-GFX-* |

**Checkpoint:** depth test CPU vs GL; smoke `artillery_sw.exe`; barrier batch do state tracker.

---

## Bloco 7 — Parsers + agent (4 h)

| Módulo | TODOs |
|--------|-------|
| `parsers/pratt_query_lang` | D5-PRATT-* |
| `agent/loop_state_machine` | D5-AGENT-* |

**Checkpoint:** AST de `foo AND bar:baz`; trace FSM até DONE com retry.

---

## Síntese final

```powershell
python scripts/run_day_tests.py --day 2026-09-07 --mode solutions
```

Benchmarks observados: [`benchmarks/results-2026-09-07.json`](../../benchmarks/results-2026-09-07.json).
