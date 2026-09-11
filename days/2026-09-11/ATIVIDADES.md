# ATIVIDADES — 2026-09-11 (relocação, ABI, verificação cruzada)

**Dia:** 13 módulos | **~28–36 h**  
**Regra:** não avance de bloco sem o **checkpoint conceitual** (papel). PASS nos testes sozinho não basta.

---

## Preparação (30 min)

- [ ] Ler `START_HERE.md` e `README.md`
- [ ] Baseline:

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-11
```

---

## Bloco 1 — Relocação CLVM (C + Rust) (4–5 h)

### Objetivo conceitual

Entender **site = offset do imediato u16**, não do opcode; validar bounds antes de escrever.

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `systems/clvm_reloc_apply` | CLVM-RELOC-01..04 | `09 0A 00` +5 → `0F`; wrap `FFFF+1→0` |
| `rust/clvm_reloc_verify` | RS-RELOC-01..03 | site 7 com code_len 8 → Err |

**Checkpoint conceitual:**

- [ ] Desenhei JMP com site no índice 1
- [ ] Calculei 10+5=15 e o wrap
- [ ] Expliquei `Result` vs panic OOB

---

## Bloco 2 — ABI / arena / uevent (4–5 h)

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `systems/bump_poison_arena` | SYS-BUMP-01..03 | used=9, canário @8, 66>64 |
| `linux/uevent_kv_parse` | LIN-UEVENT-01..03 | ACTION=add; n=2; DEVNAME=sda |

**Checkpoint:**

- [ ] Poison 0xA5 e canário 0xC3 no papel
- [ ] Sei por que `=x` é rejeitado

---

## Bloco 3 — PE / COFF / import triage (5–6 h)

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `dotnet/pe_import_span` | DOTNET-IMP-01..03 | e_lfanew 0x80; import RVA 0x2000 |
| `tooling/coff_sym_name` | TOOL-COFF-01..03 | `main` len 4; long DWORD0=0 |
| `redteam/import_name_triage` | RT-IMP-01..03 | score 20 para 2 hits |

**Checkpoint:**

- [ ] Diferencio export (dia 08) de import (0x2000)
- [ ] Sei short vs long name COFF

---

## Bloco 4 — Blend, RMS, quantum, INI, ring, agent (8–10 h)

| Módulo | Checkpoint |
|--------|------------|
| `graphics/alpha_blend_scanline` | r≈128 com a=128 |
| `ai/rms_norm` | √12.5 para [3,4] |
| `quantum/phase_kickback` | CZ flip \|11>; P=0.5 após H |
| `parsers/ini_rd_lexer` | tokens core → name → EOF |
| `nodejs/shared_atomics_ring` | 5º push false; pop 10 |
| `agent/tool_barrier_join` | arrive False→True com expected=2 |

**Gate final:**

```powershell
python scripts/run_day_tests.py --day 2026-09-11 --mode solutions
```

---

## Honestidade

- Reloc CLVM é educacional (não ELF completa).
- PE fixture é mínimo (não um binário real).
- GFX é headless (sem janela Win32).

---

## Atividades extras do GitHub (ainda sem pasta `days/` completa)

O remote listava estes temas; **o código portado está em `projects/`**, não como módulos canônicos deste dia. Faça como extensão depois do core.

- [ ] `systems/hazard_pointer_stack` — Hazard pointers
- [ ] `ai/kv_cache_ring` — KV-cache ring
- [ ] `redteam/dwarf_line_program` — DWARF line program
- [ ] `dotnet/jit_callsite_model` — JIT call-site model
- [ ] `nodejs/worker_pool_scheduler` — Worker pool scheduler
- [ ] `parsers/pike_regex_vm` — Pike regex VM
- [ ] `agent/context_budgeter` — Context budgeter
- [ ] `quantum/statevector_bitmask` — Statevector bitmask
- [ ] `network/length_prefixed_framing` — Length-prefixed framing
- [ ] `algorithms/robin_hood_hash` — Robin Hood hash

Portas em `projects/` (ex.: `chris-agent-core/context_budgeter.py`, `chris-binary-toolkit/dwarf_line_subset.py`, `chris-qsim`).

