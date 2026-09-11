# Resolucao guiada — branch_predictor

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D7-BR-INIT` | `starter/branch_predictor.py` | `__init__` |
| `D7-BR-PRED` | `starter/branch_predictor.py` | `predict` |
| `D7-BR-UPDATE` | `starter/branch_predictor.py` | `update` |


## Baseline

```powershell
cd days/2026-09-09/architecture/branch_predictor/starter
python test_branch_predictor.py
```

**Esperado antes dos TODOs:** FAIL.


## D7-BR-INIT

### Onde colocar (D7-BR-INIT)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/branch_predictor.py` |
| Funcao | `__init__` |
| Substituir | corpo sob `TODO [D7-BR-INIT]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-BR-INIT` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
        self.state = 1  # 0,1 not-taken; 2,3 taken
    def predict(self):
        return self.state >= 2
    def update(self, taken: bool):
        if taken:
            self.state = min(3, self.state + 1)
        else:
            self.state = max(0, self.state - 1)
```

### Por que funciona?
Materializa o contrato numerico de `D7-BR-INIT`.

### Verifique
Baseline parcial; `D7-BR-INIT` PASS.

### Checkpoint
- [ ] `D7-BR-INIT` PASS

## D7-BR-PRED

### Onde colocar (D7-BR-PRED)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/branch_predictor.py` |
| Funcao | `predict` |
| Substituir | corpo sob `TODO [D7-BR-PRED]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-BR-PRED` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
        return self.state >= 2
    def update(self, taken: bool):
        if taken:
            self.state = min(3, self.state + 1)
        else:
            self.state = max(0, self.state - 1)
```

### Por que funciona?
Materializa o contrato numerico de `D7-BR-PRED`.

### Verifique
Baseline parcial; `D7-BR-PRED` PASS.

### Checkpoint
- [ ] `D7-BR-PRED` PASS

## D7-BR-UPDATE

### Onde colocar (D7-BR-UPDATE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/branch_predictor.py` |
| Funcao | `update` |
| Substituir | corpo sob `TODO [D7-BR-UPDATE]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-BR-UPDATE` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
        if taken:
            self.state = min(3, self.state + 1)
        else:
            self.state = max(0, self.state - 1)
```

### Por que funciona?
Materializa o contrato numerico de `D7-BR-UPDATE`.

### Verifique
Baseline parcial; `D7-BR-UPDATE` PASS.

### Checkpoint
- [ ] `D7-BR-UPDATE` PASS

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
