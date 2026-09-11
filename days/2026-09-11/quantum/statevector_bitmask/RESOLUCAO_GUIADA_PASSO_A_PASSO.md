# Resolucao guiada — statevector_bitmask

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D9-Q-SET` | `starter/statevector_bitmask.py` | `set` |
| `D9-Q-GET` | `starter/statevector_bitmask.py` | `get` |
| `D9-Q-NORM` | `starter/statevector_bitmask.py` | `normalize` |


## Baseline

```powershell
cd days/2026-09-11/quantum/statevector_bitmask/starter
python test_statevector_bitmask.py
```

**Esperado antes dos TODOs:** FAIL.


## D9-Q-SET

### Onde colocar (D9-Q-SET)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/statevector_bitmask.py` |
| Funcao | `set` |
| Substituir | corpo sob `TODO [D9-Q-SET]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-Q-SET` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-Q-SET`.

### Escreva o codigo

```python
        self.amp[mask] = value
    def get(self, mask):
        return self.amp[mask]
    def normalize(self):
        s = math.sqrt(sum(a*a for a in self.amp))
        if s == 0:
            return
        self.amp = [a / s for a in self.amp]
```

### Por que funciona?
Materializa o contrato numerico de `D9-Q-SET`.

### Verifique
Baseline parcial; `D9-Q-SET` PASS.

### Checkpoint
- [ ] `D9-Q-SET` PASS

## D9-Q-GET

### Onde colocar (D9-Q-GET)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/statevector_bitmask.py` |
| Funcao | `get` |
| Substituir | corpo sob `TODO [D9-Q-GET]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-Q-GET` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-Q-GET`.

### Escreva o codigo

```python
        return self.amp[mask]
    def normalize(self):
        s = math.sqrt(sum(a*a for a in self.amp))
        if s == 0:
            return
        self.amp = [a / s for a in self.amp]
```

### Por que funciona?
Materializa o contrato numerico de `D9-Q-GET`.

### Verifique
Baseline parcial; `D9-Q-GET` PASS.

### Checkpoint
- [ ] `D9-Q-GET` PASS

## D9-Q-NORM

### Onde colocar (D9-Q-NORM)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/statevector_bitmask.py` |
| Funcao | `normalize` |
| Substituir | corpo sob `TODO [D9-Q-NORM]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-Q-NORM` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-Q-NORM`.

### Escreva o codigo

```python
        s = math.sqrt(sum(a*a for a in self.amp))
        if s == 0:
            return
        self.amp = [a / s for a in self.amp]
```

### Por que funciona?
Materializa o contrato numerico de `D9-Q-NORM`.

### Verifique
Baseline parcial; `D9-Q-NORM` PASS.

### Checkpoint
- [ ] `D9-Q-NORM` PASS

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
