# Day 2026-09-08 — CLVM toolchain + trilha GitHub (cache/SPSC/BM25)

**22 módulos:** 13 core multilíngue (CLVM/PE/ASM) + 9 da trilha paralela trazida do GitHub.

## Core (ordem cognitiva)

| # | Módulo | Linguagem | Fundamento | Horas |
|---|--------|-----------|------------|-------|
| 1 | `systems/clvm_disassembler` | **C** | PUSH/JMP sizes | 2–3 |
| 2 | `systems/clvm_peephole_opt` | **C++** | peephole fold | 2–3 |
| 3 | `linux/input_event_ring_mux` | **C** | ring CAP4 | 2–3 |
| 4 | `rust/clvm_disasm` | **Rust** | ISA Result | 2–3 |
| 5 | `dotnet/pe_export_span` | **.NET** | e_lfanew/export | 2–3 |
| 6 | `graphics/shader_stage_fsm` | **C++** | shader FSM | 2–3 |
| 7 | `redteam/pe_export_triage` | **Python** | MZ triage | 2–3 |
| 8 | `quantum/bell_state_prep` | **C++** | Bell P=0.5 | 2–3 |
| 9 | `ai/softmax_stable` | **C** | stable softmax | 2–3 |
| 10 | `nodejs/duplex_event_pipe` | **JS** | 24B framing | 2–3 |
| 11 | `parsers/json_rd_lexer` | **C** | JSON lexer | 2–3 |
| 12 | `agent/tool_protocol_fsm` | **Python** | tool FSM | 2–3 |
| 13 | `tooling/wasm_section_header` | **ASM** | WASM magic | 2–3 |

## Trilha paralela GitHub

| # | Módulo | Linguagem | Fundamento | Horas |
|---|--------|-----------|------------|-------|
| 14 | `systems/spsc_ring_buffer` | **C++** | SPSC ring push/pop/size | 2–3 |
| 15 | `architecture/cache_set_sim` | **C++** | cache set decode/hit/evict | 2–3 |
| 16 | `ai/online_softmax` | **Python** | online softmax stats/normalize | 2–3 |
| 17 | `redteam/wasm_binary_triage` | **Python** | WASM header/ULEB/sections | 2–3 |
| 18 | `parsers/nfa_to_dfa` | **Python** | ε-closure / subset / match | 2–3 |
| 19 | `agent/bm25_code_ranker` | **Python** | BM25 tokenize/index/score | 2–3 |
| 20 | `unix/xargs_lite` | **Python** | split/batch/run | 2–3 |
| 21 | `nodejs/worker_transfer` | **JS** | worker transferables | 2–3 |
| 22 | `dotnet/gc_allocation_probe` | **.NET** | alloc/new/pool probe | 2–3 |

**Total:** ~40–50 h (pode fatiar core num dia e trilha A no seguinte).

C/C++/ASM: Visual Studio 18 2026 via `run_day_tests.py` (Ninja + cl).
