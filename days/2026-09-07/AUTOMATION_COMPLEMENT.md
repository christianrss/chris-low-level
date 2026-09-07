# Treino Low-Level Unificado — complemento diário de 2026-09-07

O `main` já possuía o arco CLVM do próprio dia (`clvm_js_codegen`, `clvm_bytecode_verifier`, `N3_SUBSET_MOD`,
`clvm_v2_strings`). Esta entrega **não recria nem substitui** esses módulos. Ela completa as trilhas permanentes que
ainda faltavam no dia.

## Módulos acrescentados

1. `ai/kv_cache_ring` — AI/ML Systems — KV cache circular e eviction determinístico
2. `redteam/elf_program_header_triage` — Red Team seguro — ELF64 Program Header triage defensivo
3. `dotnet/cil_cfg_verifier` — .NET/CLR — CIL branch CFG e propagação de stack depth
4. `nodejs/libuv_phase_probe` — Node.js/JS Runtime — probes de fases, microtasks e starvation
5. `graphics/resource_state_tracker` — GPU/Graphics — Resource-state tracker Vulkan/D3D12
6. `linux/proc_task_snapshot` — Linux/Unix — /proc task snapshot para base do chris-top
7. `parsers/pratt_query_lang` — Parsers — Pratt parser para query language do smart grep
8. `agent/loop_state_machine` — Coding Agent — harness perceive→plan→act→observe→verify→revise

## Fluxo
Teoria → pesquisa guiada → baseline do starter → TODO em pequenas etapas → teste intermediário → debugging →
benchmark → comparison com solution.

O ZIP é autocontido para estes oito módulos complementares e inclui o DOCX mestre final.
