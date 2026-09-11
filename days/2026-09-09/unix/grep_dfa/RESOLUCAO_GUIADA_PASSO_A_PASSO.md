# Resolucao guiada — grep_dfa

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D7-GREP-DFA` | `starter/grep_dfa.py` | `__init__` |
| `D7-GREP-SEARCH` | `starter/grep_dfa.py` | `contains` |
| `D7-GREP-FILE` | `starter/grep_dfa.py` | `grep_file` |


## Baseline

```powershell
cd days/2026-09-09/unix/grep_dfa/starter
python test_grep_dfa.py
```

**Esperado antes dos TODOs:** FAIL.


## D7-GREP-DFA

### Onde colocar (D7-GREP-DFA)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/grep_dfa.py` |
| Funcao | `__init__` |
| Substituir | corpo sob `TODO [D7-GREP-DFA]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-GREP-DFA` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
        self.pattern=pattern;self.accept=len(pattern);self.trans={(i,ch):i+1 for i,ch in enumerate(pattern)}
    def fullmatch_at(self,text,start):
        if self.accept==0:return True
        state=0
        for ch in text[start:]:
            key=(state,ch)
            if key not in self.trans:return False
            state=self.trans[key]
```

### Por que funciona?
Materializa o contrato numerico de `D7-GREP-DFA`.

### Verifique
Baseline parcial; `D7-GREP-DFA` PASS.

### Checkpoint
- [ ] `D7-GREP-DFA` PASS

## D7-GREP-SEARCH

### Onde colocar (D7-GREP-SEARCH)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/grep_dfa.py` |
| Funcao | `contains` |
| Substituir | corpo sob `TODO [D7-GREP-SEARCH]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-GREP-SEARCH` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
        return any(self.fullmatch_at(text,i) for i in range(len(text)+1))
def grep_file(path,pattern):
    dfa=LiteralDFA(pattern);out=[]
    with open(path,"r",encoding="utf-8",errors="replace") as f:
        for n,line in enumerate(f,1):
            if dfa.contains(line):out.append((n,line.rstrip("\n")))
    return out
```

### Por que funciona?
Materializa o contrato numerico de `D7-GREP-SEARCH`.

### Verifique
Baseline parcial; `D7-GREP-SEARCH` PASS.

### Checkpoint
- [ ] `D7-GREP-SEARCH` PASS

## D7-GREP-FILE

### Onde colocar (D7-GREP-FILE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/grep_dfa.py` |
| Funcao | `grep_file` |
| Substituir | corpo sob `TODO [D7-GREP-FILE]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-GREP-FILE` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
    dfa=LiteralDFA(pattern);out=[]
    with open(path,"r",encoding="utf-8",errors="replace") as f:
        for n,line in enumerate(f,1):
            if dfa.contains(line):out.append((n,line.rstrip("\n")))
    return out
```

### Por que funciona?
Materializa o contrato numerico de `D7-GREP-FILE`.

### Verifique
Baseline parcial; `D7-GREP-FILE` PASS.

### Checkpoint
- [ ] `D7-GREP-FILE` PASS

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
