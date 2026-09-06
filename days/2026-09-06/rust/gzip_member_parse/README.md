# Ordem de estudo deste módulo

1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Abra `starter/src/lib.rs` e localize `TODO [RS-GZ-01..03]`.
3. Siga `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` sem pular etapas.
4. Rode `cargo test` após cada TODO.
5. Só então compare com `solutions/`.

---

# Treino Low-Level Rust — 2026-09-06 — Gzip member parse

Lab: parser **estrutural** de um member gzip (RFC 1952) — magic, flags, header variável, trailer CRC32/ISIZE. **Não** implementa inflate (isso fica no lab Node/`deflate_blocks`).

## Estrutura

- `starter/`: stubs em `src/lib.rs`; testes em `tests/gzip_tests.rs`.
- `solutions/`: gabarito (`validate_fixed_header`, `deflate_payload_start`, `parse_member`).
- Helpers já prontos: `crc32_gzip`, `build_minimal_member`.

## Pré-requisitos

- Rust 1.70+ (`cargo`)
- Ideal: ter visto `tooling/zlib_gzip_containers` e/ou `nodejs/gunzip_transform`

## Caminho recomendado

1. Teoria: layout fixo 10 bytes + flags.
2. `RS-GZ-01` — magic/method/flags.
3. `RS-GZ-02` — pular FEXTRA/FNAME/FCOMMENT/FHCRC.
4. `RS-GZ-03` — trailer e `GzipMemberView`.
5. Conferir gabarito.

## Build do starter (esperado FAIL)

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\rust\gzip_member_parse\starter
cargo test
```

## Build do gabarito (esperado PASS)

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\rust\gzip_member_parse\solutions
cargo test
```

## O que os testes cobrem

| Caso | PEDAGOGY-TEST | Comportamento |
|------|---------------|---------------|
| 1 | RS-GZ-01 | magic/method; reserved flags; truncado |
| 2 | RS-GZ-02 | FNAME zero-terminated → offset DEFLATE |
| 3 | RS-GZ-03 | `parse_member` offsets + CRC/ISIZE |

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | sidecar em `chris-compress` ou crate `gzip-triage` |
| O que levar | `parse_member` + CRC local |
| Commit sugerido | `feat(rust): gzip member structural parse from day lab` |
