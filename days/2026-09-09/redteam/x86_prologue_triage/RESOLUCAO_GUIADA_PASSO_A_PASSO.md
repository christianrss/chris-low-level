# Resolucao guiada — x86_prologue_triage

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D7-X86-PUSH` | `starter/x86_prologue_triage.py` | `triage` |
| `D7-X86-MOV` | `starter/x86_prologue_triage.py` | `triage` |
| `D7-X86-STACK` | `starter/x86_prologue_triage.py` | `triage` |


## Baseline

```powershell
cd days/2026-09-09/redteam/x86_prologue_triage/starter
python test_x86_prologue_triage.py
```

**Esperado antes dos TODOs:** FAIL.


## D7-X86-PUSH

### Onde colocar (D7-X86-PUSH)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/x86_prologue_triage.py` |
| Funcao | `triage` |
| Substituir | corpo sob `TODO [D7-X86-PUSH]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-X86-PUSH` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
    if i < len(data) and data[i] == 0x55:
        out["push_rbp"] = True
        i += 1
    if data[i:i+3] == b"\x48\x89\xe5":
        out["frame_pointer"] = True
        i += 3
    if data[i:i+3] == b"\x48\x83\xec" and i + 4 <= len(data):
        out["stack_reserve"] = data[i+3]
```

### Por que funciona?
Materializa o contrato numerico de `D7-X86-PUSH`.

### Verifique
Baseline parcial; `D7-X86-PUSH` PASS.

### Checkpoint
- [ ] `D7-X86-PUSH` PASS

## D7-X86-MOV

### Onde colocar (D7-X86-MOV)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/x86_prologue_triage.py` |
| Funcao | `triage` |
| Substituir | corpo sob `TODO [D7-X86-MOV]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-X86-MOV` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
    if data[i:i+3] == b"\x48\x89\xe5":
        out["frame_pointer"] = True
        i += 3
    if data[i:i+3] == b"\x48\x83\xec" and i + 4 <= len(data):
        out["stack_reserve"] = data[i+3]
        i += 4
    elif data[i:i+3] == b"\x48\x81\xec" and i + 7 <= len(data):
        out["stack_reserve"] = int.from_bytes(data[i+3:i+7], "little")
```

### Por que funciona?
Materializa o contrato numerico de `D7-X86-MOV`.

### Verifique
Baseline parcial; `D7-X86-MOV` PASS.

### Checkpoint
- [ ] `D7-X86-MOV` PASS

## D7-X86-STACK

### Onde colocar (D7-X86-STACK)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/x86_prologue_triage.py` |
| Funcao | `triage` |
| Substituir | corpo sob `TODO [D7-X86-STACK]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-X86-STACK` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
    if data[i:i+3] == b"\x48\x83\xec" and i + 4 <= len(data):
        out["stack_reserve"] = data[i+3]
        i += 4
    elif data[i:i+3] == b"\x48\x81\xec" and i + 7 <= len(data):
        out["stack_reserve"] = int.from_bytes(data[i+3:i+7], "little")
        i += 7
    out["consumed"] = i
    return out
```

### Por que funciona?
Materializa o contrato numerico de `D7-X86-STACK`.

### Verifique
Baseline parcial; `D7-X86-STACK` PASS.

### Checkpoint
- [ ] `D7-X86-STACK` PASS

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
