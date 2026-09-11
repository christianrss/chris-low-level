# Resolucao guiada — transactional_patcher

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D8-PATCH-BEGIN` | `starter/transactional_patcher.py` | `begin` |
| `D8-PATCH-APPLY` | `starter/transactional_patcher.py` | `apply` |
| `D8-PATCH-COMMIT` | `starter/transactional_patcher.py` | `commit` |


## Baseline

```powershell
cd days/2026-09-10/agent/transactional_patcher/starter
python test_transactional_patcher.py
```

**Esperado antes dos TODOs:** FAIL.


## D8-PATCH-BEGIN

### Onde colocar (D8-PATCH-BEGIN)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/transactional_patcher.py` |
| Funcao | `begin` |
| Substituir | corpo sob `TODO [D8-PATCH-BEGIN]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-PATCH-BEGIN` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-PATCH-BEGIN`.

### Escreva o codigo

```python
        self.snap = self.text
    def apply(self, start, end, repl):
        if self.snap is None:
            raise RuntimeError("no tx")
        self.text = self.text[:start] + repl + self.text[end:]
    def commit(self):
        if self.snap is None:
            raise RuntimeError("no tx")
```

### Por que funciona?
Materializa o contrato numerico de `D8-PATCH-BEGIN`.

### Verifique
Baseline parcial; `D8-PATCH-BEGIN` PASS.

### Checkpoint
- [ ] `D8-PATCH-BEGIN` PASS

## D8-PATCH-APPLY

### Onde colocar (D8-PATCH-APPLY)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/transactional_patcher.py` |
| Funcao | `apply` |
| Substituir | corpo sob `TODO [D8-PATCH-APPLY]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-PATCH-APPLY` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-PATCH-APPLY`.

### Escreva o codigo

```python
        if self.snap is None:
            raise RuntimeError("no tx")
        self.text = self.text[:start] + repl + self.text[end:]
    def commit(self):
        if self.snap is None:
            raise RuntimeError("no tx")
        self.snap = None
    def rollback(self):
```

### Por que funciona?
Materializa o contrato numerico de `D8-PATCH-APPLY`.

### Verifique
Baseline parcial; `D8-PATCH-APPLY` PASS.

### Checkpoint
- [ ] `D8-PATCH-APPLY` PASS

## D8-PATCH-COMMIT

### Onde colocar (D8-PATCH-COMMIT)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/transactional_patcher.py` |
| Funcao | `commit` |
| Substituir | corpo sob `TODO [D8-PATCH-COMMIT]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-PATCH-COMMIT` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-PATCH-COMMIT`.

### Escreva o codigo

```python
        if self.snap is None:
            raise RuntimeError("no tx")
        self.snap = None
    def rollback(self):
        if self.snap is None:
            raise RuntimeError("no tx")
        self.text = self.snap
        self.snap = None
```

### Por que funciona?
Materializa o contrato numerico de `D8-PATCH-COMMIT`.

### Verifique
Baseline parcial; `D8-PATCH-COMMIT` PASS.

### Checkpoint
- [ ] `D8-PATCH-COMMIT` PASS

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
