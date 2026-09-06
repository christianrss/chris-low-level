# RESOLUÇÃO GUIADA — Red Team / Compressed blob triage

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `RT-COMP-01` | `starter/blob_triage.py` | `detect_compression_magic` |
| `RT-COMP-02` | `starter/blob_triage.py` | `validate_size_limits` |
| `RT-COMP-03` | `starter/blob_triage.py` | `extract_ascii_strings` |

Helper já pronto no starter: `safe_inflate_preview` (usa magic + `gzip`/`zlib`).

Cada ID existe como `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` no gabarito e `PEDAGOGY-TEST: ID` em `starter/test_blob_triage.py`.

> Trabalhe em `days/2026-09-06/redteam/compressed_blob_triage/starter/`. `solutions/` só depois da tentativa.

---

## RT-COMP-01 — detect_compression_magic

### 1. O problema (starter stub)

```python
def detect_compression_magic(data: bytes) -> CompressionKind:
    """Detecta gzip (1F 8B) ou zlib (78 9C / 78 DA).

    TODO [RT-COMP-01]
    """
    raise NotImplementedError("RT-COMP-01")
```

Sem magic, os testes de gzip/zlib falham imediatamente; `validate_size_limits` também depende desta função.

### 2. O algoritmo

```text
se len(data) < 2 → "unknown"
se data[0]==0x1F e data[1]==0x8B → "gzip"
se data[0]==0x78 e data[1] in (0x01, 0x5E, 0x9C, 0xDA) → "zlib"
senão → "unknown"
```

### 3. Código completo

```python
def detect_compression_magic(data: bytes) -> CompressionKind:
    if len(data) < 2:
        return "unknown"
    if data[0] == 0x1F and data[1] == 0x8B:
        return "gzip"
    if data[0] == 0x78 and data[1] in (0x01, 0x5E, 0x9C, 0xDA):
        return "zlib"
    return "unknown"
```

### 4. Por que funciona? (entenda linha a linha)

- `len < 2`: guarda contra IndexError em buffer vazio/curto.
- `1F 8B`: assinatura gzip fixa (RFC 1952).
- Tupla de FLG zlib: cobre store/fast/default/best usados por `zlib.compress` nos níveis comuns; o teste oficial espera `78 9c`.
- `"unknown"` explícito: Literal do módulo — não retorne `None`.

### 5. Verificação parcial

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\redteam\compressed_blob_triage
python -c "import gzip,zlib,sys; sys.path.insert(0,'starter'); from blob_triage import detect_compression_magic; print(detect_compression_magic(gzip.compress(b'hi')), detect_compression_magic(zlib.compress(b'hi')))"
```

Esperado: `gzip zlib`.

---

## RT-COMP-02 — validate_size_limits

### 1. O problema (starter stub)

```python
def validate_size_limits(
    data: bytes,
    max_compressed: int,
    max_uncompressed: int,
) -> bool:
    """Retorna True se tamanhos estão dentro dos limites seguros.

    TODO [RT-COMP-02]
    """
    raise NotImplementedError("RT-COMP-02")
```

### 2. O algoritmo

```text
se len(data) > max_compressed → False
kind ← detect_compression_magic(data)
se kind == "unknown" → (len(data) <= max_uncompressed)
tentar:
  preview ← safe_inflate_preview(data, max_out=max_uncompressed+1)
exceto qualquer Exception → False
retornar len(preview) <= max_uncompressed
```

### 3. Código completo

```python
def validate_size_limits(
    data: bytes,
    max_compressed: int,
    max_uncompressed: int,
) -> bool:
    if len(data) > max_compressed:
        return False
    kind = detect_compression_magic(data)
    if kind == "unknown":
        return len(data) <= max_uncompressed
    try:
        preview = safe_inflate_preview(data, max_out=max_uncompressed + 1)
    except Exception:
        return False
    return len(preview) <= max_uncompressed
```

### 4. Por que funciona? (entenda linha a linha)

- Primeiro corte: compressed oversized — barato, sem CPU de inflate.
- `unknown`: não há inflate seguro conhecido; trata o buffer como “já é o dado” sob o teto uncompressed.
- `max_out=max_uncompressed+1`: o helper rejeita se `len(out) > max_out`; depois ainda exigimos `<= max_uncompressed`. Assim um inflate exatamente no limite passa; um byte a mais falha no helper ou na comparação.
- `except Exception`: blob corrompido → `False`, não crash do triager.
- Depende de `RT-COMP-01` e do `safe_inflate_preview` já presente **abaixo** no mesmo arquivo (resolução em tempo de chamada — ok em Python).

### 5. Verificação parcial

```powershell
python -c "import gzip,sys; sys.path.insert(0,'starter'); from blob_triage import validate_size_limits; big=gzip.compress(b'x'*200000); print(validate_size_limits(big,100000,50000)); print(validate_size_limits(gzip.compress(b'ok'),10000,10000))"
```

Esperado: `False` depois `True`.

---

## RT-COMP-03 — extract_ascii_strings

### 1. O problema (starter stub)

```python
def extract_ascii_strings(data: bytes, min_len: int = 4) -> list[str]:
    """Extrai strings ASCII imprimíveis do payload.

    TODO [RT-COMP-03]
    """
    raise NotImplementedError("RT-COMP-03")
```

`import re` já está no starter.

### 2. O algoritmo

```text
pattern ← bytes regex [\x20-\x7e]{min_len,}
retornar [match.decode("ascii") for match in findall(pattern, data)]
```

### 3. Código completo

```python
def extract_ascii_strings(data: bytes, min_len: int = 4) -> list[str]:
    pattern = rb"[\x20-\x7e]{%d,}" % min_len
    return [m.decode("ascii") for m in re.findall(pattern, data)]
```

### 4. Por que funciona? (entenda linha a linha)

- `\x20-\x7e`: espaço até til — inclui `=`, `_`, dígitos (necessário para `SECRET_KEY=abc123`).
- `% min_len`: quantificador dinâmico; não hardcode `{4,}`.
- `findall` em `bytes` → lista de `bytes`; `decode("ascii")` seguro nesse range.
- Não filtra gzip interno — o teste coloca a string **antes** do blob gzipado.

### 5. Verificação completa

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\redteam\compressed_blob_triage
python starter/test_blob_triage.py
```

Saída esperada:

```text
OK blob triage
```

Gabarito:

```powershell
python solutions/test_blob_triage.py
```

---

## Ordem sugerida

1. Magic (`RT-COMP-01`).
2. Limites (`RT-COMP-02`) — precisa do magic.
3. Strings (`RT-COMP-03`) — independente.
4. Suite completa; só então `solutions/blob_triage.py`.

## Relatório de resolução

### O que foi validado

- TODOs `RT-COMP-01..03` em `starter/blob_triage.py`.
- Testes `PEDAGOGY-TEST` gzip, zlib, limites e strings passam.
- Starter original falha com `NotImplementedError` até preenchimento.

### Armadilhas encontradas

- Zlib: incluir `01/5E/9C/DA`, não só `9C`.
- Limites: compressed pequeno com uncompressed enorme deve falhar.
- Strings: charset imprimível completo, não só alfanumérico.
- `safe_inflate_preview` já no starter — não reimplementar inflate dentro de `validate` além de chamá-lo.

### Depuração e saída esperada

- **Depuração:** `print(payload[:4].hex())`; confira `1f8b` / `789c`.
- **Saída esperada:** `OK blob triage`.

### Próximo passo sugerido

Refazer sem olhar o gabarito. Em `BENCHMARK_GUIADO.md`, compare tempo de magic-only vs validate com inflate em blobs repetitivos vs aleatórios.
