# Resolucao guiada — bm25_code_ranker

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D6-BM25-TOKENIZE` | `starter/bm25.py` | `tokenize` |
| `D6-BM25-INDEX` | `starter/bm25.py` | `tokenize` |
| `D6-BM25-SCORE` | `starter/bm25.py` | `__init__` |
| `D6-BM25-EVAL` | `starter/bm25.py` | `rank` |


## Baseline

```powershell
cd days/2026-09-08/agent/bm25_code_ranker/starter
python test_bm25.py
```

**Esperado antes dos TODOs:** FAIL.


## D6-BM25-TOKENIZE

### Onde colocar (D6-BM25-TOKENIZE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/bm25.py` |
| Funcao | `tokenize` |
| Substituir | corpo sob `TODO [D6-BM25-TOKENIZE]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-BM25-TOKENIZE` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-BM25-TOKENIZE` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```python
PEDAGOGY-SOLUTION: D6-BM25-TOKENIZE
    return [x.lower() for x in re.findall(r"[A-Za-z_][A-Za-z0-9_]*",text)]
class BM25:
    def __init__(self,docs):
        # 
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-BM25-TOKENIZE`.

### Verifique
Rode o baseline; o caminho de `D6-BM25-TOKENIZE` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-BM25-TOKENIZE` PASS
- [ ] Nao alterei o teste

## D6-BM25-INDEX

### Onde colocar (D6-BM25-INDEX)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/bm25.py` |
| Funcao | `tokenize` |
| Substituir | corpo sob `TODO [D6-BM25-INDEX]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-BM25-INDEX` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-BM25-INDEX` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```python
PEDAGOGY-SOLUTION: D6-BM25-INDEX
        self.docs=docs; self.toks={p:tokenize(t) for p,t in docs.items()}; self.tf={p:Counter(ts) for p,ts in self.toks.items()}
        self.df=Counter()
        for ts in self.toks.values():
            for term in set(ts): self.df[term]+=1
        self.N=len(docs); self.avgdl=sum(map(len,self.toks.values()))/max(1,self.N)
    def rank(self,query):
        # 
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-BM25-INDEX`.

### Verifique
Rode o baseline; o caminho de `D6-BM25-INDEX` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-BM25-INDEX` PASS
- [ ] Nao alterei o teste

## D6-BM25-SCORE

### Onde colocar (D6-BM25-SCORE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/bm25.py` |
| Funcao | `__init__` |
| Substituir | corpo sob `TODO [D6-BM25-SCORE]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-BM25-SCORE` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-BM25-SCORE` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```python
PEDAGOGY-SOLUTION: D6-BM25-SCORE
        q=tokenize(query); k1=1.2; b=.75; out=[]
        for p,tfm in self.tf.items():
            dl=len(self.toks[p]); score=0.0
            for term in q:
                if not tfm[term]: continue
                df=self.df[term]; idf=math.log(1+(self.N-df+.5)/(df+.5)); tf=tfm[term]
                score += idf*(tf*(k1+1))/(tf+k1*(1-b+b*dl/self.avgdl))
            if score>0: out.append((p,score))
        return [p for p,_ in sorted(out,key=lambda x:(-x[1],x[0]))]
def reciprocal_rank(ranked,relevant):
    # 
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-BM25-SCORE`.

### Verifique
Rode o baseline; o caminho de `D6-BM25-SCORE` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-BM25-SCORE` PASS
- [ ] Nao alterei o teste

## D6-BM25-EVAL

### Onde colocar (D6-BM25-EVAL)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/bm25.py` |
| Funcao | `rank` |
| Substituir | corpo sob `TODO [D6-BM25-EVAL]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-BM25-EVAL` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-BM25-EVAL` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```python
PEDAGOGY-SOLUTION: D6-BM25-EVAL
    for i,p in enumerate(ranked,1):
        if p in relevant: return 1.0/i
    return 0.0
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-BM25-EVAL`.

### Verifique
Rode o baseline; o caminho de `D6-BM25-EVAL` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-BM25-EVAL` PASS
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
