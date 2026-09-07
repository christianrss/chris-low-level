# Resolução guiada — KV cache circular

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `D5-KV-APPEND` | `starter/kv_cache.py` | `append` |
| `D5-KV-WINDOW` | `starter/kv_cache.py` | `window` |
| `D5-KV-RESET` | `starter/kv_cache.py` | `reset` |

Cada ID existe como `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` no gabarito e `PEDAGOGY-TEST: ID` em `starter/test_kv_cache.py`.

> Trabalhe em `days/2026-09-07/ai/kv_cache_ring/starter/`. O gabarito em `solutions/` é só para conferência depois da tentativa honesta.

## Baseline

Antes de editar, confirme que o starter falha nos TODOs:

```powershell
cd days/2026-09-07/ai/kv_cache_ring
python starter/test_kv_cache.py
```

**Esperado:** falha no primeiro `append` (corpo vazio / `pass`) ou assert de `next_position`.

---

## D5-KV-APPEND — gravar K/V e tag lógico

### O problema

Sem implementação, `append` não grava nada e `next_position` permanece 0. O teste faz quatro appends e espera `next_position==4`.

Stub atual:

```python
def append(self, position, key, value):
    # TODO [D5-KV-APPEND]: grave K/V e tag lógico no slot circular.
    pass
```

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/kv_cache.py` |
| **Função / âncora** | `append` — comentário `TODO [D5-KV-APPEND]` |
| **Substituir** | o corpo `pass` inteiro |
| **Não mexer** | `__init__`, `window`, `reset` neste passo |

### Código completo

```python
def append(self, position, key, value):
    if position != self.next_position:
        raise ValueError("non-contiguous position")
    slot = position % self.capacity
    self.keys[slot] = key
    self.values[slot] = value
    self.positions[slot] = position
    self.next_position += 1
```

### Por que funciona?

- `position != self.next_position` garante append autoregressivo — sem buracos artificiais.
- `slot = position % capacity` mapeia posição lógica ao ring físico.
- Escrever K, V e tag juntos evita estado onde valor novo coexiste com tag velho.
- `next_position += 1` separa contagem lógica total de índice físico.

### Verificação parcial

```powershell
python -c "import sys; sys.path.insert(0,'starter'); from kv_cache import KVCacheRing; c=KVCacheRing(3); c.append(0,'a','b'); print(c.next_position, c.positions)"
```

**Esperado:** `1 [0, None, None]`. Teste completo ainda falha em `window`.

---

## D5-KV-WINDOW — janela com detecção de eviction

### O problema

Com append ok, `window` retorna `[]` sempre. O teste espera `[("k1","v1"),("k2","v2"),("k3","v3")]` para `(1,4)` e `KeyError` ao pedir posição 0 evictada.

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/kv_cache.py` |
| **Função / âncora** | `window` — comentário `TODO [D5-KV-WINDOW]` |
| **Substituir** | o `return []` stub |
| **Não mexer** | lógica de `append` já passando |

### Código completo

```python
def window(self, start, end):
    if start < 0 or end < start or end > self.next_position:
        raise ValueError("invalid window")
    out = []
    for p in range(start, end):
        slot = p % self.capacity
        if self.positions[slot] != p:
            raise KeyError(f"position {p} was evicted")
        out.append((self.keys[slot], self.values[slot]))
    return out
```

### Por que funciona?

- Bounds em `start/end/next_position` impedem ler além do que foi commitado.
- `positions[slot] != p` detecta slot reutilizado por posição mais nova — stale read vira erro explícito.
- Loop em ordem de `p` preserva ordem temporal na saída.

### Verificação parcial

Após quatro appends em capacity=3:

```powershell
python -c "import sys; sys.path.insert(0,'starter'); from kv_cache import KVCacheRing; c=KVCacheRing(3); [c.append(p,f'k{p}',f'v{p}') for p in range(4)]; print(c.window(1,4))"
```

**Esperado:** `[('k1', 'v1'), ('k2', 'v2'), ('k3', 'v3')]`.

---

## D5-KV-RESET — limpar ownership e cursor

### O problema

Sem reset real, tags antigas sobrevivem e o teste falha em `c.reset(); assert c.next_position==0 and c.positions==[None]*3`.

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/kv_cache.py` |
| **Função / âncora** | `reset` — comentário `TODO [D5-KV-RESET]` |
| **Substituir** | o corpo `pass` |
| **Não mexer** | `capacity` — só limpe estado mutável |

### Código completo

```python
def reset(self):
    self.positions = [None] * self.capacity
    self.keys = [None] * self.capacity
    self.values = [None] * self.capacity
    self.next_position = 0
```

### Por que funciona?

- Três listas zeradas removem tags e pares K/V residuais.
- `next_position = 0` reinicia sequência lógica para nova “conversa”.
- Reatribuir listas (em vez de mutar in-place parcial) garante igualdade `== [None]*capacity` do teste.

### Verificação final

```powershell
python starter/test_kv_cache.py
```

**Esperado:** `chris-kv-cache tests passed`.

---

## Debug

| Sintoma | Causa típica | Correção |
|---------|--------------|----------|
| `window(0,1)` retorna dado errado | leitura sem comparar tag | exija `positions[slot]==p` |
| `next_position` não avança | esqueceu incremento | `+= 1` após gravar |
| reset passa parcialmente | só zerou cursor | limpe `keys`, `values`, `positions` |
| `ValueError non-contiguous` inesperado | append fora de ordem | use `range(n)` contíguo |

Trace útil: após cada append, imprima `(position, slot, positions[slot], next_position)`.

---

## Relatório de resolução

Preencha após passar no teste:

1. **Capacidade usada no trace manual:** _____
2. **Posição lógica evictada primeiro (capacity=3, 4 appends):** _____
3. **Por que `positions[slot]` é necessário além de `keys[slot]`?** _____
4. **Tempo gasto por TODO:** APPEND ___ / WINDOW ___ / RESET ___
5. **Bug que mais demorou:** _____
