# VALIDATION_DAY06 — 2026-09-08

## Escopo

- 9 módulos.
- 28 TODOs reais.
- Gate pedagógico: PASS (`day06 pedagogy check passed: 28 TODO mappings`).
- Gate estrutural: PASS (`day06 quality check passed: 9 modules`).

## Execução observada

Solutions executadas com sucesso:
- `systems/spsc_ring_buffer` — CMake/CTest PASS.
- `architecture/cache_set_sim` — CMake/CTest PASS.
- `ai/online_softmax` — Python PASS.
- `redteam/wasm_binary_triage` — Python PASS.
- `parsers/nfa_to_dfa` — Python PASS.
- `agent/bm25_code_ranker` — Python PASS.
- `unix/xargs_lite` — Python PASS.
- `nodejs/worker_transfer` — Node PASS.

Starters correspondentes falharam como esperado nos TODOs planejados.

## Toolchain ausente

- `.NET SDK`: não disponível neste ambiente. O módulo `dotnet/gc_allocation_probe` foi revisado estruturalmente,
  mas não há alegação de execução.

## Benchmarks observados

- online softmax: median_ms=2.8967 min_ms=2.5867 max_ms=5.5271
- BM25: docs=5000 median_ms=3.4547 min_ms=3.0214 max_ms=5.0319

Os números são locais deste ambiente e não são generalizados.

## Segurança

`wasm_binary_triage` usa somente fixture sintético e não executa WebAssembly externo.
`xargs_lite` usa `subprocess.run(..., shell=False)` e teste benigno local.

## DOCX/ZIP

- DOCX mestre: `Treino_LowLevel_Unificado_2026-09-08.docx`.
- Renderização: 34 páginas.
- QA visual: 34/34 páginas inspecionadas; PASS.
- Nenhum clipping, overlap ou glyph quebrado observado.
