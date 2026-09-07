# Ordem de estudo deste módulo

1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Abra `starter/` e localize os TODOs.
3. Siga `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` sem pular etapas.
4. Compile/teste após cada etapa.
5. Só então compare com `solutions/`.

---

# Treino Low-Level Systems — 2026-09-03

Projeto do dia: **CLVM (Christian Low-Level Virtual Machine)** — um formato binário, assembler, loader, VM de pilha e validador seguro.

## Estrutura

- `starter/`: versão para resolver os exercícios (TODOs localizados).
- `solutions/`: gabarito completo.
- `docs/FORMAT.md`: especificação binária CLVM v1.
- `tests/`: scripts de smoke test.

## Pré-requisitos

- Python 3.10+
- CMake 3.20+
- compilador C11 e C++17 (GCC/Clang/MSVC)
- Rust/Cargo para o exercício guiado `rust-validator` (`CLVM-RS-*`)
- opcional: GDB/LLDB, `xxd`/`hexdump`, `objdump`

## Caminho recomendado

1. Leia `docs/FORMAT.md`.
2. Comece em `starter/` e procure por `TODO`.
3. Faça primeiro o checksum FNV-1a em Python e C.
4. Complete o parser C.
5. Complete as operações aritméticas da VM C++.
6. Implemente labels/JMP/JZ no assembler e na VM.
7. Complete o **validador Rust** (`CLVM-RS-FNV-01` → `HEADER` → `WALK`) em `starter/rust-validator`.
8. Use `solutions/` apenas para conferência.

## Build do gabarito (Linux/macOS/WSL)

```bash
cd solutions
cmake -S . -B build
cmake --build build
python3 tools/assemble.py programs/arithmetic.asm arithmetic.clvm
./build/clvm arithmetic.clvm --trace
python3 tools/assemble.py programs/countdown.asm countdown.clvm
./build/clvm countdown.clvm --trace
```

Saída esperada de `arithmetic.clvm`: `38`.

Saída esperada de `countdown.clvm`:

```text
3
2
1
0
```

## Windows (PowerShell, Visual Studio Build Tools)

```powershell
cd solutions
cmake -S . -B build
cmake --build build --config Release
python tools/assemble.py programs/arithmetic.asm arithmetic.clvm
.\build\Release\clvm.exe arithmetic.clvm --trace
```

## Rust validator (exercício guiado)

O `starter/rust-validator` (gabarito em `solutions/rust-validator`) é um **validador estrutural** de CLVM: magic, bounds, FNV-1a e walk de opcodes — **não executa** bytecode. TODOs: `CLVM-RS-FNV-01`, `CLVM-RS-HEADER-01`, `CLVM-RS-WALK-01`.

```powershell
cd starter/rust-validator
cargo test
cargo run -- ../programs/../  # após montar um .clvm, aponte o path
```

Ou, pelo gate CMake: `ctest` chama `integration_test.py`, que roda `cargo test` se `cargo` estiver no PATH.

**Trilha Rust completa:** Dia 2026-09-06 (`rust/rle_byte_codec`, `rust/gzip_member_parse`).

## Inspeção binária

```bash
python3 solutions/tools/inspect_clvm.py solutions/arithmetic.clvm
xxd solutions/arithmetic.clvm
```

## Segurança

O laboratório trabalha apenas com um formato e VM educacionais próprios. Não executa código nativo
arbitrário nem interage com processos de terceiros.

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-vm` |
| O que levar | CLVM loader + stack VM |
| Testes a replicar | integration tests |
| Evolução | Dia 04 `systems/clvm_extended` (CALL/mem/cmp) → `projects/chris-vm` → **`js2clvm`** (JS subset → CLVM) |
| Milestone | MILESTONES.md — CLVM VM |
| Commit sugerido | `feat(vm): port CLVM from day01 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
