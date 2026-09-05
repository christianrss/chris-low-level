# Resolução guiada passo a passo — ELF64 triage defensivo

## Mapa exato starter → resolução

- `D2-ELF-STRINGS` → `starter/tools/ascii_strings.py`
- `D2-ELF-HEADER` → `starter/tools/elf64.py`

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

## Baseline
Na raiz do repositório:

```bash
python days/2026-09-04/redteam/elf64_triage/starter/tests/test_elf64.py
python days/2026-09-04/redteam/elf64_triage/starter/tests/test_ascii_strings.py
```

Ambos devem falhar com `NotImplementedError`.

## Fácil — extractor de strings
Abra `starter/tools/ascii_strings.py`.

Comece:

```python
results: list[tuple[int, str]] = []
start: int | None = None
```

Percorra `data + b"\x00"`; a sentinela força o fechamento de string que termina no último byte:

```python
for index, byte in enumerate(data + b"\x00"):
    printable = 0x20 <= byte <= 0x7E
```

Início de run:

```python
if printable and start is None:
    start = index
```

Fim de run:

```python
elif not printable and start is not None:
    if index - start >= minimum:
        text = data[start:index].decode("ascii")
        results.append((start, text))
    start = None
```

Ao final:

```python
return results
```

### Por que funciona?
A sentinela `b"\x00"` força fechamento de run que termina no último byte do arquivo. Só bytes printable (0x20–0x7E) contam; runs curtas que `minimum` filtra reduzem ruído em binários.

Rode `test_ascii_strings.py`; esperado `chris-binary-toolkit tests passed`.

## Médio — estrutura do ELF header
Abra `starter/tools/elf64.py`. Adicione:

```python
import struct
```

Valide tamanho:

```python
if len(data) < 64:
    raise ValueError("ELF64 header is truncated")
```

Magic/class/data/version:

```python
if data[:4] != b"\x7fELF": raise ValueError("ELF magic mismatch")
if data[4] != 2: raise ValueError("only ELFCLASS64 is supported")
if data[5] != 1: raise ValueError("only little-endian ELF is supported")
if data[6] != 1: raise ValueError("unsupported ELF identification version")
```

### Por que funciona?
Checagens em cascata falham cedo com mensagens distintas — mais útil em triage que um único “invalid ELF”. `len(data) < 64` precede qualquer indexação além de `e_ident`.

## Difícil — ler campos pelos offsets da especificação
Use little-endian (`<`). Digite:

```python
machine = struct.unpack_from("<H", data, 18)[0]
entry = struct.unpack_from("<Q", data, 24)[0]
phoff = struct.unpack_from("<Q", data, 32)[0]
shoff = struct.unpack_from("<Q", data, 40)[0]
phnum = struct.unpack_from("<H", data, 56)[0]
shnum = struct.unpack_from("<H", data, 60)[0]
shstrndx = struct.unpack_from("<H", data, 62)[0]
```

Retorne:

```python
return Elf64Header(machine, entry, phoff, shoff, phnum, shnum, shstrndx)
```

### Por que funciona?
Offsets 18, 24, 32… são fixos no ELF64 header independente do alvo. `<H` e `<Q` com little-endian reproduzem o layout do fixture (`machine=62`, `entry=0x401000`). `unpack_from` lê in-place sem fatiar cópias extras.

O fixture do teste espera `machine=62`, `entry=0x401000`, `phnum=3`, `shnum=12`, `shstrndx=11`.

## Debugging
Se um offset estiver errado, imprima `data[offset:offset+8].hex()` e compare com o valor empacotado em `tests/test_elf64.py`. Não “ajuste até passar”: volte à tabela do ELF header na especificação.

## Analisar o alvo benigno
Em Linux, compile apenas o nosso `lab_target.c`:

```bash
cc -O0 -g days/2026-09-04/redteam/elf64_triage/starter/src/lab_target.c -o /tmp/chris_lab_target
```

Depois, em uma cópia do extractor/CLI da solução ou pequeno script próprio, leia `/tmp/chris_lab_target` e passe os primeiros bytes a `parse_elf64_header`. Compare `machine` com `readelf -h /tmp/chris_lab_target` **apenas como oracle externo**.

## Benchmark

```bash
python days/2026-09-04/redteam/elf64_triage/starter/benchmarks/elf64_benchmark.py
```

Registre headers/s. Não interprete isso como velocidade de um analisador ELF completo; é apenas header parsing em memória.


## Solução final comentada
Depois de deixar o starter verde, compare somente os blocos `PEDAGOGY-SOLUTION` em `solutions/` correspondentes aos IDs do mapa. Se houver uma linha necessária no gabarito que não foi ensinada acima, trate como defeito do material e não como algo que você deveria adivinhar.

## Relatório de resolução

| ID | Arquivo | Aceite |
|----|---------|--------|
| D2-ELF-STRINGS | `ascii_strings.py` | runs ≥ minimum; sentinela NUL fecha última run |
| D2-ELF-HEADER | `elf64.py` | magic/class/endian; campos do fixture |

Aceite: ambos testes Python reportam `chris-binary-toolkit tests passed`. Offsets ELF devem bater com tabela da especificação — use hex dump, não ajuste mágico. Compare binário compilado de `lab_target.c` com `readelf -h` como sanity check externo.
