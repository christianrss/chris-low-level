# Teoria passo a passo — Red Team seguro: ELF entry-point inspector

Um ELF64 little-endian começa com `0x7fELF`. `e_ident[4]` informa classe (2=64-bit), `e_ident[5]` endianess (1=little). No header ELF64, a partir do offset 16 aparecem `e_type` (2 bytes), `e_machine` (2), `e_version` (4), `e_entry` (8).

Esse exercício treina leitura de estruturas binárias e bounds checking, não exploração. Nenhum arquivo é executado.
