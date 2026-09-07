# Ordem de estudo — CLVM v2 verify (Rust)

1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Abra `starter/src/lib.rs` e localize `TODO [CLVM-RS-V2-HEADER-01..STACK-04]`.
3. Siga `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` sem pular etapas.
4. Rode `cargo test` após cada TODO.
5. Confira o gabarito em `solutions/` somente depois de tentar.

---

# Treino Low-Level Rust — 2026-09-07 — CLVM v2 parser + PRINTS + stack verify

Lab: parser da **imagem CLVM version=2** em Rust — header FNV, pool de strings UTF-8, opcode `PRINTS` (0x21) e walk estático de verificação. Wire format idêntico ao lab Python `systems/clvm_v2_strings`.

## Estrutura

| Pasta | Conteúdo |
|-------|----------|
| `starter/` | stubs em `src/lib.rs`; testes `tests/clvm_v2_tests.rs`; fixtures `.clvm` |
| `solutions/` | gabarito completo |
| `fixtures/` | `hello_v2.clvm`, `bad_magic.clvm`, `bad_checksum.clvm` |

## Pré-requisitos

- Rust 1.70+ (`cargo`)
- Ter concluído (ou lido) `systems/clvm_v2_strings` e `systems/clvm_bytecode_verifier`

## TODOs

| ID | Função |
|----|--------|
| `CLVM-RS-V2-HEADER-01` | `parse_image` |
| `CLVM-RS-V2-POOL-02` | `encode_pool` / `decode_pool` |
| `CLVM-RS-V2-PRINTS-03` | `assemble_hello` / `run_prints` |
| `CLVM-RS-V2-STACK-04` | `verify_stack` |

## Build starter (esperado FAIL)

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-07\rust\clvm_v2_verify\starter
cargo test
```

## Build gabarito (esperado PASS)

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-07\rust\clvm_v2_verify\solutions
cargo test
```

## O que os testes cobrem

| Caso | PEDAGOGY-TEST | Comportamento |
|------|---------------|---------------|
| 1 | CLVM-RS-V2-HEADER-01 | parse fixture `hello_v2.clvm` |
| 2 | CLVM-RS-V2-HEADER-01 | rejeita magic/checksum |
| 3 | CLVM-RS-V2-POOL-02 | round-trip pool |
| 4 | CLVM-RS-V2-PRINTS-03 | stdout `hi\n` |
| 5 | CLVM-RS-V2-STACK-04 | OOB pool index |
| 6 | CLVM-RS-V2-HEADER-01 | `build_image` checksum FNV |

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | crate `clvm-v2` no `chris-vm` |
| O que levar | `parse_image`, `verify_stack`, `fnv1a32` |
| Commit sugerido | `feat(rust): CLVM v2 image parser from day lab` |
