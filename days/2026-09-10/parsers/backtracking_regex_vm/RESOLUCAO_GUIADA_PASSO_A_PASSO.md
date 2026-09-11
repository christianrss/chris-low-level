# Resolucao guiada — backtracking_regex_vm

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D8-RE-CHAR` | `starter/backtracking_regex_vm.py` | `match` |
| `D8-RE-STAR` | `starter/backtracking_regex_vm.py` | `match` |
| `D8-RE-MATCH` | `starter/backtracking_regex_vm.py` | `match` |


## Baseline

```powershell
cd days/2026-09-10/parsers/backtracking_regex_vm/starter
python test_backtracking_regex_vm.py
```

**Esperado antes dos TODOs:** FAIL.


## D8-RE-CHAR

### Onde colocar (D8-RE-CHAR)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/backtracking_regex_vm.py` |
| Funcao | `match` |
| Substituir | corpo sob `TODO [D8-RE-CHAR]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-RE-CHAR` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-RE-CHAR`.

### Escreva o codigo

```python
        if op[0] == "CHAR":
            if i < len(text) and text[i] == op[1]:
                return run(pc + 1, i + 1)
            return False
        if op[0] == "STAR":
            j = i
            ch = op[1]
            while j < len(text) and text[j] == ch:
```

### Por que funciona?
Materializa o contrato numerico de `D8-RE-CHAR`.

### Verifique
Baseline parcial; `D8-RE-CHAR` PASS.

### Checkpoint
- [ ] `D8-RE-CHAR` PASS

## D8-RE-STAR

### Onde colocar (D8-RE-STAR)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/backtracking_regex_vm.py` |
| Funcao | `match` |
| Substituir | corpo sob `TODO [D8-RE-STAR]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-RE-STAR` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-RE-STAR`.

### Escreva o codigo

```python
        if op[0] == "STAR":
            j = i
            ch = op[1]
            while j < len(text) and text[j] == ch:
                j += 1
            while j >= i:
                if run(pc + 1, j):
                    return True
```

### Por que funciona?
Materializa o contrato numerico de `D8-RE-STAR`.

### Verifique
Baseline parcial; `D8-RE-STAR` PASS.

### Checkpoint
- [ ] `D8-RE-STAR` PASS

## D8-RE-MATCH

### Onde colocar (D8-RE-MATCH)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/backtracking_regex_vm.py` |
| Funcao | `match` |
| Substituir | corpo sob `TODO [D8-RE-MATCH]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-RE-MATCH` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-RE-MATCH`.

### Escreva o codigo

```python
    def run(pc, i):
        if pc >= len(code):
            return i == len(text)
        op = code[pc]
        if op[0] == "CHAR":
            if i < len(text) and text[i] == op[1]:
                return run(pc + 1, i + 1)
            return False
```

### Por que funciona?
Materializa o contrato numerico de `D8-RE-MATCH`.

### Verifique
Baseline parcial; `D8-RE-MATCH` PASS.

### Checkpoint
- [ ] `D8-RE-MATCH` PASS

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
