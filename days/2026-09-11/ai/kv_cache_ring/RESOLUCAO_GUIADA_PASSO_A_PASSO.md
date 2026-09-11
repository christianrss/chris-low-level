# Resolucao guiada — kv_cache_ring

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D9-KV-WRITE` | `starter/kv_cache_ring.py` | `write` |
| `D9-KV-READ` | `starter/kv_cache_ring.py` | `read` |
| `D9-KV-WINDOW` | `starter/kv_cache_ring.py` | `window` |


## Baseline

```powershell
cd days/2026-09-11/ai/kv_cache_ring/starter
python test_kv_cache_ring.py
```

**Esperado antes dos TODOs:** FAIL.


## D9-KV-WRITE

### Onde colocar (D9-KV-WRITE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/kv_cache_ring.py` |
| Funcao | `write` |
| Substituir | corpo sob `TODO [D9-KV-WRITE]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-KV-WRITE` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-KV-WRITE`.

### Escreva o codigo

```python
        self.buf[self.pos] = item
        self.pos = (self.pos + 1) % self.cap
        self.count = min(self.cap, self.count + 1)
    def read(self, i):
        if i < 0 or i >= self.count:
            raise IndexError(i)
        start = (self.pos - self.count) % self.cap
        return self.buf[(start + i) % self.cap]
```

### Por que funciona?
Materializa o contrato numerico de `D9-KV-WRITE`.

### Verifique
Baseline parcial; `D9-KV-WRITE` PASS.

### Checkpoint
- [ ] `D9-KV-WRITE` PASS

## D9-KV-READ

### Onde colocar (D9-KV-READ)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/kv_cache_ring.py` |
| Funcao | `read` |
| Substituir | corpo sob `TODO [D9-KV-READ]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-KV-READ` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-KV-READ`.

### Escreva o codigo

```python
        if i < 0 or i >= self.count:
            raise IndexError(i)
        start = (self.pos - self.count) % self.cap
        return self.buf[(start + i) % self.cap]
    def window(self):
        return [self.read(i) for i in range(self.count)]
```

### Por que funciona?
Materializa o contrato numerico de `D9-KV-READ`.

### Verifique
Baseline parcial; `D9-KV-READ` PASS.

### Checkpoint
- [ ] `D9-KV-READ` PASS

## D9-KV-WINDOW

### Onde colocar (D9-KV-WINDOW)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/kv_cache_ring.py` |
| Funcao | `window` |
| Substituir | corpo sob `TODO [D9-KV-WINDOW]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-KV-WINDOW` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-KV-WINDOW`.

### Escreva o codigo

```python
        return [self.read(i) for i in range(self.count)]
result = handle_d9_kv_window(state)
assert result is not None  # D9-KV-WINDOW
return result
```

### Por que funciona?
Materializa o contrato numerico de `D9-KV-WINDOW`.

### Verifique
Baseline parcial; `D9-KV-WINDOW` PASS.

### Checkpoint
- [ ] `D9-KV-WINDOW` PASS

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
