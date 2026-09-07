# ATIVIDADES — 2026-09-07 (CLVM v2 + input + multi-trilha)

**Dia:** 13 módulos | **~32–40 h**  
**Regra:** checkpoint conceitual antes de cada bloco. `pedagogy_check` + `run_day_tests` ao final.

---

## Preparação (30 min)

- [ ] `START_HERE.md`, `README.md`, `TODO_MAP.md`
- [ ] Baseline:

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-07
```

---

## Bloco 1 — CLVM codegen + verifier (6–8 h)

| Módulo | TODOs | Paper-trace obrigatório |
|--------|-------|-------------------------|
| `systems/clvm_js_codegen` | CLVM-JS-* | `let` → STORE; `while` → labels |
| `systems/clvm_bytecode_verifier` | CLVM-VFY-* | stack-effect de `CALL` |
| `systems/clvm_v2_strings` | CLVM-V2-* | pool de strings v2 |

**Checkpoint conceitual:**

- [ ] Desenho stack antes/depois de `CALL`; header v2 com campo strings
- [ ] Explico por que verifier estático ≠ runtime VM

---

## Bloco 2 — Input Linux (4–6 h)

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `linux/hid_keyboard_boot` | HID-KBD-* | report boot 8B → InputEvent |
| `linux/ps2_mouse_input` | PS2-MOUSE-* | pacote 3B → REL_X/REL_Y |

**Checkpoint conceitual:**

- [ ] Hex de um `input_event` de 24 bytes anotado (type/code/value)

---

## Bloco 3 — Rust + .NET (4–6 h)

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `rust/clvm_v2_verify` | CLVM-RS-* | opcode v2 + bounds |
| `dotnet/input_event_span` | DN-INPUT-* | layout evdev + Span |

**Checkpoint conceitual:**

- [ ] Por que `Span` evita cópia no parse HID?

---

## Bloco 4 — Red team + quantum (4–5 h)

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `redteam/hid_report_fuzz` | RT-HID-* | report truncado vs magic 8B |
| `quantum/measurement_born` | Q-MEAS-*, Q-BORN-* | P(|0⟩), P(|1⟩) após H |

**Checkpoint conceitual:**

- [ ] Listei 3 inputs maliciosos para o parser HID
- [ ] Calculei probabilidades de medição em |+⟩ no papel

---

## Bloco 5 — AI + Node + GFX (8–10 h)

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `ai/input_event_entropy` | AI-EVT-* | Shannon em bytes de evento |
| `nodejs/input_event_transform` | ND-INPUT-* | buffer parcial 24B |
| `graphics/artillery_trajectory_2d` | GFX-ART-* | parábola + trail |
| `graphics/raster_depth_parity` | GFX-DEPTH-* | Z-test CPU vs GL |

**Checkpoint conceitual:**

- [ ] Entropia de um stream curto de eventos no papel
- [ ] Trace de `Transform` com chunk de 13 bytes (parcial)
- [ ] Desenhei depth test de dois triângulos sobrepostos

---

## Síntese final

1. O que o verifier estático captura que a VM só veria em runtime?
2. Como HID boot e PS/2 convergem no mesmo `InputEvent`?
3. Por que v2 strings exige novo capstone em vez de patch no Dia 01?
4. Como fuzz de HID se conecta ao driver legítimo do bloco 2?

```powershell
python scripts/run_day_tests.py --day 2026-09-07 --mode solutions
```
