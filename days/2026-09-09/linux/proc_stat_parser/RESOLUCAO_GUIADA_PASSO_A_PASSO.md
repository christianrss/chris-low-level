# Resolucao guiada — proc_stat_parser

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D7-PROC-PREFIX` | `starter/proc_stat_parser.py` | `parse_stat` |
| `D7-PROC-FIELDS` | `starter/proc_stat_parser.py` | `parse_stat` |
| `D7-PROC-SELF` | `starter/proc_stat_parser.py` | `read_self` |


## Baseline

```powershell
cd days/2026-09-09/linux/proc_stat_parser/starter
python test_proc_stat_parser.py
```

**Esperado antes dos TODOs:** FAIL.


## D7-PROC-PREFIX

### Onde colocar (D7-PROC-PREFIX)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/proc_stat_parser.py` |
| Funcao | `parse_stat` |
| Substituir | corpo sob `TODO [D7-PROC-PREFIX]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-PROC-PREFIX` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
    lp = text.find("(")
    rp = text.rfind(")")
    if lp < 0 or rp < lp:
        raise ValueError("format")
    pid = int(text[:lp].strip())
    comm = text[lp+1:rp]
    rest = text[rp+2:].split()
    if len(rest) < 20:
```

### Por que funciona?
Materializa o contrato numerico de `D7-PROC-PREFIX`.

### Verifique
Baseline parcial; `D7-PROC-PREFIX` PASS.

### Checkpoint
- [ ] `D7-PROC-PREFIX` PASS

## D7-PROC-FIELDS

### Onde colocar (D7-PROC-FIELDS)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/proc_stat_parser.py` |
| Funcao | `parse_stat` |
| Substituir | corpo sob `TODO [D7-PROC-FIELDS]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-PROC-FIELDS` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
    rest = text[rp+2:].split()
    if len(rest) < 20:
        raise ValueError("truncated")
    return {
        "pid": pid,
        "comm": comm,
        "state": rest[0],
        "ppid": int(rest[1]),
```

### Por que funciona?
Materializa o contrato numerico de `D7-PROC-FIELDS`.

### Verifique
Baseline parcial; `D7-PROC-FIELDS` PASS.

### Checkpoint
- [ ] `D7-PROC-FIELDS` PASS

## D7-PROC-SELF

### Onde colocar (D7-PROC-SELF)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/proc_stat_parser.py` |
| Funcao | `read_self` |
| Substituir | corpo sob `TODO [D7-PROC-SELF]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-PROC-SELF` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
    fixture = "1 (init) S 0 0 0 0 0 0 0 0 0 0 0 10 20 0 0 0 0 1 0 100"
    return parse_stat(fixture)
result = handle_d7_proc_self(state)
assert result is not None  # D7-PROC-SELF
return result
```

### Por que funciona?
Materializa o contrato numerico de `D7-PROC-SELF`.

### Verifique
Baseline parcial; `D7-PROC-SELF` PASS.

### Checkpoint
- [ ] `D7-PROC-SELF` PASS

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
