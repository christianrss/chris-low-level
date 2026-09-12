# clvm_xdbg — mini debugger da CLVM

CLI de texto no estilo xdbg: hex dump, disassembly da instrução em PC,
single-step, duas pilhas e RAM de 256 bytes. O alvo é a imagem CLVM v1
com a ISA estendida do Dia 04. Não há GUI Win32 nem anexação de processo.

**Carga:** 6–8 h | **Lane:** systems | **Ciclo:** depth-core-01

## Pré-requisitos

- Dia 01 (`systems/clvm`): header 16 B, FNV-1a, stack VM
- Dia 04 (`systems/clvm_extended`): CALL/RET, LOAD/STORE, EQ/LT/JNZ
- CMake + compilador C++17; Python 3 para o assembler e os testes

## O que você constrói

`starter/src/session.cpp` — o núcleo observável. O host (REPL, loader) e
o assembler já existem. Você **não** reimplementa o assembler.

## Comandos

```text
clvm-xdbg program.clvm
> hex
> disasm
> regs
> mem 0 64
> step
> break 13
> continue
> quit
```

## Ordem

TEORIA → EXERCICIOS (M1–M6) → `starter/src/session.cpp` → TESTES →
RESOLUCAO só ao travar → benchmark → `RUBRIC.md`.
