# Day 2026-09-08 — CLVM toolchain + input, linguagens misturadas

Não é um dia só em Python. Cada módulo tem uma linguagem e um contrato numérico.

| # | Módulo | Linguagem | Fundamento | Horas |
|---|--------|-----------|------------|-------|
| 1 | `systems/clvm_disassembler` | **C + bytecode** `.clbc` | PUSH 5 / JMP 3 | 3 |
| 2 | `systems/clvm_peephole_opt` | **C++** bytecode | PUSH 0+ADD, fold 2+3 | 2–3 |
| 3 | `linux/input_event_ring_mux` | **C** | anel CAP 4, FIFO | 2–3 |
| 4 | `rust/clvm_disasm` | **Rust** | mesma ISA, `Result` | 2 |
| 5 | `dotnet/pe_export_span` | **.NET** | e_lfanew 0x80, RVA 0x1000 | 2–3 |
| 6 | `graphics/shader_stage_fsm` | **C++** | EDIT não vai a READY | 2 |
| 7 | `redteam/pe_export_triage` | **Python** | evidência MZ | 2 |
| 8 | `quantum/bell_state_prep` | **C++** | H + CNOT, P=0.5 | 2–3 |
| 9 | `ai/softmax_stable` | **C** | max=3 em {1,2,3} | 2 |
| 10 | `nodejs/duplex_event_pipe` | **JavaScript** | 24×2=48 | 2 |
| 11 | `parsers/json_rd_lexer` | **C** | 5 tokens em `{"a":1}` | 2–3 |
| 12 | `agent/tool_protocol_fsm` | **Python** | FSM de tool call | 2 |
| 13 | `tooling/wasm_section_header` | **Assembly** | magic `\0asm`, RCX | 2–3 |

**Total:** ~30–36 h.

C, C++ e Assembly usam o gerador **Visual Studio 18 2026** (`-A x64`). O runner passa `CMAKE_GENERATOR_INSTANCE` a partir do `vswhere`, porque o CMake sozinho não enxerga o VS 2026.
