# Teoria passo a passo — Triagem ELF64 segura

## 1. Escopo
Somente fixtures sintéticas e binários próprios/benignos. Não há exploração, injeção, persistência, evasão ou acesso a processos de terceiros.

## 2. `e_ident`
Os primeiros bytes são `0x7F 'E' 'L' 'F'`. `EI_CLASS=2` indica ELF64, `EI_DATA=1` little-endian e `EI_VERSION=1` a versão de identificação.

## 3. Campos úteis
`e_machine` identifica a arquitetura; `e_entry` o entry point; `e_phoff/e_shoff` localizam program/section header tables; `e_phnum/e_shnum` dão contagens.

## 4. Parsing defensivo
Sempre valide tamanho, magic, class e endianness antes de ler offsets. Parser de binário deve tratar input como não confiável, mesmo no laboratório.

## 5. Exercícios
**Fácil:** reconheça magic/class/data.  
**Médio:** leia `e_machine` e `e_entry` com `struct.unpack_from`.  
**Difícil:** rejeite headers truncados/invalid magic/class/data.  
**Desafio:** adicione parser de section headers com bounds checks e nomes via `.shstrtab`.
