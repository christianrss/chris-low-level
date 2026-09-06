# RESOLUÇÃO GUIADA — Red Team / ELF64 entry inspector

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `RT-ELF-HDR-01` | `starter/elf_entry.py` | `parse_ident` — magic, class, endian |
| `RT-ELF-ENTRY-02` | `starter/elf_entry.py` | `parse_elf64` — `e_type`…`e_entry` via `ELF64_OFFSETS` |

Cada ID existe como `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` no gabarito e `PEDAGOGY-TEST: ID` em `starter/test_elf_entry.py`.

> Trabalhe em `days/2026-09-05/redteam/elf_entry_inspector/starter/`. `solutions/` é gabarito — consulte só depois da tentativa.

> Não comece copiando `solutions/`. Rode o teste após cada TODO.

---

## RT-ELF-HDR-01 — validar `e_ident`

### 1. O problema (starter stub)

```python
def parse_ident(data: bytes) -> dict[str, Any]:
    """TODO [RT-ELF-HDR-01]"""
    raise NotImplementedError("RT-ELF-HDR-01")
```

`test_rejects_bad_magic` passa `b""` e `b"NOTELF"+…` para `parse_elf64`, que deve chamar `parse_ident` (ou repetir as checagens). Sem validação, o unpack lê lixo.

### 2. O algoritmo

```text
se len(data) < 16 → ValueError("truncated ident")
se data[0:4] ≠ 7F 45 4C 46 → ValueError("bad magic")
se data[4] ≠ 2 → ValueError("not ELF64")
se data[5] ≠ 1 → ValueError("not little-endian")
retornar {class: 64, little_endian: True}
```

### 3. Código completo

Substitua o corpo de `parse_ident` em `starter/elf_entry.py`:

```python
def parse_ident(data: bytes) -> dict[str, Any]:
    if len(data) < 16:
        raise ValueError("truncated ident")
    if data[:4] != b"\x7fELF":
        raise ValueError("bad magic")
    if data[4] != 2:
        raise ValueError("not ELF64")
    if data[5] != 1:
        raise ValueError("not little-endian")
    return {"class": 64, "little_endian": True}
```

### 4. Por que funciona?

- `len < 16` antes de `data[4]`/`data[5]`: evita `IndexError` no buffer vazio do teste.
- Magic `\x7fELF` é o contrato do formato; qualquer outra assinatura é rejeitada cedo.
- Byte 4 = `ELFCLASS64` (2); byte 5 = `ELFDATA2LSB` (1). O lab só aceita esse par — o resto do parser assume LE64.
- O dict retornado documenta o que foi validado; `parse_elf64` usa o side-effect de exceção, não os campos.

### 5. Verificação

```bash
python days/2026-09-05/redteam/elf_entry_inspector/starter/test_elf_entry.py
```

Esperado **ainda FAIL**: `parse_elf64` continua `NotImplementedError`. Isoladamente:

```python
from elf_entry import parse_ident
parse_ident(b"\x7fELF" + bytes([2, 1]) + bytes(10))  # → class 64
parse_ident(b"")  # → ValueError
```

---

## RT-ELF-ENTRY-02 — extrair `e_machine` e `e_entry`

### 1. O problema (starter stub)

```python
def parse_elf64(data: bytes) -> dict[str, Any]:
    """TODO [RT-ELF-ENTRY-02]"""
    raise NotImplementedError("RT-ELF-ENTRY-02")
```

O teste sintético grava em offset 16: `e_type=2`, `e_machine=62`, `e_version=1`, `e_entry=0x401000` e espera esses campos no dict.

### 2. O algoritmo

```text
se len(data) < 64 → ValueError("truncated ELF64 header")
parse_ident(data)
(e_type, e_machine, e_version, e_entry) ← unpack "<HHIQ" em ELF64_OFFSETS["e_type"] (16)
retornar dict com os quatro campos
```

Layout a partir do offset 16:

```text
+0  u16 e_type
+2  u16 e_machine
+4  u32 e_version
+8  u64 e_entry   → absoluto file offset 24
```

### 3. Código completo

```python
def parse_elf64(data: bytes) -> dict[str, Any]:
    if len(data) < 64:
        raise ValueError("truncated ELF64 header")
    parse_ident(data)
    e_type, e_machine, e_version, e_entry = struct.unpack_from(
        "<HHIQ", data, ELF64_OFFSETS["e_type"]
    )
    return {
        "e_type": e_type,
        "e_machine": e_machine,
        "e_version": e_version,
        "e_entry": e_entry,
    }
```

### 4. Por que funciona?

- Header ELF64 tem 64 bytes; truncar antes do unpack evita ler além do buffer.
- `parse_ident` primeiro: magic/class/endian já validados antes de confiar no LE unpack.
- `"<HHIQ"` casa com a sequência de tipos; `ELF64_OFFSETS["e_type"]` = 16 fixa o ponto de partida — `e_entry` cai em 24 sem hardcode solto.
- `e_machine == 62` é `EM_X86_64`; `0x401000` é o entry típico da fixture.

### 5. Verificação

```bash
python days/2026-09-05/redteam/elf_entry_inspector/starter/test_elf_entry.py
```

Saída esperada:

```text
OK ELF inspector
```

Trace do fixture sintético:

```text
struct.pack_into("<HHIQ", blob, 16, 2, 62, 1, 0x401000)
bytes[24:32] = 00 10 40 00 00 00 00 00  → e_entry = 0x401000
```

Debug se `e_entry` errado: `print(data[24:32].hex())`. Se magic inválido for aceito: `parse_elf64` não chamou `parse_ident`.

---

## Mapa de consistência auditada

- `RT-ELF-HDR-01` — `starter/elf_entry.py` → `solutions/elf_entry.py` (`parse_ident`).
- `RT-ELF-ENTRY-02` — `starter/elf_entry.py` → `solutions/elf_entry.py` (`parse_elf64`).

## Relatório de resolução

### O que foi validado

- TODOs `RT-ELF-HDR-01` e `RT-ELF-ENTRY-02` implementados em `starter/elf_entry.py`.
- `PEDAGOGY-TEST` em `test_elf_entry.py`: header sintético, fixture `hello_elf64.bin`, rejeição de magic/vazio.
- Starter original levanta `NotImplementedError` até cada ID ser preenchido.

### Armadilhas encontradas

- Validar `len` antes de indexar `e_ident`.
- Usar `ELF64_OFFSETS["e_type"]`, não offset 0 no unpack do header.
- `parse_elf64` deve rejeitar via `parse_ident` — o teste só chama `parse_elf64` nos casos ruins.

### Depuração e saída esperada

- **Depuração:** `data[:16].hex()` e `data[24:32].hex()`; confira LE de `0x401000`.
- **Saída esperada:** `OK ELF inspector`.

### Próximo passo sugerido

Refazer o parser sem olhar esta resolução. Depois registre offsets extras (`e_phoff`, `e_shnum`) em `BENCHMARK_GUIADO.md` se medir tempo de parse.
