# Resolução guiada passo a passo — chris-xargs-lite

Edite `starter/xargs_lite.py`.

### TODO D6-XARGS-SPLIT
`split_items(data,nul)`:
```python
if nul: return [x for x in data.split("\0") if x!=""]
return data.split()
```

### TODO D6-XARGS-BATCH
Gere fatias `items[i:i+n]`, rejeitando n<=0.

### TODO D6-XARGS-RUN
Para cada batch:
```python
cp=subprocess.run(command+batch, shell=False, text=True, capture_output=True)
```
Acumule return codes e pare no primeiro !=0. Não use `shell=True`.

Teste inclui item `"two words"` no modo NUL para provar preservação.
Execute `python starter/test_xargs_lite.py`.
