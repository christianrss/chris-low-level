# Resolucao guiada — online_softmax

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D6-SM-STATS` | `starter/online_softmax.py` | `online_softmax` |
| `D6-SM-NORMALIZE` | `starter/online_softmax.py` | `online_softmax` |
| `D6-SM-REFERENCE` | `starter/online_softmax.py` | `softmax_two_pass` |


## Baseline

```powershell
cd days/2026-09-08/ai/online_softmax/starter
python test_online_softmax.py
```

**Esperado antes dos TODOs:** FAIL.


## D6-SM-STATS

### Onde colocar (D6-SM-STATS)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/online_softmax.py` |
| Funcao | `online_softmax` |
| Substituir | corpo sob `TODO [D6-SM-STATS]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-SM-STATS` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-SM-STATS` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```python
PEDAGOGY-SOLUTION: D6-SM-STATS
    m=float("-inf"); d=0.0
    for x in values:
        m_new=max(m,x); d=d*math.exp(m-m_new)+math.exp(x-m_new); m=m_new
    # 
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-SM-STATS`.

### Verifique
Rode o baseline; o caminho de `D6-SM-STATS` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-SM-STATS` PASS
- [ ] Nao alterei o teste

## D6-SM-NORMALIZE

### Onde colocar (D6-SM-NORMALIZE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/online_softmax.py` |
| Funcao | `online_softmax` |
| Substituir | corpo sob `TODO [D6-SM-NORMALIZE]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-SM-NORMALIZE` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-SM-NORMALIZE` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```python
PEDAGOGY-SOLUTION: D6-SM-NORMALIZE
    return [math.exp(x-m)/d for x in values]
def softmax_two_pass(values):
    # 
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-SM-NORMALIZE`.

### Verifique
Rode o baseline; o caminho de `D6-SM-NORMALIZE` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-SM-NORMALIZE` PASS
- [ ] Nao alterei o teste

## D6-SM-REFERENCE

### Onde colocar (D6-SM-REFERENCE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/online_softmax.py` |
| Funcao | `softmax_two_pass` |
| Substituir | corpo sob `TODO [D6-SM-REFERENCE]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-SM-REFERENCE` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-SM-REFERENCE` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```python
PEDAGOGY-SOLUTION: D6-SM-REFERENCE
    if not values: raise ValueError("empty")
    m=max(values); ex=[math.exp(x-m) for x in values]; s=sum(ex)
    return [x/s for x in ex]
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-SM-REFERENCE`.

### Verifique
Rode o baseline; o caminho de `D6-SM-REFERENCE` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-SM-REFERENCE` PASS
- [ ] Nao alterei o teste

## Debug

| Sintoma | Causa | Correcao |
|---------|-------|----------|
| stub | corpo intacto | cole o bloco do TODO |
| off-by-one | size/indice | refaca o trace |
| 2o caso falha | estado residual | reset |

## Relatorio de resolucao

- TODOs concluidos:
- Comandos + saida:
- Invariantes:
- Edge cases:
- Benchmark: nao executado / preencher
