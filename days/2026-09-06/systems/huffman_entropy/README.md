# Ordem de estudo deste módulo

1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Abra `starter/bit_io.cpp` e `starter/huffman.cpp`; localize `TODO [COMP-HUF-01..04]`.
3. Siga `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` na ordem dos TODOs.
4. Compile/teste após cada etapa.
5. Só então compare com `solutions/`.

---

# Treino Low-Level Systems — 2026-09-06 — Huffman entropy

Lab: **CHHUF** — Huffman clássico + bit packing MSB-first + tabela serializada.

## Estrutura

- `starter/`: `bit_io.cpp` / `huffman.cpp` com TODOs; `test_huffman.cpp`.
- `solutions/`: gabarito (`BitWriter`/`BitReader`, `build_huffman_codes`, encode/decode).
- Headers: `bit_io.hpp`, `huffman.hpp` (`CHHUF_MAGIC`, `HuffmanCodeEntry`).

## Pré-requisitos

- CMake 3.16+
- C++20

## Caminho recomendado

1. Bit I/O (`COMP-HUF-01`) até o Caso 1 passar na lógica.
2. Árvore (`COMP-HUF-02`).
3. Encode (`COMP-HUF-03`).
4. Decode (`COMP-HUF-04`).
5. Conferir gabarito.

## Build do starter (esperado FAIL)

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\systems\huffman_entropy\starter
cmake -S . -B build
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

Stubs: `write_bit` vazio, `read_bit` false, encode/decode false → testes falham. Intencional.

## Build do gabarito (esperado PASS)

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\systems\huffman_entropy\solutions
cmake -S . -B build
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

Saída: `OK huffman`.

## Linux/macOS/WSL

```bash
cd starter   # ou solutions
cmake -S . -B build && cmake --build build && ctest --test-dir build --output-on-failure
```

## O que os testes cobrem

| Caso | PEDAGOGY-TEST | Foco |
|------|---------------|------|
| 1 | COMP-HUF-01 | `0xB0` + leitura 1,0,1,1 |
| 2 | COMP-HUF-02 | tabela Huffman não vazia |
| 3 | COMP-HUF-03 | encode |
| 4 | COMP-HUF-04 | decode round-trip + magic ruim |

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-compress` |
| O que levar | `bit_io` + Huffman CHHUF + testes |
| Milestone | compressão — entropy coding |
| Commit sugerido | `feat(compress): port CHHUF Huffman from day lab` |
