# Pesquisa guiada — ELF64 triage defensivo

## Fonte primária
System V ABI / AMD64 psABI, capítulo de Object Files / ELF Header:
https://refspecs.linuxfoundation.org/elf/x86_64-SysV-psABI.pdf

Índice de especificações ELF da Linux Foundation:
https://refspecs.linuxfoundation.org/

## Pesquise
- `ELF e_ident EI_CLASS EI_DATA`
- `Elf64_Ehdr e_machine e_entry e_phoff e_shoff e_phnum e_shnum e_shstrndx`
- `Elf64_Phdr p_type p_offset p_vaddr p_filesz p_memsz` (56 bytes)
- `Elf64_Shdr sh_name sh_type sh_offset sh_size` (64 bytes) + `.shstrtab`
- `Elf64_Sym st_name st_value` (24 bytes) + `.dynsym` / `.dynstr`
- `EM_X86_64 value 62`
- `python struct unpack_from little endian`

## Perguntas
1. Qual é a magic ELF de 4 bytes?
2. Qual valor de `EI_CLASS` identifica ELF64?
3. Qual valor de `EI_DATA` identifica little-endian?
4. Onde ficam `e_phoff`, `e_shoff`, `e_phnum`, `e_shnum` e `e_shstrndx`?
5. Quais offsets relativos de `p_type`, `p_offset`, `p_vaddr`, `p_filesz`, `p_memsz` na Phdr de 56 B?
6. Como `sh_name` se combina com a seção em `e_shstrndx`?
7. Por que um parser defensivo valida tamanho **antes** de loops `phnum`/`shnum`?

## Limite de segurança
Use somente fixtures e o `lab_target` deste laboratório ou outros binários autorizados. Objetivo: formato/triagem, não evasão ou comprometimento. Sem conteúdo de malware.

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha após ler as fontes acima) | | |

## Checkpoint

Antes do primeiro `TODO [ID]`, explique Ehdr→Phdr→Shstrtab→Dynsym **sem** olhar a resolução.
