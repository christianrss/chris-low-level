# Resolucao guiada — robin_hood_hash

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D9-RH-INSERT` | `starter/robin_hood_hash.py` | `insert` |
| `D9-RH-LOOKUP` | `starter/robin_hood_hash.py` | `lookup` |
| `D9-RH-PROBE` | `starter/robin_hood_hash.py` | `_probe` |


## Baseline

```powershell
cd days/2026-09-11/algorithms/robin_hood_hash/starter
python test_robin_hood_hash.py
```

**Esperado antes dos TODOs:** FAIL.


## D9-RH-INSERT

### Onde colocar (D9-RH-INSERT)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/robin_hood_hash.py` |
| Funcao | `insert` |
| Substituir | corpo sob `TODO [D9-RH-INSERT]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-RH-INSERT` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-RH-INSERT`.

### Escreva o codigo

```python
        idx = self._probe(key)
        d = 0
        while True:
            if self.keys[idx] is None:
                self.keys[idx] = key
                self.dist[idx] = d
                return idx
            if self.keys[idx] == key:
```

### Por que funciona?
Materializa o contrato numerico de `D9-RH-INSERT`.

### Verifique
Baseline parcial; `D9-RH-INSERT` PASS.

### Checkpoint
- [ ] `D9-RH-INSERT` PASS

## D9-RH-LOOKUP

### Onde colocar (D9-RH-LOOKUP)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/robin_hood_hash.py` |
| Funcao | `lookup` |
| Substituir | corpo sob `TODO [D9-RH-LOOKUP]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-RH-LOOKUP` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-RH-LOOKUP`.

### Escreva o codigo

```python
        idx = self._probe(key)
        d = 0
        while self.keys[idx] is not None and d <= self.cap:
            if self.keys[idx] == key:
                return idx
            if self.dist[idx] < d:
                return None
            idx = (idx + 1) % self.cap
```

### Por que funciona?
Materializa o contrato numerico de `D9-RH-LOOKUP`.

### Verifique
Baseline parcial; `D9-RH-LOOKUP` PASS.

### Checkpoint
- [ ] `D9-RH-LOOKUP` PASS

## D9-RH-PROBE

### Onde colocar (D9-RH-PROBE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/robin_hood_hash.py` |
| Funcao | `_probe` |
| Substituir | corpo sob `TODO [D9-RH-PROBE]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-RH-PROBE` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-RH-PROBE`.

### Escreva o codigo

```python
        return hash(key) % self.cap
    def insert(self, key):
        idx = self._probe(key)
        d = 0
        while True:
            if self.keys[idx] is None:
                self.keys[idx] = key
                self.dist[idx] = d
```

### Por que funciona?
Materializa o contrato numerico de `D9-RH-PROBE`.

### Verifique
Baseline parcial; `D9-RH-PROBE` PASS.

### Checkpoint
- [ ] `D9-RH-PROBE` PASS

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
