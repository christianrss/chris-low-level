# Resolucao guiada — elf64_relocation_triage

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D8-ELF-MAGIC` | `starter/elf64_relocation_triage.py` | `triage` |
| `D8-ELF-CLASS` | `starter/elf64_relocation_triage.py` | `triage` |
| `D8-ELF-RELOC` | `starter/elf64_relocation_triage.py` | `triage` |


## Baseline

```powershell
cd days/2026-09-10/redteam/elf64_relocation_triage/starter
python test_elf64_relocation_triage.py
```

**Esperado antes dos TODOs:** FAIL.


## D8-ELF-MAGIC

### Onde colocar (D8-ELF-MAGIC)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/elf64_relocation_triage.py` |
| Funcao | `triage` |
| Substituir | corpo sob `TODO [D8-ELF-MAGIC]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-ELF-MAGIC` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-ELF-MAGIC`.

### Escreva o codigo

```python
    if data[:4] != b"\x7fELF":
        return {"ok": False, "reason": "magic"}
    if len(data) < 5 or data[4] != 2:
        return {"ok": False, "reason": "class"}
    n = data[5] if len(data) > 5 else 0
    return {"ok": True, "class": 64, "relocs": n}
```

### Por que funciona?
Materializa o contrato numerico de `D8-ELF-MAGIC`.

### Verifique
Baseline parcial; `D8-ELF-MAGIC` PASS.

### Checkpoint
- [ ] `D8-ELF-MAGIC` PASS

## D8-ELF-CLASS

### Onde colocar (D8-ELF-CLASS)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/elf64_relocation_triage.py` |
| Funcao | `triage` |
| Substituir | corpo sob `TODO [D8-ELF-CLASS]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-ELF-CLASS` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-ELF-CLASS`.

### Escreva o codigo

```python
    if len(data) < 5 or data[4] != 2:
        return {"ok": False, "reason": "class"}
    n = data[5] if len(data) > 5 else 0
    return {"ok": True, "class": 64, "relocs": n}
```

### Por que funciona?
Materializa o contrato numerico de `D8-ELF-CLASS`.

### Verifique
Baseline parcial; `D8-ELF-CLASS` PASS.

### Checkpoint
- [ ] `D8-ELF-CLASS` PASS

## D8-ELF-RELOC

### Onde colocar (D8-ELF-RELOC)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/elf64_relocation_triage.py` |
| Funcao | `triage` |
| Substituir | corpo sob `TODO [D8-ELF-RELOC]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-ELF-RELOC` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-ELF-RELOC`.

### Escreva o codigo

```python
    n = data[5] if len(data) > 5 else 0
    return {"ok": True, "class": 64, "relocs": n}
result = handle_d8_elf_reloc(state)
assert result is not None  # D8-ELF-RELOC
return result
```

### Por que funciona?
Materializa o contrato numerico de `D8-ELF-RELOC`.

### Verifique
Baseline parcial; `D8-ELF-RELOC` PASS.

### Checkpoint
- [ ] `D8-ELF-RELOC` PASS

## Debug

| Sintoma | Causa | Correcao |
|---------|-------|----------|
| stub | corpo intacto | cole o bloco |
| off-by-one | size | refaca trace |

## Relatorio de resolucao

- TODOs:
- Saida:
- Invariantes:
- Benchmark: nao executado
