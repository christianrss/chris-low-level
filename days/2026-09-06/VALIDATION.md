# VALIDATION — Day 06

## Gates

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-06
python scripts/day_contract_check.py --day 2026-09-06
python scripts/run_day_tests.py --day 2026-09-06 --mode solutions
python scripts/run_day_tests.py --day 2026-09-06 --mode starter --expect-fail
```

## Expectativas

| Gate | Esperado |
|------|----------|
| pedagogy_check | **PASS** — 13 módulos, 48 TODOs (strict) |
| day_contract_check | **PASS** — infra + trilhas tier-A |
| cargo (Rust) | solutions PASS; starter FAIL até TODOs (skip se sem `cargo`) |
| solutions | PASS |
| starter | FAIL até TODOs |
| Anti-padding | zero `Nota pedagógica` gerada |

## Módulos

| Trilha | Módulo | Runner |
|--------|--------|--------|
| systems | rle_byte_codec, huffman_entropy, lz77_dictionary, deflate_blocks | ctest |
| tooling | zlib_gzip_containers, png_idat_pipeline | pytest |
| graphics | verlet_rope_3d | ctest |
| ai | tensor_entropy_lab | pytest |
| redteam | compressed_blob_triage | pytest |
| dotnet | span_deflate_buffers | dotnet test |
| nodejs | gunzip_transform | node test.js |
| rust | rle_byte_codec, gzip_member_parse | cargo test |

## Auditoria rápida anti-padding

```powershell
rg "Nota pedagógica" days/2026-09-06
rg "revise o TODO e escreva um parágrafo" days/2026-09-06
```

Ambos devem retornar vazio.
