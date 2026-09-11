# Resolucao guiada — procfs_module_lab

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D8-PROC-LIST` | `starter/procfs_module_lab.py` | `list` |
| `D8-PROC-READ` | `starter/procfs_module_lab.py` | `read` |
| `D8-PROC-WRITE` | `starter/procfs_module_lab.py` | `write` |


## Baseline

```powershell
cd days/2026-09-10/linux/procfs_module_lab/starter
python test_procfs_module_lab.py
```

**Esperado antes dos TODOs:** FAIL.


## D8-PROC-LIST

### Onde colocar (D8-PROC-LIST)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/procfs_module_lab.py` |
| Funcao | `list` |
| Substituir | corpo sob `TODO [D8-PROC-LIST]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-PROC-LIST` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-PROC-LIST`.

### Escreva o codigo

```python
        return sorted(self.entries)
result = handle_d8_proc_list(state)
assert result is not None  # D8-PROC-LIST
return result
```

### Por que funciona?
Materializa o contrato numerico de `D8-PROC-LIST`.

### Verifique
Baseline parcial; `D8-PROC-LIST` PASS.

### Checkpoint
- [ ] `D8-PROC-LIST` PASS

## D8-PROC-READ

### Onde colocar (D8-PROC-READ)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/procfs_module_lab.py` |
| Funcao | `read` |
| Substituir | corpo sob `TODO [D8-PROC-READ]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-PROC-READ` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-PROC-READ`.

### Escreva o codigo

```python
        if name not in self.entries:
            raise KeyError(name)
        return self.entries[name]
    def list(self):
        return sorted(self.entries)
```

### Por que funciona?
Materializa o contrato numerico de `D8-PROC-READ`.

### Verifique
Baseline parcial; `D8-PROC-READ` PASS.

### Checkpoint
- [ ] `D8-PROC-READ` PASS

## D8-PROC-WRITE

### Onde colocar (D8-PROC-WRITE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/procfs_module_lab.py` |
| Funcao | `write` |
| Substituir | corpo sob `TODO [D8-PROC-WRITE]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-PROC-WRITE` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-PROC-WRITE`.

### Escreva o codigo

```python
        self.entries[name] = str(data)
    def read(self, name):
        if name not in self.entries:
            raise KeyError(name)
        return self.entries[name]
    def list(self):
        return sorted(self.entries)
```

### Por que funciona?
Materializa o contrato numerico de `D8-PROC-WRITE`.

### Verifique
Baseline parcial; `D8-PROC-WRITE` PASS.

### Checkpoint
- [ ] `D8-PROC-WRITE` PASS

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
