# START HERE — Day 2026-09-06

Laboratório unificado. Cada pasta `<trilha>/<modulo>/` contém teoria, exercícios, resolução e código.

## Fluxo por módulo (igual Dia 01)

1. Leia `TEORIA_PASSO_A_PASSO.md` — O quê / Como / Por quê + **trace no papel**.
2. Faça o checkpoint conceitual de [`ATIVIDADES.md`](ATIVIDADES.md) **antes** de abrir o starter.
3. `EXERCICIOS.md` — Fácil → Desafio.
4. Implemente em `starter/` (`TODO [ID]`).
5. Rode testes (`PEDAGOGY-TEST: ID`). Esperado: FAIL até completar.
6. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` só ao travar — problema → algoritmo → código → entenda.
7. Compare `solutions/` após tentativa honesta; registre `BENCHMARK_GUIADO.md`.

## Ordem recomendada (fundamentos primeiro)

1. `systems/rle_byte_codec` — runs e header
2. `systems/huffman_entropy` — entropia e bits
3. `systems/lz77_dictionary` — dicionário
4. `systems/deflate_blocks` — blocos RFC 1951
5. `tooling/zlib_gzip_containers` — wrappers
6. `tooling/png_idat_pipeline` — chunks de arquivo
7. `graphics/portal_verlet_physics` — Mat4 / portal / Verlet / demo GL
8. `ai/tensor_entropy_lab`
9. `redteam/compressed_blob_triage`
10. `dotnet/span_deflate_buffers`
11. `nodejs/gunzip_transform`
12. `rust/rle_byte_codec` — mesmo wire CHRLE, superfície `Result`
13. `rust/gzip_member_parse` — offsets de member gzip (RFC 1952)

**Capstone:** `projects/chris-compress/` após 1–6.  
**Extra:** `projects/chris-lantern-hunt/` (fora deste dia).

## Como rodar Rust

```powershell
cd days/2026-09-06/rust/rle_byte_codec/starter
cargo test          # esperado FAIL até completar TODOs

cd ../solutions
cargo test          # esperado PASS

cd ../../gzip_member_parse/starter
cargo test
cd ../solutions
cargo test
```

Requer Rust/Cargo no PATH (`rustup`). Sem `cargo`, o runner do dia **pula** o módulo (mesmo padrão de `dotnet`/`npm`).

## Gates

```bash
python scripts/pedagogy_check_unified.py --day 2026-09-06
python scripts/run_day_tests.py --day 2026-09-06 --mode solutions
python scripts/run_day_tests.py --day 2026-09-06 --mode starter --expect-fail
```
