# Ordem de estudo deste módulo

1. Leia `TEORIA_PASSO_A_PASSO.md` (Adler trace, CMF/FLG, CRC/gzip).
2. Abra `starter/` e localize `TODO [COMP-ZLIB-*]`.
3. Siga `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` sem pular etapas.
4. Compile/teste após cada TODO.
5. Só então compare com `solutions/`.

---

# Tooling — zlib/gzip containers — 2026-09-06

Envelopes **zlib** (Adler-32 BE) e **gzip** (CRC-32 + ISIZE LE) sobre DEFLATE stored já fornecido.

## Estrutura

- `starter/`: TODOs localizados (`adler32`, `zlib_wrap`, `crc32`, `gzip_wrap`).
- `solutions/`: gabarito com `PEDAGOGY-SOLUTION: COMP-ZLIB-*`.
- `test_zlib.cpp`: `PEDAGOGY-TEST` por ID.

## Pré-requisitos

- CMake 3.16+, C++17 (MSVC/GCC/Clang)
- Opcional: Python `zlib` para conferir Adler/CRC

## Caminho recomendado

1. Adler-32 → confira `0x11E60398`.
2. zlib compress/serialize → decompress.
3. CRC-32 → gzip wrap/unwrap.
4. `ctest` verde; preencha o Relatório de resolução.

## Build (Windows PowerShell)

```powershell
cmake -S days/2026-09-06/tooling/zlib_gzip_containers/starter -B days/2026-09-06/tooling/zlib_gzip_containers/starter/build -A x64
cmake --build days/2026-09-06/tooling/zlib_gzip_containers/starter/build --config Release
ctest --test-dir days/2026-09-06/tooling/zlib_gzip_containers/starter/build -C Release --output-on-failure
```

**Antes dos TODOs:** testes **FAIL** (esperado).  
**Depois:** stdout `OK zlib gzip containers`.

## Build do gabarito

```powershell
cmake -S days/2026-09-06/tooling/zlib_gzip_containers/solutions -B days/2026-09-06/tooling/zlib_gzip_containers/solutions/build_ci -A x64
cmake --build days/2026-09-06/tooling/zlib_gzip_containers/solutions/build_ci --config Release
ctest --test-dir days/2026-09-06/tooling/zlib_gzip_containers/solutions/build_ci -C Release
```

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-compress` |
| O que levar | Adler + zlib wrap (e CRC/gzip se o CLI expandir) |
| Testes | round-trip zlib / gzip |
| Commit sugerido | `feat(compress): port zlib/gzip containers from day06 lab` |
