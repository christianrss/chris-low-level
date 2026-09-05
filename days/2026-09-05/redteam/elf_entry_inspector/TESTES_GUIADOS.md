# Testes guiados

### Caso 1: `python starter/test_elf_entry.py` — valida header sintético e fixture real.
### Caso 2: **Offset table:** campos lidos via `ELF64_OFFSETS['e_entry']` etc.
### Caso 3: **Fixture:** `fixtures/hello_elf64.bin` com e_machine=62, e_entry=0x401000.
### Caso 4: **Rejeição:** magic inválido e buffer vazio → ValueError.
### Caso 5: Valide solutions/ com os mesmos testes.

## RT-ELF-ENTRY-02

Invariante protegida pelo teste com `PEDAGOGY-TEST: RT-ELF-ENTRY-02`.

## RT-ELF-HDR-01

Invariante protegida pelo teste com `PEDAGOGY-TEST: RT-ELF-HDR-01`.
