# Resolucao guiada — clvm_v2_strings

## Mapa exato starter → resolução

| ID | Arquivo | Ancora |
|----|---------|--------|
| `CLVM-V2-POOL-01` | `starter/clvm_v2.py` | `encode_pool` / `decode_pool` |
| `CLVM-V2-PRINTS-01` | idem | `assemble_hello` / `run_v2` |

---

## CLVM-V2-POOL-01

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/clvm_v2.py` |
| **Função / âncora** | `TODO [CLVM-V2-POOL-01]` |
| **Substituir** | raises encode/decode |
| **Não mexer** | Dia 01 loader C |

### Escreva o codigo

Ver `solutions/clvm_v2.py` (`encode_pool` / `decode_pool`).

### Por que funciona

Lens LE + UTF-8 = pool deterministico.

### Verifique

Esperado: round-trip `["hi"]`. Depure offset apos count.

---

## CLVM-V2-PRINTS-01

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/clvm_v2.py` |
| **Função / âncora** | `assemble_hello` + case PRINTS |
| **Substituir** | raises PRINTS |
| **Não mexer** | numeros de opcode documentados |

### Escreva o codigo

```python
code = bytes([PRINTS]) + struct.pack("<H", 0) + bytes([HALT])
return build_image(code, ["hi"])
```

No run: ler u16, append `strings[idx]`.

### Por que funciona

Code referencia indice; texto vive no pool.

### Verifique

Esperado: stdout `hi`. Depure `data[4]==2`.

---

## Relatório de resolução

- TODOs: ___
- Testes esperado PASS: ___
- Depuracao: ___
- Duvidas: ___

Checklist: version byte == 2.
Checklist: checksum cobre code+pool.
Checklist: nao quebre labs v1.
Checklist: compare solutions apos tentar.
Checklist: leia docs/FORMAT_v2.md no chris-vm.

Fim da resolucao guiada do lab v2 strings (N4).
