# Resolução guiada — ELF64 PHDR triage

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `D5-ELF-HEADER` | `starter/elf_phdr.py` | `parse_program_headers` (início) |
| `D5-ELF-PHDR` | `starter/elf_phdr.py` | loop de decode |
| `D5-ELF-RANGE` | `starter/elf_phdr.py` | checks antes de append |

Cada ID: `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` em `solutions/elf_phdr.py`, `PEDAGOGY-TEST: ID` em `starter/test_elf_phdr.py`.

> Edite apenas `starter/elf_phdr.py`. Fixture sintético — não execute binários desconhecidos.

## Baseline

```powershell
cd days/2026-09-07/redteam/elf_program_header_triage
python starter/test_elf_phdr.py
```

**Esperado:** FAIL — função retorna `[]` ou levanta exceção antes dos asserts.

---

## D5-ELF-HEADER — validar ELF64 LE e localizar tabela

### O problema

Sem validação, `parse_program_headers` retorna lista vazia. O teste espera duas entradas parseadas a partir do fixture de 256 bytes.

Stub:

```python
def parse_program_headers(data: bytes):
    # TODO [D5-ELF-HEADER]: valide ELF64 LE e localize tabela.
    # TODO [D5-ELF-PHDR]: leia Elf64_Phdr.
    # TODO [D5-ELF-RANGE]: valide ranges e PT_LOAD sizes.
    return []
```

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/elf_phdr.py` |
| **Função / âncora** | `parse_program_headers` — comentário `TODO [D5-ELF-HEADER]` |
| **Substituir** | `return []` por validação + variáveis `phoff`, `ents`, `num` + `out=[]` |
| **Não mexer** | fixture em `test_elf_phdr.py` |

### Código — bloco HEADER

```python
def parse_program_headers(data: bytes):
    if len(data) < 64 or data[:4] != b"\x7fELF" or data[4] != 2 or data[5] != 1:
        raise ValueError("invalid ELF64 LE")
    phoff = int.from_bytes(data[32:40], "little")
    ents = int.from_bytes(data[54:56], "little")
    num = int.from_bytes(data[56:58], "little")
    if ents < 56 or phoff + ents * num > len(data):
        raise ValueError("truncated phdr table")
    out = []
```

### Por que funciona?

- Magic + class + endian filtram formatos fora do lab antes de offsets.
- `phoff + ents*num <= len(data)` garante que o loop não lê além do buffer.
- `ents >= 56` é tamanho mínimo de `Elf64_Phdr` na ABI.

### Verificação parcial

```powershell
python -c "import sys; sys.path.insert(0,'starter'); from test_elf_phdr import make; from elf_phdr import parse_program_headers; d=make(); print(parse_program_headers(d))"
```

Ainda falha ou retorna vazio até PHDR — próximo TODO.

---

## D5-ELF-PHDR — decodificar cada entrada

### O problema

Com header ok mas sem loop, `out` permanece vazio. Teste exige `len(x)==2` e `x[0]["type"]==1`.

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/elf_phdr.py` |
| **Função / âncora** | logo após `out = []` — comentário `TODO [D5-ELF-PHDR]` |
| **Inserir** | loop `for i in range(num)` com leitura de campos |
| **Não mexer** | validação de header já escrita |

### Código — loop decode (RANGE ainda pendente)

```python
    for i in range(num):
        o = phoff + i * ents
        typ = int.from_bytes(data[o:o+4], "little")
        flags = int.from_bytes(data[o+4:o+8], "little")
        po = int.from_bytes(data[o+8:o+16], "little")
        va = int.from_bytes(data[o+16:o+24], "little")
        fs = int.from_bytes(data[o+32:o+40], "little")
        ms = int.from_bytes(data[o+40:o+48], "little")
        al = int.from_bytes(data[o+48:o+56], "little")
        out.append(dict(type=typ, flags=flags, offset=po, vaddr=va, filesz=fs, memsz=ms, align=al))
    return out
```

### Por que funciona?

- `o = phoff + i * ents` respeita stride do header — entrada 1 começa em 120 no fixture.
- Offsets +8/+16/+32… seguem layout ELF64 Phdr, não ELF32.
- Dict com chaves nomeadas casa com asserts do teste.

### Verificação parcial

**Esperado:** `len==2`, primeira entrada `type==1`. Teste de mutação RANGE ainda pode passar indevidamente até próximo TODO.

---

## D5-ELF-RANGE — bounds e PT_LOAD

### O problema

Sem checks, mutação `p_offset=250` + `filesz=16` passa — parser aceita segmento fora do arquivo.

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/elf_phdr.py` |
| **Função / âncora** | dentro do loop, **antes** de `out.append` — `TODO [D5-ELF-RANGE]` |
| **Inserir** | dois `if` de validação |
| **Não mexer** | offsets de decode |

### Código — bloco RANGE

```python
        if po + fs > len(data):
            raise ValueError("segment outside file")
        if typ == 1 and ms < fs:
            raise ValueError("PT_LOAD memsz < filesz")
        out.append(dict(type=typ, flags=flags, offset=po, vaddr=va, filesz=fs, memsz=ms, align=al))
```

### Por que funciona?

- `po + fs > len(data)` detecta segmento que ultrapassa o buffer — caso do teste mutado.
- `typ == 1` restringe regra BSS a PT_LOAD: memória reservada deve cobrir bytes do arquivo.
- Validar **antes** de append impede entrada inválida na lista de saída.

### Verificação final

```powershell
python starter/test_elf_phdr.py
```

**Esperado:** `chris-elf-phdr tests passed`.

---

## Debug

| Sintoma | Causa | Correção |
|---------|-------|----------|
| `typ` absurdo na 2ª entrada | stride errado | confira `o = phoff + i*ents` |
| mutação passa | RANGE ausente | `po+fs > len(data)` |
| `truncated phdr table` no fixture ok | `phoff` lido errado | offset 32:40 u64 LE |
| IndexError | bounds antes do loop | `phoff+ents*num <= len` |

Use `breakpoint()` após ler `phoff, ents, num` e dentro do loop imprima `i, o, typ, po, fs`.

---

## Relatório de resolução

1. **Offset byte de `e_phoff` no ELF64:** _____
2. **Onde começa entrada 1 no fixture (phoff=64, ents=56):** _____
3. **Por que `memsz >= filesz` só para PT_LOAD?** _____
4. **Mensagem de erro na mutação do teste:** _____
5. **Campo que mais confundiu offsets ELF32 vs 64:** _____
