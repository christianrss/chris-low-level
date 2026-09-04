# Teoria passo a passo — ELF64 e extração de strings

## 1. ELF
ELF é um formato de executável/objeto. Os primeiros bytes `0x7f 45 4c 46` identificam o formato. O array `e_ident` também informa classe e endianness.

## 2. Header de 64 bytes
Nosso parser cobre apenas subset ELF64 little-endian. Isso é deliberado: primeiro construir parser pequeno, validado e testável.

## 3. Campos estudados
`e_machine` identifica ISA; `e_entry` ponto de entrada; `e_phoff` e `e_shoff` apontam tabelas; contagens dizem quantas entradas existem; `e_shstrndx` indica a string table de nomes de seção.

## 4. Strings ASCII
Triagem simples encontra runs de bytes imprimíveis. Isso pode revelar mensagens/paths, mas também produz falsos positivos. Nunca conclua comportamento de um binário apenas por strings.
