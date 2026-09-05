# Exercícios — miniobjdump

## Fácil

- **OBJDUMP-U16-01:** leia halfword little-endian com bounds check.
- **OBJDUMP-U32-01:** leia word little-endian com bounds check.

## Médio

- **OBJDUMP-PARSE-01:** parse ELF header e enumere section headers.
- **OBJDUMP-TEXT-01:** dump hex da seção `.text` com offset correto.

## Difícil

- **OBJDUMP-VALID-01:** rejeite arquivos curtos ou magic inválido com mensagem clara.
- **OBJDUMP-SYMTAB-01:** leia `e_shstrndx` e resolva nomes de seção.

## Desafio

- **OBJDUMP-DIFF-01:** compare saída com `readelf -S` em binário de teste.
