# Resolução guiada passo a passo — Online softmax

Edite `starter/online_softmax.py`.

### TODO D6-SM-STATS
Inicialize:
```python
m = float("-inf")
d = 0.0
```
Para cada `x`:
```python
m_new = max(m, x)
d = d * math.exp(m - m_new) + math.exp(x - m_new)
m = m_new
```
No primeiro elemento, `m=-inf`; `exp(-inf-x)=0`, então o termo antigo desaparece.

### TODO D6-SM-NORMALIZE
Depois da passagem:
```python
return [math.exp(x-m)/d for x in values]
```

### TODO D6-SM-REFERENCE
Implemente também `softmax_two_pass` usando `m=max(values)` e compare elemento a elemento no teste.

Trace `[1000,1001]`: ingênuo overflowa; online usa referências 1000 e depois 1001, mantendo expoentes <= 1.
Execute `python starter/test_online_softmax.py`. Esperado: `chris-online-softmax tests passed`.
Debug: registre `(x,m_old,m_new,d_old,d_new)`.
