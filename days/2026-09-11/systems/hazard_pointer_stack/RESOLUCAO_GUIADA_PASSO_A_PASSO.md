# Resolucao guiada — hazard_pointer_stack

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D9-HP-PUSH` | `starter/hazard_pointer_stack.py` | `push` |
| `D9-HP-POP` | `starter/hazard_pointer_stack.py` | `pop` |
| `D9-HP-PROTECT` | `starter/hazard_pointer_stack.py` | `protect` |


## Baseline

```powershell
cd days/2026-09-11/systems/hazard_pointer_stack/starter
python test_hazard_pointer_stack.py
```

**Esperado antes dos TODOs:** FAIL.


## D9-HP-PUSH

### Onde colocar (D9-HP-PUSH)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/hazard_pointer_stack.py` |
| Funcao | `push` |
| Substituir | corpo sob `TODO [D9-HP-PUSH]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-HP-PUSH` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-HP-PUSH`.

### Escreva o codigo

```python
        node = {"value": value, "next": self.head}
        self.head = node
    def pop(self):
        node = self.protect(self.head)
        if node is None:
            return None
        self.head = node["next"]
        if self.hazard is node:
```

### Por que funciona?
Materializa o contrato numerico de `D9-HP-PUSH`.

### Verifique
Baseline parcial; `D9-HP-PUSH` PASS.

### Checkpoint
- [ ] `D9-HP-PUSH` PASS

## D9-HP-POP

### Onde colocar (D9-HP-POP)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/hazard_pointer_stack.py` |
| Funcao | `pop` |
| Substituir | corpo sob `TODO [D9-HP-POP]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-HP-POP` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-HP-POP`.

### Escreva o codigo

```python
        node = self.protect(self.head)
        if node is None:
            return None
        self.head = node["next"]
        if self.hazard is node:
            self.hazard = None
        return node["value"]
```

### Por que funciona?
Materializa o contrato numerico de `D9-HP-POP`.

### Verifique
Baseline parcial; `D9-HP-POP` PASS.

### Checkpoint
- [ ] `D9-HP-POP` PASS

## D9-HP-PROTECT

### Onde colocar (D9-HP-PROTECT)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/hazard_pointer_stack.py` |
| Funcao | `protect` |
| Substituir | corpo sob `TODO [D9-HP-PROTECT]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-HP-PROTECT` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-HP-PROTECT`.

### Escreva o codigo

```python
        self.hazard = node
        return node
    def push(self, value):
        node = {"value": value, "next": self.head}
        self.head = node
    def pop(self):
        node = self.protect(self.head)
        if node is None:
```

### Por que funciona?
Materializa o contrato numerico de `D9-HP-PROTECT`.

### Verifique
Baseline parcial; `D9-HP-PROTECT` PASS.

### Checkpoint
- [ ] `D9-HP-PROTECT` PASS

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
