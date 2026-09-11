# Resolucao guiada — buddy_allocator

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D7-BUDDY-INIT` | `starter/buddy_allocator.py` | `__init__` |
| `D7-BUDDY-ALLOC` | `starter/buddy_allocator.py` | `alloc` |
| `D7-BUDDY-FREE` | `starter/buddy_allocator.py` | `free` |


## Baseline

```powershell
cd days/2026-09-09/systems/buddy_allocator/starter
python test_buddy_allocator.py
```

**Esperado antes dos TODOs:** FAIL.


## D7-BUDDY-INIT

### Onde colocar (D7-BUDDY-INIT)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/buddy_allocator.py` |
| Funcao | `__init__` |
| Substituir | corpo sob `TODO [D7-BUDDY-INIT]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-BUDDY-INIT` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
        if size < 1 or (size & (size - 1)) != 0:
            raise ValueError("size power of two")
        self.size = size
        self.free = {size: [0]}
        self.used = {}
    def alloc(self, n):
        need = 1
        while need < n:
```

### Por que funciona?
Materializa o contrato numerico de `D7-BUDDY-INIT`.

### Verifique
Baseline parcial; `D7-BUDDY-INIT` PASS.

### Checkpoint
- [ ] `D7-BUDDY-INIT` PASS

## D7-BUDDY-ALLOC

### Onde colocar (D7-BUDDY-ALLOC)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/buddy_allocator.py` |
| Funcao | `alloc` |
| Substituir | corpo sob `TODO [D7-BUDDY-ALLOC]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-BUDDY-ALLOC` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
        need = 1
        while need < n:
            need <<= 1
        if need > self.size:
            return None
        order = need
        while order <= self.size and not self.free.get(order):
            order <<= 1
```

### Por que funciona?
Materializa o contrato numerico de `D7-BUDDY-ALLOC`.

### Verifique
Baseline parcial; `D7-BUDDY-ALLOC` PASS.

### Checkpoint
- [ ] `D7-BUDDY-ALLOC` PASS

## D7-BUDDY-FREE

### Onde colocar (D7-BUDDY-FREE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/buddy_allocator.py` |
| Funcao | `free` |
| Substituir | corpo sob `TODO [D7-BUDDY-FREE]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-BUDDY-FREE` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
        if idx not in self.used:
            raise KeyError(idx)
        order = self.used.pop(idx)
        while order < self.size:
            buddy = idx ^ order
            lst = self.free.setdefault(order, [])
            if buddy in lst:
                lst.remove(buddy)
```

### Por que funciona?
Materializa o contrato numerico de `D7-BUDDY-FREE`.

### Verifique
Baseline parcial; `D7-BUDDY-FREE` PASS.

### Checkpoint
- [ ] `D7-BUDDY-FREE` PASS

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
