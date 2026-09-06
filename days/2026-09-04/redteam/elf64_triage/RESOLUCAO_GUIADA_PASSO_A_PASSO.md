# RESOLUÇÃO GUIADA — Redteam / ELF64 triage defensivo

## Mapa exato starter → resolução

| TODO ID | Starter | Função/área |
|---------|---------|-------------|
| `D2-ELF-STRINGS` | `starter/tools/ascii_strings.py` | `extract_ascii_strings` |
| `D2-ELF-HEADER` | `starter/tools/elf64.py` | `parse_elf64_header` |
| `D2-ELF-PHDR` | `starter/tools/elf64.py` | `parse_program_headers` |
| `D2-ELF-SHDR` | `starter/tools/elf64.py` | `parse_section_headers` |
| `D2-ELF-DYNSYM` | `starter/tools/elf64.py` | `list_dynamic_symbols` |

Cada ID existe como `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` no gabarito e `PEDAGOGY-TEST: ID` nos testes.

> Trabalhe em `days/2026-09-04/redteam/elf64_triage/starter/`. `solutions/` é gabarito.

---

## Baseline

```bash
python starter/tests/test_ascii_strings.py
python starter/tests/test_elf64.py
```

Enquanto houver TODOs, espere `NotImplementedError`.

---

## Exercício Fácil — `D2-ELF-STRINGS`

### 1. O problema

Listar runs ASCII imprimíveis `(offset, text)` com `len >= minimum`.

### 2. O algoritmo

```text
results = []
start = None
para cada (index, byte) em (data + b"\x00"):
  printable = 0x20 <= byte <= 0x7E
  se printable e start is None: start = index
  senão se not printable e start is not None:
    se index - start >= minimum: append (start, decode)
    start = None
```

### 3. Escreva o código

```python
results: list[tuple[int, str]] = []
start: int | None = None
for index, byte in enumerate(data + b"\x00"):
    printable = 0x20 <= byte <= 0x7E
    if printable and start is None:
        start = index
    elif not printable and start is not None:
        if index - start >= minimum:
            results.append((start, data[start:index].decode("ascii")))
        start = None
return results
```

### 4. Por que funciona

A sentinela NUL fecha a última run. `minimum` reduz ruído de opcodes curtos.

### 5. Verifique

```bash
python starter/tests/test_ascii_strings.py
```

---

## Exercício Médio — `D2-ELF-HEADER`

### 1. O problema

Rejeitar lixo cedo; depois ler machine/entry/phoff/shoff/phnum/shnum/shstrndx.

### 2. O algoritmo

```text
len>=64, magic \x7fELF, class==2, data==1, version==1
unpack_from offsets 18,24,32,40,56,60,62
```

### 3. Escreva o código

```python
import struct
# ... validações ValueError ...
machine = struct.unpack_from("<H", data, 18)[0]
entry = struct.unpack_from("<Q", data, 24)[0]
phoff = struct.unpack_from("<Q", data, 32)[0]
shoff = struct.unpack_from("<Q", data, 40)[0]
phnum = struct.unpack_from("<H", data, 56)[0]
shnum = struct.unpack_from("<H", data, 60)[0]
shstrndx = struct.unpack_from("<H", data, 62)[0]
return Elf64Header(machine, entry, phoff, shoff, phnum, shnum, shstrndx)
```

### 4. Por que funciona

Offsets fixos do ELF64 Ehdr. Fixture curto espera `machine=62`, `entry=0x401000`, `phnum=3`, `shnum=12`, `shstrndx=11`.

### 5. Verifique

Parte do `test_elf64.py` (asserts de header) passa; Phdr/Shdr ainda falham até os próximos TODOs.

---

## Exercício Médio-Difícil — `D2-ELF-PHDR`

### 1. O problema

Ler `phnum` entradas de **56 bytes** a partir de `header.program_header_offset`. Campos: type, offset, vaddr, filesz, memsz.

### 2. O algoritmo

```text
end = phoff + phnum * 56
se end > len(data): ValueError
para i em 0..phnum-1:
  base = phoff + i * 56
  type   @ base+0  (<I)
  offset @ base+8  (<Q)
  vaddr  @ base+16 (<Q)
  filesz @ base+32 (<Q)
  memsz  @ base+40 (<Q)
```

### 3. Escreva o código

```python
phoff = header.program_header_offset
phnum = header.program_header_count
end = phoff + phnum * ELF64_PHDR_SIZE
if phoff < 0 or end > len(data):
    raise ValueError("program header table is truncated")
result = []
for index in range(phnum):
    base = phoff + index * ELF64_PHDR_SIZE
    p_type = struct.unpack_from("<I", data, base + 0)[0]
    p_offset = struct.unpack_from("<Q", data, base + 8)[0]
    p_vaddr = struct.unpack_from("<Q", data, base + 16)[0]
    p_filesz = struct.unpack_from("<Q", data, base + 32)[0]
    p_memsz = struct.unpack_from("<Q", data, base + 40)[0]
    result.append(Elf64Phdr(p_type, p_offset, p_vaddr, p_filesz, p_memsz))
return result
```

### 4. Por que funciona

O fixture rico tem 1× `PT_LOAD` (`type=1`) com `vaddr=0x400000` e `filesz=memsz=len(blob)`.

### 5. Verifique

Asserts de PHDR em `test_elf64.py` devem passar.

---

## Exercício Difícil — `D2-ELF-SHDR`

### 1. O problema

Ler `shnum` Shdr de **64 bytes**; resolver `name` via string table da seção `e_shstrndx`.

### 2. O algoritmo

```text
1) unpack name_index@0, type@4, offset@24, size@32 para cada i
2) str_off/size = raw[shstrndx]
3) name = C-string em data[str_off + name_index] (se name_index != 0)
```

### 3. Escreva o código

```python
# após montar lista raw de tuplas:
shstrndx = header.section_name_index
if shstrndx >= shnum:
    raise ValueError("e_shstrndx out of range")
str_off, str_size = raw[shstrndx][2], raw[shstrndx][3]
str_end = str_off + str_size
# ... bounds check ...
sections = []
for name_index, sh_type, sh_offset, sh_size in raw:
    name = _read_c_string(data, str_off + name_index, str_end) if name_index else ""
    sections.append(Elf64Shdr(name_index, sh_type, sh_offset, sh_size, name))
return sections
```

Helper sugerido: `find(b"\x00")` entre `start` e `end_limit`.

### 4. Por que funciona

No fixture: índice 1 → `.dynsym` (type 11 @ 0x100), índice 2 → `.dynstr` (type 3 @ 0x120). Nomes vêm de `.shstrtab` (shstrndx=3).

### 5. Verifique

Asserts de seções nomeadas passam.

---

## Exercício Difícil — `D2-ELF-DYNSYM`

### 1. O problema

Achar seções `.dynsym` / `.dynstr` (por nome; type 11/3 como reforço). Para cada `Elf64_Sym` de 24 B, emitir `(name, st_value)` se o nome não for vazio.

### 2. O algoritmo

```text
dynsym = seção nome ".dynsym" (type 11)
dynstr = seção nome ".dynstr" (type 3)
para base em dynsym.offset .. +size step 24:
  st_name  @ base+0 (<I)
  st_value @ base+8 (<Q)
  name = C-string(dynstr.offset + st_name)
  se name: append Elf64DynSym(name, st_value)
```

### 3. Escreva o código

```python
dynsym = _find_section(sections, ".dynsym", SHT_DYNSYM)
dynstr = _find_section(sections, ".dynstr", SHT_STRTAB)
if dynsym is None or dynstr is None:
    return []
# bounds + size % 24 == 0
symbols = []
for base in range(dynsym.offset, dynsym.offset + dynsym.size, ELF64_SYM_SIZE):
    st_name = struct.unpack_from("<I", data, base + 0)[0]
    st_value = struct.unpack_from("<Q", data, base + 8)[0]
    name = _read_c_string(data, dynstr.offset + st_name, dynstr.offset + dynstr.size) if st_name else ""
    if name:
        symbols.append(Elf64DynSym(name, st_value))
return symbols
```

### 4. Por que funciona

Fixture: um símbolo `lab_main` com `st_value=0x401100`. Entrada nula (se existisse) seria pulada.

### 5. Verifique

```bash
python starter/tests/test_elf64.py
```

Esperado: `ELF64 triage tests passed`.

---

## Analisar o alvo benigno (opcional, Linux)

```bash
cc -O0 -g starter/src/lab_target.c -o /tmp/chris_lab_target
readelf -h -l -S -s /tmp/chris_lab_target
```

Use só como oracle externo. Não execute binários desconhecidos.

---

## Debugging

| Sintoma | Ação |
|---------|------|
| Um campo Phdr errado | confira offsets 0/8/16/32/40 — não a tabela Elf32 |
| Nomes de seção vazios | `shstrndx` errado ou C-string além de `str_end` |
| Dynsym vazio | `.dynsym`/`.dynstr` não resolvidos; confira shstrtab |
| Última ASCII some | faltou sentinela `b"\x00"` |

```bash
python starter/benchmarks/elf64_benchmark.py
```

---

## Mapa de consistência auditada

- `D2-ELF-STRINGS` — `ascii_strings.py`
- `D2-ELF-HEADER` / `D2-ELF-PHDR` / `D2-ELF-SHDR` / `D2-ELF-DYNSYM` — `elf64.py`

Compare somente blocos `PEDAGOGY-SOLUTION`.

---

## Relatório de resolução

### O que foi validado

- Strings ASCII com sentinela + `minimum`
- Ehdr defensivo + Phdr/Shdr/Dynsym no fixture sintético

### Armadilhas

- Offsets Elf32 em parser 64-bit
- `sh_name` tratado como file offset
- Conclusão de malware só por símbolo/string benignos

### Próximo passo

Portar para `projects/chris-binary-toolkit` e cruzar com a regra YARA do módulo.
