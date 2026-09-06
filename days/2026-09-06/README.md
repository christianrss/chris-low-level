# Day 06 — 2026-09-06

Dia multi-módulo: **fundamentos de compressão** (RLE → Huffman → LZ77 → DEFLATE → zlib/gzip → PNG) + **portais Verlet** (gráficos/física) + trilhas AI / Red Team / .NET / Node / **Rust**.

Rust neste dia = **ownership + parsing de bytes não confiáveis** (mesmo formato CHRLE do lab C++, e member gzip estrutural sem inflate).

## Módulos (13) — ordem cognitiva

| # | Módulo | Fundamento a internalizar | Horas |
|---|--------|---------------------------|-------|
| 1 | `systems/rle_byte_codec` | Runs, header LE32, round-trip | 2–3 |
| 2 | `systems/huffman_entropy` | Frequência → árvore → bits MSB | 2–3 |
| 3 | `systems/lz77_dictionary` | Match (dist,len) vs literal | 2–3 |
| 4 | `systems/deflate_blocks` | BFINAL/BTYPE; stored + fixed | 3–4 |
| 5 | `tooling/zlib_gzip_containers` | CMF/FLG, Adler-32, CRC32 | 2–3 |
| 6 | `tooling/png_idat_pipeline` | Chunks IHDR/IDAT/IEND | 2–3 |
| 7 | `graphics/portal_verlet_physics` | Mat4 → portal → stencil → Verlet | 3–4 |
| 8 | `ai/tensor_entropy_lab` | Shannon + RLE em tensor | 2 |
| 9 | `redteam/compressed_blob_triage` | Magic bytes, limites, strings | 2 |
| 10 | `dotnet/span_deflate_buffers` | Span + inflate stored | 2 |
| 11 | `nodejs/gunzip_transform` | Transform + backpressure | 2 |
| 12 | `rust/rle_byte_codec` | CHRLE em Rust: `Result` + slices | 2 |
| 13 | `rust/gzip_member_parse` | Header/flags/trailer gzip sem panic | 2 |

**Total:** ~24–32 h.

## Projeto extra (fora do dia)

[`projects/chris-lantern-hunt/`](../../projects/chris-lantern-hunt/) — FPS horror OpenGL (capstone gráfico opcional).

## Capstone

[`projects/chris-compress/`](../../projects/chris-compress/) — CLI RLE + zlib stored.

## Como estudar

1. [`START_HERE.md`](START_HERE.md)
2. [`ATIVIDADES.md`](ATIVIDADES.md) — checkpoints **conceituais** (papel) antes de avançar
3. Por módulo: TEORIA → EXERCICIOS → starter → TESTES → RESOLUCAO (se travar)

## Validação

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-06
python scripts/run_day_tests.py --day 2026-09-06 --mode solutions
```

## Honestidade

- DEFLATE: subset RFC 1951 (stored + fixed).
- PNG: filtro `None` apenas.
- Portais: 1 nível de recursão stencil.
- Sem DOCX; pedagogia só em Markdown.
