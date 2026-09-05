# Resolução guiada passo a passo

Abra `starter/elf_entry.py`.

## `parse_ident` - RT-ELF-HDR-01
Exija no mínimo 16 bytes. Confira `data[:4] == b"\x7fELF"`, `data[4] == 2` (ELF64) e `data[5] == 1` (little-endian). Em erro, levante `ValueError`.

## `parse_elf64` - RT-ELF-ENTRY-02
Exija no mínimo 64 bytes, chame `parse_ident(data)` e extraia:
```python
e_type, e_machine, e_version, e_entry = struct.unpack_from("<HHIQ", data, 16)
```
Retorne um dict com esses campos.

Teste:
```bash
python3 starter/test_elf_entry.py
```

Debug: use `data[:16].hex()` e `hex(e_entry)`. Não passe a fixture para `subprocess` nem tente executá-la.

## Mapa de consistência auditada
- `RT-ELF-HDR-01` - starter -> resolução -> teste -> solution.
- `RT-ELF-ENTRY-02` - starter -> resolução -> teste -> solution.
