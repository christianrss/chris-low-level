# Exercícios — ELF64 e extração de strings

## Fácil

- **D2-ELF-STRINGS:** implemente scanner de runs ASCII 0x20..0x7E com sentinela NUL.
- Liste offsets de strings em `b"Hello\x00World"` com minimum=4 e minimum=5.

## Médio

- **D2-ELF-HEADER:** valide magic, class, endian e version em `elf64.py`.
- Desenhe mapa dos primeiros 64 bytes com offsets dos campos lidos.

## Difícil

- Leia `machine`, `entry`, `phoff`, `shoff`, `phnum`, `shnum`, `shstrndx` com `struct.unpack_from`.
- Compile `lab_target.c` e compare `machine`/`entry` com `readelf -h` como oracle externo.

## Desafio

- Rode benchmark de headers/s e discuta diferença versus parser completo de seções.
- Escreva duas strings que parecem suspeitas mas são benignas em contexto CTF.
