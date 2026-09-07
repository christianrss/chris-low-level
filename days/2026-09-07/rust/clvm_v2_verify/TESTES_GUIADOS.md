# Testes guiados — CLVM v2 Rust

## Por que testar parse + run juntos?

Parser “quase certo” passa header mas quebra pool ou PRINTS. `tests/clvm_v2_tests.rs` amarra fixtures binárias aos IDs.

## CLVM-RS-V2-HEADER-01

### Caso 1 — hello fixture

1. `parse_image(fixture("hello_v2.clvm"))`.
2. `strings == ["hi"]`, `code[0]==PRINTS`, `code[3]==HALT`.

**Se falhar:** checksum só sobre code; ou `code_size` errado.

### Caso 2 — bad magic/checksum

1. `bad_magic` → `BadMagic`.
2. `bad_checksum` → `ChecksumMismatch`.

### Caso 6 — build_image FNV

`fnv1a32(body) == stored checksum`.

## CLVM-RS-V2-POOL-02

### Caso 3 — pool round-trip

Round-trip `["hi","world"]`, `end == pool.len()`.

## CLVM-RS-V2-PRINTS-03

### Caso 4 — PRINTS stdout

`run_prints(assemble_hello()) == "hi\n"`.

## CLVM-RS-V2-STACK-04

### Caso 5 — stack OOB

Índice 1 com `pool_len=1` → erro contendo `OOB`.

## Depuração

```powershell
cargo test caso_1 -- --nocapture
```
