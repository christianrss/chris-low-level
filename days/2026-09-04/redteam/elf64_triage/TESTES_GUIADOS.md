# Testes guiados — elf64_triage

Este arquivo é a ponte entre cada TODO real do `starter/` e a evidência que deve ficar verde. Não pule diretamente para `solutions/`.

## Baseline

A partir da pasta deste módulo:

```bash
python starter/tests/test_ascii_strings.py
python starter/tests/test_elf64.py
```

**Antes de implementar:** falham com `NotImplementedError`.

## Mapa TODO → teste

### `D2-ELF-STRINGS`
- Arquivo: `starter/tools/ascii_strings.py`
- Validação: extrai runs ASCII com offset e respeita `minimum`.
- Marcador: `PEDAGOGY-TEST: D2-ELF-STRINGS`

### `D2-ELF-HEADER`
- Arquivo: `starter/tools/elf64.py` → `parse_elf64_header`
- Validação: fixture curto (machine/entry/phnum/…) + rejeição de truncado/magic/class/endian/version.
- Marcador: `PEDAGOGY-TEST: D2-ELF-HEADER`

### `D2-ELF-PHDR`
- Arquivo: `starter/tools/elf64.py` → `parse_program_headers`
- Validação: fixture rico com 1× PT_LOAD (`type=1`, `vaddr=0x400000`, filesz/memsz = len(blob)).
- Marcador: `PEDAGOGY-TEST: D2-ELF-PHDR`

### `D2-ELF-SHDR`
- Arquivo: `starter/tools/elf64.py` → `parse_section_headers`
- Validação: resolve `.dynsym` / `.dynstr` via `shstrndx`; confere type/offset/size.
- Marcador: `PEDAGOGY-TEST: D2-ELF-SHDR`

### `D2-ELF-DYNSYM`
- Arquivo: `starter/tools/elf64.py` → `list_dynamic_symbols`
- Validação: um símbolo benigno `lab_main` com `st_value=0x401100`.
- Marcador: `PEDAGOGY-TEST: D2-ELF-DYNSYM`

## Depois de concluir

Rode novamente os mesmos comandos. Resultado esperado:

- `chris-binary-toolkit tests passed`
- `ELF64 triage tests passed`
- Não remova/afrouxe asserts.
- Compare com `solutions/` só depois do starter verde.
- Acrescente um edge case próprio (ex.: Phdr truncado) e anote a regressão.
