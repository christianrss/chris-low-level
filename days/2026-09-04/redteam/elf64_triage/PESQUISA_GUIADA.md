# Pesquisa guiada — ELF64 triage defensivo

## Fonte primária
System V ABI / AMD64 psABI, capítulo de Object Files / ELF Header:
https://refspecs.linuxfoundation.org/elf/x86_64-SysV-psABI.pdf

Índice de especificações ELF da Linux Foundation:
https://refspecs.linuxfoundation.org/

## Pesquise
- `ELF e_ident EI_CLASS EI_DATA`
- `Elf64_Ehdr e_machine e_entry e_phoff e_shoff`
- `EM_X86_64 value 62`
- `python struct unpack_from little endian`

## Perguntas
1. Qual é a magic ELF de 4 bytes?
2. Qual valor de `EI_CLASS` identifica ELF64?
3. Qual valor de `EI_DATA` identifica little-endian?
4. Onde ficam `e_machine`, `e_entry`, `e_phoff`, `e_shoff`, `e_phnum`, `e_shnum` e `e_shstrndx` no header de 64 bytes?
5. Por que um parser defensivo valida tamanho **antes** de `unpack_from`?

## Limite de segurança
Use somente fixtures e o `lab_target` produzido por este laboratório ou outros binários que você tenha autorização para analisar. O objetivo é formato/triagem, não evasão ou comprometimento.
