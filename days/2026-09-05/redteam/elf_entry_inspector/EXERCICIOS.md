# Exercícios — ELF entry inspector

## Fácil — RT-ELF-HDR-01
Desenhe os 16 bytes de `e_ident` para um ELF64 LE válido.

## Médio — RT-ELF-HDR-01
Implemente `parse_ident()` rejeitando magic inválido e ELF32.

## Médio — RT-ELF-ENTRY-02
Implemente `parse_elf64()` extraindo `e_machine` e `e_entry` com `struct.unpack_from`.

## Difícil
Adicione suporte a leitura de `e_phoff` e `e_phnum` e explique por que ainda não dá para converter `e_entry` em offset de arquivo.

## Desafio
Parse um binário real (`/bin/ls`) e compare `e_entry` com saída de `readelf -h`.

## Reflexão
Por que parsers binários devem falhar explicitamente em vez de retornar valores default?
