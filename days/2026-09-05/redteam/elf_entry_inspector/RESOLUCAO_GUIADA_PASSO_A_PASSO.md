# Resolução guiada passo a passo — Red Team — ELF64 entry inspector

## Mapa exato starter → resolução

- `RT-ELF-HDR-01` → `starter/elf_entry.py`, função `parse_ident`
- `RT-ELF-ENTRY-02` → `starter/elf_entry.py`, função `parse_elf64`

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-05/redteam/elf_entry_inspector/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

## 0. Preparar o projeto

Na raiz do repositório:

```bash
python days/2026-09-05/redteam/elf_entry_inspector/starter/test_elf_entry.py
```

Saída esperada **antes** dos TODOs: `NotImplementedError` ou falha de assert. Esse é o baseline.

## Exercício fácil — `parse_ident` (RT-ELF-HDR-01)

### Arquivo

Abra:

```text
starter/elf_entry.py
```

Localize:

```python
def parse_ident(data: bytes) -> dict[str, Any]:
```

Substitua o corpo por:

```python
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

### Por que funciona?

Os primeiros 16 bytes (`e_ident`) concentram tudo que você precisa para saber **como** interpretar o resto. Magic `\x7fELF` descarta lixo; byte 4 = 2 fixa ELF64; byte 5 = 1 fixa little-endian. Validar tamanho antes de `data[4]` evita `IndexError` em buffer vazio — o teste `test_rejects_bad_magic` passa `b""` de propósito.

### Verificação manual

| `data` | Resultado esperado |
|--------|-------------------|
| 16+ bytes com magic válido, class 2, LE | `{"class": 64, "little_endian": True}` |
| `b""` | `ValueError` |
| `b"NOTELF" + ...` | `ValueError("bad magic")` |

## Exercício médio — `parse_elf64` (RT-ELF-ENTRY-02)

Localize:

```python
def parse_elf64(data: bytes) -> dict[str, Any]:
```

Substitua o corpo por:

```python
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

### Por que funciona?

O formato `"<HHIQ"` corresponde exatamente à sequência de tipos no header a partir de offset 16: dois `u16`, um `u32`, um `u64` — todos little-endian (`<`). `ELF64_OFFSETS["e_type"]` é 16, então `e_machine` cai em 18 e `e_entry` em 24 sem você decorar números. Chamar `parse_ident` primeiro garante que magic/classe/endian já foram validados antes do unpack.

### Trace no papel

Fixture do teste grava em offset 24 o valor `0x401000`:

```text
struct.pack_into("<HHIQ", blob, 16, 2, 62, 1, 0x401000)
                              ^type ^mach ^ver ^entry@24
```

Resultado: `e_machine == 62`, `e_entry == 0x401000`.

## Rode os testes novamente

```bash
python days/2026-09-05/redteam/elf_entry_inspector/starter/test_elf_entry.py
```

Saída esperada:

```text
OK ELF inspector
```

## Como depurar se falhar

- **`e_entry` errado**: imprima `data[24:32].hex()` e compare com `0x401000` em LE (`00 10 40 00 00 00 00 00`).
- **`bad data accepted`**: `parse_elf64` deve chamar `parse_ident` ou repetir checagem de magic — buffer `b""` não pode retornar dict.
- **`e_machine` zero**: confira se `unpack_from` usa offset `ELF64_OFFSETS["e_type"]` (16), não 0.
- **Fixture file falha**: confirme que `fixtures/hello_elf64.bin` existe ao lado de `test_elf_entry.py`.

Debug rápido no REPL:

```python
from pathlib import Path
from elf_entry import parse_elf64
data = Path("starter/fixtures/hello_elf64.bin").read_bytes()
print(parse_elf64(data))
```

## Solução final comentada

Compare seu arquivo com `solutions/elf_entry.py`. Você deve conseguir justificar cada validação e o uso de `ELF64_OFFSETS` + `struct.unpack_from`.

## Relatório de resolução

| ID | Função | Resultado esperado |
|----|--------|-------------------|
| RT-ELF-HDR-01 | `parse_ident` | magic/class/endian validados; truncado rejeitado |
| RT-ELF-ENTRY-02 | `parse_elf64` | `e_machine`, `e_entry` corretos; header < 64 rejeitado |

Critério de aceite: `python starter/test_elf_entry.py` imprime `OK ELF inspector`. Se magic inválido não lança `ValueError`, revise `parse_ident` — o teste `test_rejects_bad_magic` depende disso.
