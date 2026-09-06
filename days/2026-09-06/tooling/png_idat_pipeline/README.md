# Ordem de estudo deste módulo

1. Leia `TEORIA_PASSO_A_PASSO.md` (CRC de chunk, IHDR 13 B, filter None, pipeline IDAT).
2. Abra `starter/png.cpp` e localize `TODO [COMP-PNG-*]`.
3. Siga `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` na ordem 01→04.
4. Compile/teste após cada TODO.
5. Só então compare com `solutions/`.

---

# Tooling — PNG IDAT pipeline — 2026-09-06

PNG mínimo grayscale 8-bit: chunks com CRC, IHDR, scanlines filtro None, IDAT via `zlib_min` (stored + Adler).

## Estrutura

- `starter/`: TODOs em `png.cpp`; CRC/zlib/deflate auxiliares fornecidos.
- `solutions/`: gabarito com `PEDAGOGY-SOLUTION: COMP-PNG-*`.
- `test_png.cpp`: `PEDAGOGY-TEST` por ID.

## Pré-requisitos

- CMake 3.16+, C++17
- Recomendado: ter feito `tooling/zlib_gzip_containers` (Adler/CRC mental)
- Opcional: viewer PNG ou `pngcheck`

## Caminho recomendado

1. Chunk CRC + framing.
2. IHDR 13 bytes.
3. Filter None.
4. Encode/decode round-trip.
5. Relatório + benchmark 8×8.

## Build (Windows PowerShell)

```powershell
cmake -S days/2026-09-06/tooling/png_idat_pipeline/starter -B days/2026-09-06/tooling/png_idat_pipeline/starter/build -A x64
cmake --build days/2026-09-06/tooling/png_idat_pipeline/starter/build --config Release
ctest --test-dir days/2026-09-06/tooling/png_idat_pipeline/starter/build -C Release --output-on-failure
```

**Antes dos TODOs:** testes **FAIL**.  
**Depois:** `OK png idat pipeline`.

## Build do gabarito

```powershell
cmake -S days/2026-09-06/tooling/png_idat_pipeline/solutions -B days/2026-09-06/tooling/png_idat_pipeline/solutions/build_ci -A x64
cmake --build days/2026-09-06/tooling/png_idat_pipeline/solutions/build_ci --config Release
ctest --test-dir days/2026-09-06/tooling/png_idat_pipeline/solutions/build_ci -C Release
```

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-compress` (ou utilitário PNG dump) |
| O que levar | `png_chunk` / CRC(type+data) + `zlib_min` |
| Testes | round-trip 3×2 / 8×8 |
| Commit sugerido | `feat(png): port minimal IDAT pipeline from day06 lab` |
