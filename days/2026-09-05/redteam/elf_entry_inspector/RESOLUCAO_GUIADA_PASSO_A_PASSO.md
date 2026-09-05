# Resolução guiada passo a passo — Red Team seguro: ELF entry-point inspector

Abra `starter/elf_entry.py`.

1. Em `parse_ident`, exija pelo menos 16 bytes, magic correto, classe 2 e little-endian 1.
2. Em `parse_elf64`, exija pelo menos 64 bytes, chame `parse_ident` e use `struct.unpack_from("<HHIQ", data, 16)` para extrair `e_type, e_machine, e_version, e_entry`.
3. Retorne dict com esses campos.

Execute `python starter/test_elf_entry.py`. Debug: imprima `data[:16].hex()` e `hex(entry)`; nunca tente executar a fixture.

## Mapa de consistência auditada
- `RT-ELF-HDR-01` — starter → resolução → teste → solution.
- `RT-ELF-ENTRY-02` — starter → resolução → teste → solution.
