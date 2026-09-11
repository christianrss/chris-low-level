# Validação — 2026-09-08

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-08
python scripts/day_contract_check.py --day 2026-09-08
python scripts/run_day_tests.py --day 2026-09-08 --mode solutions
```

## Módulos core (13)

- `systems/clvm_disassembler` — C
- `systems/clvm_peephole_opt` — C++
- `linux/input_event_ring_mux` — C
- `rust/clvm_disasm` — Rust
- `dotnet/pe_export_span` — .NET
- `graphics/shader_stage_fsm` — C++
- `redteam/pe_export_triage` — Python
- `quantum/bell_state_prep` — C++
- `ai/softmax_stable` — C
- `nodejs/duplex_event_pipe` — JS
- `parsers/json_rd_lexer` — C
- `agent/tool_protocol_fsm` — Python
- `tooling/wasm_section_header` — ASM

## Trilha paralela GitHub (9)

- `systems/spsc_ring_buffer` — C++ (SPSC ring push/pop/size)
- `architecture/cache_set_sim` — C++ (cache set decode/hit/evict)
- `ai/online_softmax` — Python (online softmax stats/normalize)
- `redteam/wasm_binary_triage` — Python (WASM header/ULEB/sections)
- `parsers/nfa_to_dfa` — Python (ε-closure / subset / match)
- `agent/bm25_code_ranker` — Python (BM25 tokenize/index/score)
- `unix/xargs_lite` — Python (split/batch/run)
- `nodejs/worker_transfer` — JS (worker transferables)
- `dotnet/gc_allocation_probe` — .NET (alloc/new/pool probe)

## Notas do remote

Benchmarks observados no remote (online_softmax / BM25) estão em `benchmarks/results-2026-09-08.*`.
`dotnet/gc_allocation_probe` exige .NET SDK (presente nesta máquina).
