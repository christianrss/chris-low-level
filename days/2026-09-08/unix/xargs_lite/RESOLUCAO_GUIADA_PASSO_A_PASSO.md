# Resolucao guiada — xargs_lite

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D6-XARGS-SPLIT` | `starter/xargs_lite.py` | `split_items` |
| `D6-XARGS-BATCH` | `starter/xargs_lite.py` | `split_items` |
| `D6-XARGS-RUN` | `starter/xargs_lite.py` | `batches` |


## Baseline

```powershell
cd days/2026-09-08/unix/xargs_lite/starter
python test_xargs_lite.py
```

**Esperado antes dos TODOs:** FAIL.


## D6-XARGS-SPLIT

### Onde colocar (D6-XARGS-SPLIT)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/xargs_lite.py` |
| Funcao | `split_items` |
| Substituir | corpo sob `TODO [D6-XARGS-SPLIT]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-XARGS-SPLIT` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-XARGS-SPLIT` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```python
PEDAGOGY-SOLUTION: D6-XARGS-SPLIT
    return [x for x in data.split("\0") if x!=""] if nul else data.split()
def batches(items,n):
    # 
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-XARGS-SPLIT`.

### Verifique
Rode o baseline; o caminho de `D6-XARGS-SPLIT` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-XARGS-SPLIT` PASS
- [ ] Nao alterei o teste

## D6-XARGS-BATCH

### Onde colocar (D6-XARGS-BATCH)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/xargs_lite.py` |
| Funcao | `split_items` |
| Substituir | corpo sob `TODO [D6-XARGS-BATCH]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-XARGS-BATCH` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-XARGS-BATCH` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```python
PEDAGOGY-SOLUTION: D6-XARGS-BATCH
    if n<=0: raise ValueError("n")
    return [items[i:i+n] for i in range(0,len(items),n)]
def run_batches(command,items,n):
    # 
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-XARGS-BATCH`.

### Verifique
Rode o baseline; o caminho de `D6-XARGS-BATCH` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-XARGS-BATCH` PASS
- [ ] Nao alterei o teste

## D6-XARGS-RUN

### Onde colocar (D6-XARGS-RUN)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/xargs_lite.py` |
| Funcao | `batches` |
| Substituir | corpo sob `TODO [D6-XARGS-RUN]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-XARGS-RUN` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-XARGS-RUN` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```python
PEDAGOGY-SOLUTION: D6-XARGS-RUN
    for batch in batches(items,n):
        cp=subprocess.run(command+batch,shell=False)
        if cp.returncode!=0: return cp.returncode
    return 0
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-XARGS-RUN`.

### Verifique
Rode o baseline; o caminho de `D6-XARGS-RUN` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-XARGS-RUN` PASS
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
