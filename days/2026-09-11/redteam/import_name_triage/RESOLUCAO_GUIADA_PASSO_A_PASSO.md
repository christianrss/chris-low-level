# Resolução guiada — import_name_triage

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `RT-IMP-01` | `starter/import_name_triage.py` | `normalize_name` |
| `RT-IMP-02` | `starter/import_name_triage.py` | `flag_suspicious` |
| `RT-IMP-03` | `starter/import_name_triage.py` | `triage_score` |

## Baseline

```powershell
// contexto: substitua o corpo sob o TODO
python days/2026-09-11/redteam/import_name_triage/starter/test_import_name_triage.py
// fim do corpo; preserve a assinatura
```

**Esperado:** FAIL.

## RT-IMP-01

### Onde colocar (RT-IMP-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/import_name_triage.py` |
| Função | `normalize_name` |
| Substituir | o corpo sob o comentário `TODO [RT-IMP-01]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Whitespace e vazio.

### Algoritmo / trace

strip; se vazio raise ValueError.

### Escreva o código

```python
    s = name.strip()
    if not s:
        raise ValueError("empty")
    return s
```

### Por que funciona?

Contrato limpo antes do match.

### Verifique

VirtualAlloc; ValueError em espaços.

### Código completo alinhado ao solutions/ (RT-IMP-01)

```python
PEDAGOGY-SOLUTION: RT-IMP-01
    s = name.strip()
    if not s:
        raise ValueError("empty")
    return s

def flag_suspicious(names: list[str]) -> list[str]:
    # 
```

## RT-IMP-02

### Onde colocar (RT-IMP-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/import_name_triage.py` |
| Função | `flag_suspicious` |
| Substituir | o corpo sob o comentário `TODO [RT-IMP-02]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Só nomes na tupla SUSPICIOUS.

### Algoritmo / trace

normalize e filtre.

### Escreva o código

```python
    out = []
    for n in names:
        nn = normalize_name(n)
        if nn in SUSPICIOUS:
            out.append(nn)
    return out
```

### Por que funciona?

Preserva ordem de entrada.

### Verifique

Só VirtualAlloc no Caso 2.

### Código completo alinhado ao solutions/ (RT-IMP-02)

```python
PEDAGOGY-SOLUTION: RT-IMP-02
    out = []
    for n in names:
        nn = normalize_name(n)
        if nn in SUSPICIOUS:
            out.append(nn)
    return out

def triage_score(names: list[str]) -> int:
    # 
```

## RT-IMP-03

### Onde colocar (RT-IMP-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/import_name_triage.py` |
| Função | `triage_score` |
| Substituir | o corpo sob o comentário `TODO [RT-IMP-03]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

2 hits → 20.

### Algoritmo / trace

10 * len(flag).

### Escreva o código

```python
    return 10 * len(flag_suspicious(names))
    # score
    # end
```

### Por que funciona?

Escala linear didática.

### Verifique

score==20.

### Código completo alinhado ao solutions/ (RT-IMP-03)

```python
PEDAGOGY-SOLUTION: RT-IMP-03
    return 10 * len(flag_suspicious(names))
```

## Debug

| Sintoma | Correção |
|---------|----------|
| score 2 | *10 |

## Relatório de resolução

- TODOs: [ ]
