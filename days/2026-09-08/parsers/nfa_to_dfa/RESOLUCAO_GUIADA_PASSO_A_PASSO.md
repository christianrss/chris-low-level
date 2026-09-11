# Resolucao guiada — nfa_to_dfa

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D6-DFA-CLOSURE` | `starter/dfa.py` | `epsilon_closure` |
| `D6-DFA-SUBSET` | `starter/dfa.py` | `epsilon_closure` |
| `D6-DFA-MATCH` | `starter/dfa.py` | `subset_construct` |


## Baseline

```powershell
cd days/2026-09-08/parsers/nfa_to_dfa/starter
python test_dfa.py
```

**Esperado antes dos TODOs:** FAIL.


## D6-DFA-CLOSURE

### Onde colocar (D6-DFA-CLOSURE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/dfa.py` |
| Funcao | `epsilon_closure` |
| Substituir | corpo sob `TODO [D6-DFA-CLOSURE]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-DFA-CLOSURE` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-DFA-CLOSURE` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```python
PEDAGOGY-SOLUTION: D6-DFA-CLOSURE
    seen=set(states); stack=list(states)
    while stack:
        s=stack.pop()
        for sym,t in trans.get(s,[]):
            if sym is None and t not in seen: seen.add(t); stack.append(t)
    return seen
def subset_construct(trans,start,accept):
    # 
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-DFA-CLOSURE`.

### Verifique
Rode o baseline; o caminho de `D6-DFA-CLOSURE` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-DFA-CLOSURE` PASS
- [ ] Nao alterei o teste

## D6-DFA-SUBSET

### Onde colocar (D6-DFA-SUBSET)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/dfa.py` |
| Funcao | `epsilon_closure` |
| Substituir | corpo sob `TODO [D6-DFA-SUBSET]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-DFA-SUBSET` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-DFA-SUBSET` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```python
PEDAGOGY-SOLUTION: D6-DFA-SUBSET
    alphabet=sorted({sym for edges in trans.values() for sym,_ in edges if sym is not None})
    s0=frozenset(epsilon_closure(trans,{start})); ids={s0:0}; q=[s0]; table={}; accepting=set()
    while q:
        cur=q.pop(0); cid=ids[cur]
        if accept in cur: accepting.add(cid)
        for sym in alphabet:
            moved={t for s in cur for a,t in trans.get(s,[]) if a==sym}
            nxt=frozenset(epsilon_closure(trans,moved))
            if not nxt: continue
            if nxt not in ids: ids[nxt]=len(ids); q.append(nxt)
            table[(cid,sym)]=ids[nxt]
    return 0,accepting,table
def dfa_match(start,accepting,table,text):
    # 
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-DFA-SUBSET`.

### Verifique
Rode o baseline; o caminho de `D6-DFA-SUBSET` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-DFA-SUBSET` PASS
- [ ] Nao alterei o teste

## D6-DFA-MATCH

### Onde colocar (D6-DFA-MATCH)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/dfa.py` |
| Funcao | `subset_construct` |
| Substituir | corpo sob `TODO [D6-DFA-MATCH]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-DFA-MATCH` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-DFA-MATCH` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```python
PEDAGOGY-SOLUTION: D6-DFA-MATCH
    state=start
    for ch in text:
        key=(state,ch)
        if key not in table: return False
        state=table[key]
    return state in accepting
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-DFA-MATCH`.

### Verifique
Rode o baseline; o caminho de `D6-DFA-MATCH` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-DFA-MATCH` PASS
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
