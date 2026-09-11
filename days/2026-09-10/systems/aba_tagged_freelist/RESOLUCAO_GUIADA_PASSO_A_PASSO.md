# Resolucao guiada — aba_tagged_freelist

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D8-ABA-PUSH` | `starter/aba_tagged_freelist.py` | `push` |
| `D8-ABA-POP` | `starter/aba_tagged_freelist.py` | `pop` |
| `D8-ABA-TAG` | `starter/aba_tagged_freelist.py` | `pack` |


## Baseline

```powershell
cd days/2026-09-10/systems/aba_tagged_freelist/starter
python test_aba_tagged_freelist.py
```

**Esperado antes dos TODOs:** FAIL.


## D8-ABA-PUSH

### Onde colocar (D8-ABA-PUSH)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/aba_tagged_freelist.py` |
| Funcao | `push` |
| Substituir | corpo sob `TODO [D8-ABA-PUSH]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-ABA-PUSH` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-ABA-PUSH`.

### Escreva o codigo

```python
        self.nodes[idx]["next"] = self.head
        self.nodes[idx]["tag"] = self.head_tag
        self.head = idx
        self.head_tag = (self.head_tag + 1) & 0xFFFF
    def pop(self):
        if self.head is None:
            return None
        idx = self.head
```

### Por que funciona?
Materializa o contrato numerico de `D8-ABA-PUSH`.

### Verifique
Baseline parcial; `D8-ABA-PUSH` PASS.

### Checkpoint
- [ ] `D8-ABA-PUSH` PASS

## D8-ABA-POP

### Onde colocar (D8-ABA-POP)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/aba_tagged_freelist.py` |
| Funcao | `pop` |
| Substituir | corpo sob `TODO [D8-ABA-POP]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-ABA-POP` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-ABA-POP`.

### Escreva o codigo

```python
        if self.head is None:
            return None
        idx = self.head
        nxt = self.nodes[idx]["next"]
        self.head = nxt
        self.head_tag = (self.head_tag + 1) & 0xFFFF
        return idx
```

### Por que funciona?
Materializa o contrato numerico de `D8-ABA-POP`.

### Verifique
Baseline parcial; `D8-ABA-POP` PASS.

### Checkpoint
- [ ] `D8-ABA-POP` PASS

## D8-ABA-TAG

### Onde colocar (D8-ABA-TAG)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/aba_tagged_freelist.py` |
| Funcao | `pack` |
| Substituir | corpo sob `TODO [D8-ABA-TAG]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-ABA-TAG` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-ABA-TAG`.

### Escreva o codigo

```python
        return (idx & 0xFFFF) | ((tag & 0xFFFF) << 16)
    def push(self, idx):
        self.nodes[idx]["next"] = self.head
        self.nodes[idx]["tag"] = self.head_tag
        self.head = idx
        self.head_tag = (self.head_tag + 1) & 0xFFFF
    def pop(self):
        if self.head is None:
```

### Por que funciona?
Materializa o contrato numerico de `D8-ABA-TAG`.

### Verifique
Baseline parcial; `D8-ABA-TAG` PASS.

### Checkpoint
- [ ] `D8-ABA-TAG` PASS

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
