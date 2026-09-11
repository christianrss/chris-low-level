# Resolucao guiada — tiled_attention_online_softmax

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D8-ATT-TILE` | `starter/tiled_attention_online_softmax.py` | `online_softmax_update` |
| `D8-ATT-ONLINE` | `starter/tiled_attention_online_softmax.py` | `online_softmax_update` |
| `D8-ATT-OUT` | `starter/tiled_attention_online_softmax.py` | `finalize` |


## Baseline

```powershell
cd days/2026-09-10/ai/tiled_attention_online_softmax/starter
python test_tiled_attention_online_softmax.py
```

**Esperado antes dos TODOs:** FAIL.


## D8-ATT-TILE

### Onde colocar (D8-ATT-TILE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/tiled_attention_online_softmax.py` |
| Funcao | `online_softmax_update` |
| Substituir | corpo sob `TODO [D8-ATT-TILE]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-ATT-TILE` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-ATT-TILE`.

### Escreva o codigo

```python
    if not tile:
        return m, l
    tm = max(tile)
    nm = tm if m is None else max(m, tm)
    nl = 0.0
    if m is not None:
        nl = l * math.exp(m - nm)
    for x in tile:
```

### Por que funciona?
Materializa o contrato numerico de `D8-ATT-TILE`.

### Verifique
Baseline parcial; `D8-ATT-TILE` PASS.

### Checkpoint
- [ ] `D8-ATT-TILE` PASS

## D8-ATT-ONLINE

### Onde colocar (D8-ATT-ONLINE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/tiled_attention_online_softmax.py` |
| Funcao | `online_softmax_update` |
| Substituir | corpo sob `TODO [D8-ATT-ONLINE]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-ATT-ONLINE` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-ATT-ONLINE`.

### Escreva o codigo

```python
    if not tile:
        return m, l
    tm = max(tile)
    nm = tm if m is None else max(m, tm)
    nl = 0.0
    if m is not None:
        nl = l * math.exp(m - nm)
    for x in tile:
```

### Por que funciona?
Materializa o contrato numerico de `D8-ATT-ONLINE`.

### Verifique
Baseline parcial; `D8-ATT-ONLINE` PASS.

### Checkpoint
- [ ] `D8-ATT-ONLINE` PASS

## D8-ATT-OUT

### Onde colocar (D8-ATT-OUT)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/tiled_attention_online_softmax.py` |
| Funcao | `finalize` |
| Substituir | corpo sob `TODO [D8-ATT-OUT]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-ATT-OUT` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-ATT-OUT`.

### Escreva o codigo

```python
    if l == 0:
        return 0.0
    return weighted_sum / l
```

### Por que funciona?
Materializa o contrato numerico de `D8-ATT-OUT`.

### Verifique
Baseline parcial; `D8-ATT-OUT` PASS.

### Checkpoint
- [ ] `D8-ATT-OUT` PASS

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
