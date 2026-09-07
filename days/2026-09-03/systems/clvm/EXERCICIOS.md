# Exercícios — CLVM

## Fácil

- **CLVM-PY-FNV-01:** FNV-1a 32-bit em `assemble.py`.
- **CLVM-C-FNV-01:** mesma função em `clvm_loader.c`.

## Médio

- **CLVM-ASM-LABELS-01:** labels em duas passagens + `JMP`/`JZ`.
- **CLVM-C-HEADER-01:** valide magic, flags, entry e checksum.
- **CLVM-RS-FNV-01:** FNV-1a em `rust-validator` (`fnv1a32`).
- **CLVM-RS-HEADER-01:** validação de header CLVM em Rust (`validate`).

## Difícil

- **CLVM-VM-ARITH-01:** opcodes aritméticos e `PRINT` com stack underflow check.
- **CLVM-VM-JUMP-01:** saltos relativos signed 16-bit.
- **CLVM-RS-WALK-01:** walk estrutural de opcodes (PUSH/JMP/JZ) sem executar.

## Desafio

- **CLVM-TOOL-01:** desassembleador hex -> mnemônicos para o subset implementado.
