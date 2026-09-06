# RESOLUÇÃO GUIADA — AI / Tensor entropy lab

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `AI-ENT-01` | `starter/entropy_lab.py` | `shannon_entropy` |
| `AI-ENT-02` | `starter/entropy_lab.py` | `tensor_rle_encode`, `compression_ratio_rle` |
| `AI-ENT-03` | `starter/entropy_lab.py` | `compression_ratio_gzip` |

Cada ID existe como `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` no gabarito e `PEDAGOGY-TEST: ID` em `starter/test_entropy_lab.py`.

> Trabalhe em `days/2026-09-06/ai/tensor_entropy_lab/starter/`. `solutions/` é gabarito — consulte só depois da tentativa.

> Não comece copiando `solutions/`. Rode o teste após cada TODO.

---

## AI-ENT-01 — entropia de Shannon

### 1. O problema (starter stub)

```python
def shannon_entropy(data: bytes) -> float:
    """Retorna entropia de Shannon em bits por byte.

    TODO [AI-ENT-01]
    """
    raise NotImplementedError("AI-ENT-01")
```

Com o raise, `test_uniform_entropy` nunca chega ao assert.

### 2. O algoritmo

```text
se data vazio → 0.0
counts ← Counter(data)
n ← len(data)
H ← 0
para cada count em counts.values():
  p ← count / n
  H ← H - p * log2(p)
retornar H
```

### 3. Código completo

Substitua o corpo de `shannon_entropy` (imports `Counter` e `math` já existem no arquivo):

```python
def shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    n = len(data)
    entropy = 0.0
    for count in counts.values():
        p = count / n
        entropy -= p * math.log2(p)
    return entropy
```

### 4. Por que funciona? (entenda linha a linha)

- `if not data`: convenção do lab; evita `n=0`.
- `Counter(data)`: mapa byte→frequência em uma passagem.
- `p = count / n`: probabilidade empírica; só símbolos com count>0.
- `entropy -= p * math.log2(p)`: forma estável de somar `-p log2 p` (equivale a `+= -p*log2(p)`).
- Não use `math.log` — o teste espera bits (`log2`).

### 5. Verificação parcial

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\ai\tensor_entropy_lab
python -c "import sys; sys.path.insert(0,'starter'); from entropy_lab import shannon_entropy; print(shannon_entropy(bytes([0,1,2,3]*25)))"
```

Esperado: `2.0`. Suite completa ainda falha em `AI-ENT-02`/`03`.

---

## AI-ENT-02 — RLE + compression_ratio_rle

### 1. O problema (starter stubs)

```python
def tensor_rle_encode(tensor: list[int]) -> list[tuple[int, int]]:
    """Codifica tensor 1D como lista de pares (valor, contagem).

    TODO [AI-ENT-02]
    """
    raise NotImplementedError("AI-ENT-02")


def compression_ratio_rle(tensor: list[int]) -> float:
    """Razão compressed/raw (< 1 significa ganho).

    TODO [AI-ENT-02]
    """
    raise NotImplementedError("AI-ENT-02")
```

Helpers já prontos:

```python
def tensor_rle_size_bytes(tensor: list[int]) -> int:
    pairs = tensor_rle_encode(tensor)
    return len(pairs) * 8

def raw_tensor_size_bytes(tensor: list[int]) -> int:
    return len(tensor) * 4
```

### 2. O algoritmo

```text
encode:
  se vazio → []
  current, run ← tensor[0], 1
  para value em tensor[1:]:
    se igual: run++
    senão: append (current,run); current,run ← value,1
  append (current,run)

ratio:
  raw ← raw_tensor_size_bytes(tensor)
  se raw==0 → 1.0
  senão → tensor_rle_size_bytes(tensor) / raw
```

### 3. Código completo

```python
def tensor_rle_encode(tensor: list[int]) -> list[tuple[int, int]]:
    if not tensor:
        return []
    pairs: list[tuple[int, int]] = []
    current = tensor[0]
    run = 1
    for value in tensor[1:]:
        if value == current:
            run += 1
        else:
            pairs.append((current, run))
            current = value
            run = 1
    pairs.append((current, run))
    return pairs


def compression_ratio_rle(tensor: list[int]) -> float:
    raw = raw_tensor_size_bytes(tensor)
    if raw == 0:
        return 1.0
    return tensor_rle_size_bytes(tensor) / raw
```

### 4. Por que funciona? (entenda linha a linha)

- `tensor[1:]`: processa o restante após seed do primeiro elemento.
- `pairs.append` no `else` e **depois do loop**: sem o segundo, o último run some — falha clássica.
- `* 8` / `* 4`: modelo int32 do lab (não confundir com CHRLE de 2 bytes por par).
- Ratio `< 1` = ganho; no Caso 2, `16/6000 < 0.01`.

### 5. Verificação parcial

```powershell
python -c "import sys; sys.path.insert(0,'starter'); from entropy_lab import tensor_rle_encode, compression_ratio_rle; t=[7]*1000+[3]*500; print(tensor_rle_encode(t), compression_ratio_rle(t))"
```

Esperado: `[(7, 1000), (3, 500)]` e razão `≈0.00267`.

---

## AI-ENT-03 — compression_ratio_gzip

### 1. O problema (starter stub)

```python
def compression_ratio_gzip(data: bytes) -> float:
    """Razão len(gzip(data))/len(data). Stub usa gzip padrão.

    TODO [AI-ENT-03]
    """
    raise NotImplementedError("AI-ENT-03")
```

`import gzip` já está no topo do arquivo.

### 2. O algoritmo

```text
se data vazio → 1.0
compressed ← gzip.compress(data)
retornar len(compressed) / len(data)
```

### 3. Código completo

```python
def compression_ratio_gzip(data: bytes) -> float:
    if not data:
        return 1.0
    compressed = gzip.compress(data)
    return len(compressed) / len(data)
```

### 4. Por que funciona? (entenda linha a linha)

- `gzip.compress`: one-shot RFC 1952 (header `1F 8B` + DEFLATE + trailer).
- Numerador = bytes no fio; denominador = plaintext.
- Vazio → `1.0`: mesma convenção do ratio RLE.
- No teste, `compression_ratio_rle(list(payload))` trata cada byte como int32 — por isso gzip “vence” RLE neste padrão.

### 5. Verificação completa

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\ai\tensor_entropy_lab
python starter/test_entropy_lab.py
```

Saída esperada:

```text
OK tensor entropy lab
```

Gabarito (esperado PASS):

```powershell
python solutions/test_entropy_lab.py
```

Starter sem TODOs (esperado FAIL):

```powershell
python starter/test_entropy_lab.py
```

---

## Ordem sugerida e smoke

1. `AI-ENT-01` → confira H=2.0 no REPL.
2. `AI-ENT-02` → confira pairs e ratio do tensor 1500.
3. `AI-ENT-03` → rode a suite completa.
4. Só então compare com `solutions/entropy_lab.py`.

## Relatório de resolução

### O que foi validado

- TODOs `AI-ENT-01..03` em `starter/entropy_lab.py` na ordem Shannon → RLE → gzip.
- `starter/test_entropy_lab.py` com `PEDAGOGY-TEST: AI-ENT-01/02/03` passa.
- Starter original levanta `NotImplementedError` até cada ID ser preenchido.

### Armadilhas encontradas

- `log2` vs `log`: escala em bits vs nats.
- Append final do RLE: sem ele, pairs errados no Caso 2.
- Ratio RLE usa modelo int32 (8 B/par); não misturar com CHRLE do módulo systems.
- gzip vs RLE no Caso 3: RLE em `list(bytes)` é propositalmente caro — gzip deve ganhar.

### Depuração e saída esperada

- **Depuração:** imprima `Counter`, `pairs` e `len(gzip.compress(...))` no REPL.
- **Saída esperada:** `OK tensor entropy lab`.

### Próximo passo sugerido

Refazer as três funções sem olhar esta resolução. Depois meça H e ratios em `BENCHMARK_GUIADO.md` (constante vs uniforme vs PRNG) e registre em **Resultados observados**.
