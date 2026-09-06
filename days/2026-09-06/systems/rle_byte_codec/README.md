# Ordem de estudo deste módulo

1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Abra `starter/rle.cpp` e localize `TODO [COMP-RLE-01..03]`.
3. Siga `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` sem pular etapas.
4. Compile/teste após cada TODO.
5. Só então compare com `solutions/`.

---

# Treino Low-Level Systems — 2026-09-06 — RLE byte codec

Lab: **CHRLE** — Run-Length Encoding com header `CHRLE` + length LE32 + pares `(count, byte)`.

## Estrutura

- `starter/`: TODOs em `rle.cpp`; testes em `test_rle.cpp`.
- `solutions/`: gabarito completo (`encode_rle` / `decode_rle`).
- APIs em `rle.hpp`: `CHRLE_MAGIC`, `encode_rle`, `decode_rle`.

## Pré-requisitos

- CMake 3.16+
- Compilador C++20 (MSVC / GCC / Clang)

## Caminho recomendado

1. Teoria: formato e traces hex.
2. `COMP-RLE-01` — encode.
3. `COMP-RLE-02` — decode + magic.
4. `COMP-RLE-03` — contrato `out.size() == len`.
5. Conferir gabarito.

## Build do starter (esperado FAIL)

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\systems\rle_byte_codec\starter
cmake -S . -B build
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

O stub retorna `false` em encode/decode → `CHECK(encode_rle(...))` falha. Isso é intencional.

## Build do gabarito (esperado PASS)

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\systems\rle_byte_codec\solutions
cmake -S . -B build
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

Saída do teste: `OK rle`.

## Linux/macOS/WSL

```bash
cd starter   # ou solutions
cmake -S . -B build && cmake --build build && ctest --test-dir build --output-on-failure
```

## O que os testes cobrem

| Caso | PEDAGOGY-TEST | Comportamento |
|------|---------------|---------------|
| 1 | COMP-RLE-01 | 10 zeros round-trip |
| 2 | COMP-RLE-02 | `"ABCD"` round-trip |
| 3 | COMP-RLE-03 | magic corrompido rejeitado |

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-compress` (ou codec RLE dedicado) |
| O que levar | `encode_rle` / `decode_rle` + testes de round-trip |
| Milestone | compressão — RLE |
| Commit sugerido | `feat(compress): port CHRLE RLE from day lab` |
