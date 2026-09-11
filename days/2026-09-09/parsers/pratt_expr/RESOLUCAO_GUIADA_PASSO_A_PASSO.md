# Resolucao guiada — pratt_expr

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D7-PRATT-LEX` | `starter/pratt_expr.py` | `lex` |
| `D7-PRATT-NUD` | `starter/pratt_expr.py` | `expr` |
| `D7-PRATT-LED` | `starter/pratt_expr.py` | `expr` |


## Baseline

```powershell
cd days/2026-09-09/parsers/pratt_expr/starter
python test_pratt_expr.py
```

**Esperado antes dos TODOs:** FAIL.


## D7-PRATT-LEX

### Onde colocar (D7-PRATT-LEX)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/pratt_expr.py` |
| Funcao | `lex` |
| Substituir | corpo sob `TODO [D7-PRATT-LEX]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-PRATT-LEX` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
    out=[];i=0
    while i<len(src):
        if src[i].isspace():i+=1;continue
        m=re.match(r"(?:\d+(?:\.\d*)?|\.\d+)",src[i:])
        if m:out.append(("NUM",float(m.group())));i+=len(m.group());continue
        if src[i] in "+-*/^()":out.append((src[i],src[i]));i+=1;continue
        raise ValueError(f"bad char at {i}")
    out.append(("EOF",None));return out
```

### Por que funciona?
Materializa o contrato numerico de `D7-PRATT-LEX`.

### Verifique
Baseline parcial; `D7-PRATT-LEX` PASS.

### Checkpoint
- [ ] `D7-PRATT-LEX` PASS

## D7-PRATT-NUD

### Onde colocar (D7-PRATT-NUD)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/pratt_expr.py` |
| Funcao | `expr` |
| Substituir | corpo sob `TODO [D7-PRATT-NUD]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-PRATT-NUD` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
        typ,val=toks[pos];pos+=1
        if typ=="NUM":left=("num",val)
        elif typ=="-":left=("neg",expr(40))
        elif typ=="(":
            left=expr(0)
            if toks[pos][0]!=")":raise ValueError("missing )")
            pos+=1
        else:raise ValueError("expected expression")
```

### Por que funciona?
Materializa o contrato numerico de `D7-PRATT-NUD`.

### Verifique
Baseline parcial; `D7-PRATT-NUD` PASS.

### Checkpoint
- [ ] `D7-PRATT-NUD` PASS

## D7-PRATT-LED

### Onde colocar (D7-PRATT-LED)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/pratt_expr.py` |
| Funcao | `expr` |
| Substituir | corpo sob `TODO [D7-PRATT-LED]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-PRATT-LED` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
        bp={"+":10,"-":10,"*":20,"/":20,"^":30}
        while toks[pos][0] in bp:
            op=toks[pos][0];lbp=bp[op]
            if lbp<min_bp:break
            pos+=1;rbp=lbp if op=="^" else lbp+1;right=expr(rbp);left=("bin",op,left,right)
        return left
    ast=expr()
    if toks[pos][0]!="EOF":raise ValueError("trailing")
```

### Por que funciona?
Materializa o contrato numerico de `D7-PRATT-LED`.

### Verifique
Baseline parcial; `D7-PRATT-LED` PASS.

### Checkpoint
- [ ] `D7-PRATT-LED` PASS

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
