# Ordem de estudo deste módulo

1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Abra `starter/src/lib.rs` e localize `TODO [RS-RLE-01..03]`.
3. Siga `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` sem pular etapas.
4. Rode `cargo test` após cada TODO.
5. Só então compare com `solutions/`.

---

# Treino Low-Level Rust — 2026-09-06 — RLE byte codec

Lab: **CHRLE** em Rust — mesmo wire format do lab C++ `systems/rle_byte_codec`, mas com `Result`, slices e ownership explícitos.

## Estrutura

- `starter/`: stubs em `src/lib.rs`; testes em `tests/rle_tests.rs`.
- `solutions/`: gabarito completo (`encode` / `decode` / `round_trip_ok`).
- Formato: magic `CHRLE` + length LE32 + pares `(count, byte)`.

## Pré-requisitos

- Rust 1.70+ (`rustup` / `cargo`)

## Caminho recomendado

1. Teoria: layout e paper-trace hex.
2. `RS-RLE-01` — encode.
3. `RS-RLE-02` — decode + magic/bounds.
4. `RS-RLE-03` — round-trip helper.
5. Conferir gabarito.

## Build do starter (esperado FAIL)

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\rust\rle_byte_codec\starter
cargo test
```

Os stubs usam `unimplemented!` / `Err` → testes falham. Isso é intencional.

## Build do gabarito (esperado PASS)

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\rust\rle_byte_codec\solutions
cargo test
```

## Linux/macOS/WSL

```bash
cd starter   # ou solutions
cargo test
```

## O que os testes cobrem

| Caso | PEDAGOGY-TEST | Comportamento |
|------|---------------|---------------|
| 1 | RS-RLE-01 | 10 zeros: magic + len + um run |
| 2 | RS-RLE-02 | `"ABCD"` round-trip via decode |
| 3 | RS-RLE-03 | `round_trip_ok` + magic corrompido |

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-compress` (sidecar Rust) ou crate dedicado |
| O que levar | `encode` / `decode` + testes |
| Milestone | compressão — RLE em Rust seguro |
| Commit sugerido | `feat(rust): port CHRLE RLE from day lab` |
