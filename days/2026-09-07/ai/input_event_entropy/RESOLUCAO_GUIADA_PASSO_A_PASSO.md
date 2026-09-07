# Resolução guiada — input_event_entropy

## Mapa exato starter → resolução

| TODO ID | Arquivo starter | Função | Substituir |
|---------|-----------------|--------|------------|
| `AI-EVT-ENT-01` | `starter/input_entropy.py` | `shannon_entropy_events` | stub TODO |
| `AI-EVT-RLE-02` | `starter/input_entropy.py` | `event_rle_encode` | stub TODO |
| `AI-EVT-RATIO-03` | `starter/input_entropy.py` | `compression_ratio_gzip_events` | stub TODO |

## Baseline

```powershell
cd days/2026-09-07/ai/input_event_entropy/starter
python test_input_entropy.py
```

**Esperado:** FAIL até implementar os três TODOs.

## Relatório de resolução

## AI-EVT-ENT-01

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/input_entropy.py` |
| Função | `shannon_entropy_events` |

### 1. O problema

Medir entropia do stream bruto de eventos antes de modelar features.

### Escreva o código

```python
def shannon_entropy_events(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    n = len(data)
    ent = 0.0
    for c in counts.values():
        p = c / n
        ent -= p * math.log2(p)
    return ent
```

### Por que funciona?

H bits/byte limita compressão sem memória — stream repetitivo → H≈0.

### Verifique

Caso 1: 48 bytes iguais → entropia < 0.01.

### Debug

| Sintoma | Ação |
|---------|------|
| H > 8 | usar log2, não ln |

---

## AI-EVT-RLE-02

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/input_entropy.py` |
| Função | `event_rle_encode` |

### 1. O problema

Tecla segurada gera runs no campo `code` — RLE expõe estrutura.

### Escreva o código

```python
def event_rle_encode(codes: list[int]) -> list[tuple[int, int]]:
    if not codes:
        return []
    out: list[tuple[int, int]] = []
    cur, run = codes[0], 1
    for x in codes[1:]:
        if x == cur:
            run += 1
        else:
            out.append((cur, run))
            cur, run = x, 1
    out.append((cur, run))
    return out
```

### Por que funciona?

Runs consecutivos viram pares (valor, contagem) em O(n).

### Verifique

Caso 2: `[1,1,2]` → `[(1,2),(2,1)]`.

---

## AI-EVT-RATIO-03

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/input_entropy.py` |
| Função | `compression_ratio_gzip_events` |

### 1. O problema

Comparar gzip com raw dá baseline de compressibilidade real.

### Escreva o código

```python
def compression_ratio_gzip_events(data: bytes) -> float:
    if not data:
        return 1.0
    return len(gzip.compress(data)) / len(data)
```

### Por que funciona?

gzip explora repetição além da entropia marginal.

### Verifique

Caso 3: dados repetitivos → ratio < 0.5.

### Resultado esperado

`python test_input_entropy.py` imprime `OK input_entropy`.
