# START HERE — Day 2026-09-05

Laboratório unificado de low-level. O estudo é **modular**: cada pasta `<trilha>/<modulo>/` contém teoria, exercícios, resolução guiada e código.

## Fluxo por módulo

1. Leia `README.md` e `TEORIA_PASSO_A_PASSO.md` (≥120 linhas, diagramas, O quê/Como/Por quê).
2. Abra `EXERCICIOS.md` — quatro níveis: Fácil → Médio → Difícil → Desafio.
3. Implemente no `starter/` seguindo os `TODO [ID]` (veja `TODO_MAP.md`).
4. Rode testes — procure `PEDAGOGY-TEST: ID` nos arquivos de teste.
5. Consulte `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` só ao travar; inclui mapa starter→TODO e Relatório de resolução.
6. Compare com `solutions/` após tentativa honesta; registre benchmark em `BENCHMARK_GUIADO.md`.

## Ordem recomendada

1. `ai/tiled_matmul_cache`
2. `dotnet/cil_tiny_decoder`
3. `graphics/vulkan_d3d12_resource_states`
4. `javascript/bytecode_branch_vm`
5. `linux/distro_pkg_rootfs`
6. `linux/kernel_module_driver_lab`
7. `linux/pty_ansi_terminal`
8. `nodejs/stream_transform_backpressure`
9. `redteam/elf_entry_inspector`
10. `systems/bitmap_page_allocator`

## Gates de qualidade

```bash
python scripts/pedagogy_check_unified.py --day 2026-09-05
python scripts/run_day_tests.py --day 2026-09-05 --mode solutions
python scripts/run_day_tests.py --day 2026-09-05 --mode starter --expect-fail
```

Opcional: export DOCX via `python scripts/build_day_docx.py --day 2026-09-05`.
