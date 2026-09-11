# Resolucao guiada — pike_regex_vm

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D9-PIKE-EPSILON` | `starter/pike_regex_vm.py` | `add_thread` |
| `D9-PIKE-STEP` | `starter/pike_regex_vm.py` | `run` |
| `D9-PIKE-TRACE` | `starter/pike_regex_vm.py` | `run` |
| `D9-PIKE-MATCH` | `starter/pike_regex_vm.py` | `run` |


## Baseline

```powershell
cd days/2026-09-11/parsers/pike_regex_vm/starter
python test_pike_regex_vm.py
```

**Esperado antes dos TODOs:** FAIL.


## D9-PIKE-EPSILON

### Onde colocar (D9-PIKE-EPSILON)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/pike_regex_vm.py` |
| Funcao | `add_thread` |
| Substituir | corpo sob `TODO [D9-PIKE-EPSILON]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-PIKE-EPSILON` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-PIKE-EPSILON`.

### Escreva o codigo

```python
    if pc in seen:return
    seen.add(pc);op=code[pc]
    if op[0]=="JMP":add_thread(code,op[1],out,seen);return
    if op[0]=="SPLIT":add_thread(code,op[1],out,seen);add_thread(code,op[2],out,seen);return
    out.append(pc)
def run(code,text,trace=False):
    cur=[];add_thread(code,0,cur,set());snap=[]
    for ch in text:
```

### Por que funciona?
Materializa o contrato numerico de `D9-PIKE-EPSILON`.

### Verifique
Baseline parcial; `D9-PIKE-EPSILON` PASS.

### Checkpoint
- [ ] `D9-PIKE-EPSILON` PASS

## D9-PIKE-STEP

### Onde colocar (D9-PIKE-STEP)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/pike_regex_vm.py` |
| Funcao | `run` |
| Substituir | corpo sob `TODO [D9-PIKE-STEP]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-PIKE-STEP` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-PIKE-STEP`.

### Escreva o codigo

```python
    cur=[];add_thread(code,0,cur,set());snap=[]
    for ch in text:
        if trace:snap.append(tuple(cur))
        nxt=[];seen=set()
        for pc in cur:
            op=code[pc]
            if op[0]=="CHAR" and ch==op[1]:add_thread(code,op[2],nxt,seen)
            elif op[0]=="ANY":add_thread(code,op[1],nxt,seen)
```

### Por que funciona?
Materializa o contrato numerico de `D9-PIKE-STEP`.

### Verifique
Baseline parcial; `D9-PIKE-STEP` PASS.

### Checkpoint
- [ ] `D9-PIKE-STEP` PASS

## D9-PIKE-TRACE

### Onde colocar (D9-PIKE-TRACE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/pike_regex_vm.py` |
| Funcao | `run` |
| Substituir | corpo sob `TODO [D9-PIKE-TRACE]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-PIKE-TRACE` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-PIKE-TRACE`.

### Escreva o codigo

```python
    if trace:snap.append(tuple(cur))
    ok=any(code[pc][0]=="MATCH" for pc in cur)
    return (ok,snap) if trace else ok
```

### Por que funciona?
Materializa o contrato numerico de `D9-PIKE-TRACE`.

### Verifique
Baseline parcial; `D9-PIKE-TRACE` PASS.

### Checkpoint
- [ ] `D9-PIKE-TRACE` PASS

## D9-PIKE-MATCH

### Onde colocar (D9-PIKE-MATCH)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/pike_regex_vm.py` |
| Funcao | `run` |
| Substituir | corpo sob `TODO [D9-PIKE-MATCH]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-PIKE-MATCH` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-PIKE-MATCH`.

### Escreva o codigo

```python
    ok=any(code[pc][0]=="MATCH" for pc in cur)
    return (ok,snap) if trace else ok
result = handle_d9_pike_match(state)
assert result is not None  # D9-PIKE-MATCH
return result
```

### Por que funciona?
Materializa o contrato numerico de `D9-PIKE-MATCH`.

### Verifique
Baseline parcial; `D9-PIKE-MATCH` PASS.

### Checkpoint
- [ ] `D9-PIKE-MATCH` PASS

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
