# Resolucao guiada — welford_layernorm

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D7-WEL-MEAN` | `starter/welford_layernorm.py` | `welford` |
| `D7-WEL-VAR` | `starter/welford_layernorm.py` | `welford` |
| `D7-WEL-NORM` | `starter/welford_layernorm.py` | `layernorm` |


## Baseline

```powershell
cd days/2026-09-09/ai/welford_layernorm/starter
python test_welford_layernorm.py
```

**Esperado antes dos TODOs:** FAIL.


## D7-WEL-MEAN

### Onde colocar (D7-WEL-MEAN)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/welford_layernorm.py` |
| Funcao | `welford` |
| Substituir | corpo sob `TODO [D7-WEL-MEAN]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-WEL-MEAN` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
    n = 0
    mean = 0.0
    m2 = 0.0
    for x in xs:
        n += 1
        d = x - mean
        mean += d / n
        m2 += d * (x - mean)
```

### Por que funciona?
Materializa o contrato numerico de `D7-WEL-MEAN`.

### Verifique
Baseline parcial; `D7-WEL-MEAN` PASS.

### Checkpoint
- [ ] `D7-WEL-MEAN` PASS

## D7-WEL-VAR

### Onde colocar (D7-WEL-VAR)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/welford_layernorm.py` |
| Funcao | `welford` |
| Substituir | corpo sob `TODO [D7-WEL-VAR]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-WEL-VAR` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
    n = 0
    mean = 0.0
    m2 = 0.0
    for x in xs:
        n += 1
        d = x - mean
        mean += d / n
        m2 += d * (x - mean)
```

### Por que funciona?
Materializa o contrato numerico de `D7-WEL-VAR`.

### Verifique
Baseline parcial; `D7-WEL-VAR` PASS.

### Checkpoint
- [ ] `D7-WEL-VAR` PASS

## D7-WEL-NORM

### Onde colocar (D7-WEL-NORM)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/welford_layernorm.py` |
| Funcao | `layernorm` |
| Substituir | corpo sob `TODO [D7-WEL-NORM]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-WEL-NORM` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
    mean, var = welford(xs)
    s = math.sqrt(var + eps)
    return [(x - mean) / s for x in xs]
```

### Por que funciona?
Materializa o contrato numerico de `D7-WEL-NORM`.

### Verifique
Baseline parcial; `D7-WEL-NORM` PASS.

### Checkpoint
- [ ] `D7-WEL-NORM` PASS

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
