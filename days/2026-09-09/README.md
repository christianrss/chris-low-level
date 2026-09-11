# Day 09 — 2026-09-09

**Observabilidade multi-linguagem** — C/C++ no núcleo; Rust, .NET, JavaScript e Python nas demais trilhas.

## Módulos (13) — ordem cognitiva

| # | Módulo | Linguagem | Trace / contrato |
|---|--------|-----------|------------------|
| 1 | `systems/clvm_trace_profiler` | **C** | `02 02 08` → hottest `0x02` |
| 2 | `systems/arena_telemetry` | **C++** | alloc 8 ok; +60 falha; reset mantém allocs |
| 3 | `ai/attention_mask` | **C** | q=2; k=3 → −1e9; visible_count=3 |
| 4 | `rust/stack_sample_trace` | **Rust** | `0x1000` → `main` |
| 5 | `dotnet/activity_source_span` | **.NET** | `work\|activity_source_span` |
| 6 | `nodejs/async_hooks_trace` | **JavaScript** | phase `init`; metrics |
| 7 | `linux/perf_event_open_lab` | **Python** | open/read/close + fd sintético |
| 8 | `graphics/gpu_timer_query` | **Python** | handle 0; lap `draw` |
| 9 | `parsers/logfmt_lexer` | **Python** | `a=1 b=2` → 2 tokens |
| 10 | `quantum/decoherence_noise` | **Python** | p0+p1≈1; len(trace)=4 |
| 11 | `redteam/yara_match_scan` | **Python** | `AA ??` → hit @1 |
| 12 | `agent/verify_replay_log` | **Python** | FSM → DONE; hash 16 |
| 13 | `tooling/pdb_symbol_index` | **Python** | `1000 main` → lookup |

**Total:** ~24–32 h. Comece por `START_HERE.md` e os checkpoints de `ATIVIDADES.md`.

## Capstones relacionados

- [`projects/chris-vm/`](../../projects/chris-vm/) — bytecode / verify
- [`projects/chris-agent-harness/`](../../projects/chris-agent-harness/) — replay / agent

## Validação

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-09
python scripts/day_contract_check.py --day 2026-09-09
python scripts/run_day_tests.py --day 2026-09-09 --mode solutions
```
