# START HERE — Day 2026-09-08

Laboratório unificado: **CLVM toolchain** (disasm C, peephole C++, disasm Rust) + **input mux**, depois trilhas obrigatórias (PE, WASM, AI, parser, Node, graphics FSM, quantum, agent).

## Fluxo por módulo

1. `TEORIA_PASSO_A_PASSO.md` — O quê / Como / Por quê + **trace com números do teste**.
2. Checkpoint em [`ATIVIDADES.md`](ATIVIDADES.md) **antes** do starter.
3. `EXERCICIOS.md` — Fácil → Desafio.
4. Implemente `TODO [ID]` em `starter/`.
5. Testes `PEDAGOGY-TEST: ID` — FAIL até completar.
6. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` só ao travar.
7. Compare `solutions/` após tentativa; preencha benchmark + relatório.

---

## Bloco A — Bytecode (comece aqui)

| # | Módulo | Linguagem | Foco do paper-trace |
|---|--------|-----------|---------------------|
| 1 | `systems/clvm_disassembler` | C | `01 2A 00 00 00` → PUSH 42 |
| 2 | `systems/clvm_peephole_opt` | C++ | fold 2+3 → PUSH 5 |
| 3 | `rust/clvm_disasm` | Rust | mesmos sizes + `Result` |

## Bloco B — Input path

| # | Módulo | Linguagem | Foco |
|---|--------|-----------|------|
| 4 | `linux/input_event_ring_mux` | C | CAP=4; FIFO 10 depois −3 |
| 5 | `nodejs/duplex_event_pipe` | JS | frames de 24 bytes |

## Bloco C — Formatos de arquivo / ABI

| # | Módulo | Linguagem | Foco |
|---|--------|-----------|------|
| 6 | `dotnet/pe_export_span` | .NET | e_lfanew 0x80; RVA 0x1000 |
| 7 | `redteam/pe_export_triage` | Python | mesmos offsets + nomes |
| 8 | `tooling/wasm_section_header` | ASM | `\0asm`; RCX; id 9→0 |

## Bloco D — Numérico / texto / estados

| # | Módulo | Linguagem | Foco |
|---|--------|-----------|------|
| 9 | `ai/softmax_stable` | C | max-subtraction; Σp=1 |
| 10 | `parsers/json_rd_lexer` | C | `{"a":1}` → 5 tokens |
| 11 | `graphics/shader_stage_fsm` | C++ | arestas legais EDIT…READY |
| 12 | `quantum/bell_state_prep` | C++ | H+CNOT; P00=P11=0.5 |
| 13 | `agent/tool_protocol_fsm` | Python | IDLE→…→DONE/ERROR |

---

## Comandos úteis

```powershell
# Gate do dia
python scripts/pedagogy_check_unified.py --day 2026-09-08
python scripts/run_day_tests.py --day 2026-09-08 --mode solutions

# Rust
cd days/2026-09-08/rust/clvm_disasm/starter; cargo test
cd ../solutions; cargo test

# .NET
cd days/2026-09-08/dotnet/pe_export_span/starter; dotnet test

# Node
cd days/2026-09-08/nodejs/duplex_event_pipe/starter; node test.js
```

Sem `cargo`/`dotnet`/`node`, o runner do dia **pula** o módulo (mesmo padrão Dia 06).

**Capstone sugerido:** portar disasm ou PE span para `projects/chris-vm` / `projects/chris-*` após os blocos A–C.

## Trilha paralela GitHub (opcional no mesmo dia)

Depois do core CLVM, ou em sessão separada: `spsc_ring_buffer` → `cache_set_sim` → `nfa_to_dfa` → `bm25_code_ranker`.
Ver bloco correspondente em `ATIVIDADES.md`.

