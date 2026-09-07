# Resolução guiada — CLVM v2 strings (N4)

## Baseline

`starter/clvm_v2.py` já traz FNV-1a, `build_image`, `parse_image` e esqueleto de `run_v2`. Faltam:

- `encode_pool` / `decode_pool` → `NotImplementedError` (`CLVM-V2-POOL-01`)
- `assemble_hello` e case `PRINTS` em `run_v2` → `NotImplementedError` (`CLVM-V2-PRINTS-01`)

Estado do starter:

```powershell
cd starter
python clvm_v2.py
# NotImplementedError: TODO [CLVM-V2-POOL-01]: encode_pool
```

Após os TODOs:

```powershell
python clvm_v2.py
# hi
python tests/integration_test.py
# PASS
```

Não altere o loader C do Dia 01 (v1-only). Opcodes documentados: `PRINTS=0x21`, `HALT=0x08`.

---

## Mapa exato starter → resolução

| ID | Arquivo | Função / âncora | Substituir |
|----|---------|-----------------|------------|
| `CLVM-V2-POOL-01` | `starter/clvm_v2.py` | `encode_pool`, `decode_pool` | `raise NotImplementedError(...POOL-01...)` |
| `CLVM-V2-PRINTS-01` | idem | `assemble_hello`, `run_v2` case `PRINTS` | raises PRINTS |

---

## CLVM-V2-POOL-01

### 1. O problema (POOL-01)

`parse_image` chama `decode_pool(body, code_size)` mas o starter levanta `NotImplementedError` em `encode_pool`/`decode_pool`. Sem pool, checksum v2 e `PRINTS` não têm rodata para indexar.

### Onde colocar (POOL-01)

| | |
|--|--|
| **Arquivo** | `starter/clvm_v2.py` |
| **Funções** | `encode_pool`, `decode_pool` |
| **Âncora** | `# TODO [CLVM-V2-POOL-01]` |
| **Substituir** | ambos os `raise NotImplementedError(...POOL-01...)` |
| **Não mexer** | `build_image`, `parse_image`, FNV, header layout |

### Escreva o código — encode_pool

```python
def encode_pool(strings: list[str]) -> bytes:
    out = bytearray(struct.pack("<I", len(strings)))
    for s in strings:
        raw = s.encode("utf-8")
        out += struct.pack("<I", len(raw))
        out += raw
    return bytes(out)
```

### Escreva o código — decode_pool

```python
def decode_pool(data: bytes, offset: int) -> tuple[list[str], int]:
    (count,) = struct.unpack_from("<I", data, offset)
    offset += 4
    strings: list[str] = []
    for _ in range(count):
        (n,) = struct.unpack_from("<I", data, offset)
        offset += 4
        raw = data[offset : offset + n]
        offset += n
        strings.append(raw.decode("utf-8"))
    return strings, offset
```

### Por que funciona (POOL-01)

Formato determinístico: count LE, depois `len LE + bytes UTF-8`. `parse_image` chama `decode_pool(body, code_size)` — offset correto pula o bytecode.

### Verifique (POOL-01)

Round-trip `["hi"]` e `["hi","bye"]`. Hexdump: `01 00 00 00 02 00 00 00 68 69`.

### Debug (POOL-01)

Checksum falha após pool: confirme `build_image` hasheia `code + pool`. Offset errado: use `code_size`, não 0, em `parse_image`.

---

## CLVM-V2-PRINTS-01

### 1. O problema (PRINTS-01)

Bytecode referencia strings por índice; texto vive no pool. Sem `assemble_hello` e case `PRINTS` em `run_v2`, `python clvm_v2.py` aborta antes de imprimir `hi`.

### Onde colocar (PRINTS-01)

| | |
|--|--|
| **Arquivo** | `starter/clvm_v2.py` |
| **Funções** | `assemble_hello`, `run_v2` |
| **Âncora** | `# TODO [CLVM-V2-PRINTS-01]` |
| **Substituir** | raises em `assemble_hello` e no branch `if op == PRINTS` |
| **Não mexer** | `HALT`, `parse_image`, constantes de opcode |

### Escreva o código — assemble_hello

```python
def assemble_hello() -> bytes:
    # PRINTS 0; HALT
    code = bytes([PRINTS]) + struct.pack("<H", 0) + bytes([HALT])
    return build_image(code, ["hi"])
```

### Escreva o código — run_v2 (case PRINTS)

Substitua o raise dentro de `if op == PRINTS:` por:

```python
        if op == PRINTS:
            (idx,) = struct.unpack_from("<H", code, pc)
            pc += 2
            if idx >= len(strings):
                raise ValueError("string index OOB")
            out.append(strings[idx])
```

Contexto completo de `run_v2`:

```python
def run_v2(data: bytes) -> str:
    code, strings = parse_image(data)
    out: list[str] = []
    pc = 0
    while pc < len(code):
        op = code[pc]
        pc += 1
        if op == PRINTS:
            (idx,) = struct.unpack_from("<H", code, pc)
            pc += 2
            if idx >= len(strings):
                raise ValueError("string index OOB")
            out.append(strings[idx])
        elif op == HALT:
            break
        else:
            raise ValueError(f"unsupported op 0x{op:02x} in mini-v2 runner")
    return "\n".join(out) + ("\n" if out else "")
```

### Por que funciona (PRINTS-01)

Bytecode referencia strings por índice u16; texto vive no pool. `build_image` concatena code+pool e recalcula checksum v2.

### Verifique (PRINTS-01)

```powershell
cd starter
python clvm_v2.py
```

**Esperado:** stdout `hi` seguido de newline. `integration_test.py` → PASS.

### Debug (PRINTS-01)

stdout vazio: trace `strings` após `parse_image`. `string index OOB`: idx maior que `len(strings)-1`.

---

## Relatório de resolução

Preencha após concluir os TODOs:

- **TODOs concluídos:** `CLVM-V2-POOL-01`, `CLVM-V2-PRINTS-01`
- **Testes:** `python clvm_v2.py` → `hi`; `integration_test.py` → PASS
- **Depuração usada:** (ex.: hexdump pool, print `data[4]`, trace idx PRINTS)
- **Invariantes verificadas:** version=2; checksum sobre code||pool; round-trip UTF-8
- **Dúvidas:** ___

### Checklist final

- [ ] `encode_pool` / `decode_pool` round-trip com `["hi"]` e múltiplas strings
- [ ] `assemble_hello` emite `PRINTS` + u16(0) + `HALT`
- [ ] `run_v2` imprime pool[0] com newline
- [ ] Labs v1 (Dia 01) não modificados
- [ ] Leu `projects/chris-vm/docs/FORMAT_v2.md` para contexto experimental

Fim da resolução guiada do lab v2 strings (N4).
