# START HERE — Day 2026-09-09

**Observabilidade multi-linguagem** — C/C++ no núcleo; Rust, .NET, JavaScript e Python nas demais trilhas.

## Fluxo por módulo (igual Dia 01 / 06)

1. Leia `TEORIA_PASSO_A_PASSO.md` — O quê / Como / Por quê + **trace no papel**.
2. Faça o checkpoint de [`ATIVIDADES.md`](ATIVIDADES.md) **antes** do starter.
3. `EXERCICIOS.md` — Fácil → Desafio.
4. Implemente `starter/` (`TODO [ID]`).
5. Rode testes (`PEDAGOGY-TEST: ID`). Esperado: FAIL até completar.
6. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` só ao travar.
7. Compare `solutions/` após tentativa honesta; registre `BENCHMARK_GUIADO.md`.

## Ordem recomendada

1. `systems/clvm_trace_profiler` (C) — histograma `02 02 08`
2. `systems/arena_telemetry` (C++) — allocs sobrevivem ao reset
3. `ai/attention_mask` (C) — máscara causal
4. `rust/stack_sample_trace` — PC → main
5. `dotnet/activity_source_span` — Activity + tag
6. `nodejs/async_hooks_trace` — fases init/before/after
7. `linux/perf_event_open_lab` — fd sintético
8. `graphics/gpu_timer_query` — timer headless
9. `parsers/logfmt_lexer` — k=v
10. `quantum/decoherence_noise` — canal + trace
11. `redteam/yara_match_scan` — AA ??
12. `agent/verify_replay_log` — FSM + hash
13. `tooling/pdb_symbol_index` — 1000 main

## Gates

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-09
python scripts/day_contract_check.py --day 2026-09-09
python scripts/run_day_tests.py --day 2026-09-09 --mode solutions
```

## Ordem cognitiva (não pule)

1. Leia o `README.md` do dia e marque as linguagens de cada módulo.
2. Abra `ATIVIDADES.md` e faça o checkpoint do Bloco 1 **no papel**.
3. Só então entre em `TEORIA_PASSO_A_PASSO.md` do primeiro módulo.
4. Implemente TODOs na ordem do mapa da RESOLUCAO; não leia `solutions/` antes.
5. Feche o bloco com o teste e volte ao checkpoint do próximo bloco.

## Comandos de validação

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-09
python scripts/run_day_tests.py --day 2026-09-09 --mode solutions
```

## Se travar

Use a seção **Onde colocar** da RESOLUCAO (arquivo + função + substituir). Se a seção não nomear o arquivo, o artefato está incompleto — reporte; não invente outro path.

