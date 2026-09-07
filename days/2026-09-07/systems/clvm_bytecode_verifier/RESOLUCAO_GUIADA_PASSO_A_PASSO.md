# Resolucao guiada — verifier

## Mapa exato starter → resolução

| ID | Arquivo | Ancora |
|----|---------|--------|
| `CLVM-VFY-BRANCH-01` | `starter/verify_clvm.py` | `TODO [CLVM-VFY-BRANCH-01]` |
| `CLVM-VFY-STACK-01` | idem | `TODO [CLVM-VFY-STACK-01]` |

---

## CLVM-VFY-BRANCH-01

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/verify_clvm.py` |
| **Função / âncora** | apos `target = ...` |
| **Substituir** | `raise NotImplementedError("TODO [CLVM-VFY-BRANCH-01]...")` |
| **Não mexer** | FNV header |

### Escreva o codigo

```python
if not (0 <= target <= len(code)):
    errors.append(f"branch target OOB from {start} -> {target}")
```

### Por que funciona

Salto fora do code nunca e valido em v1.

### Verifique

Esperado: sem raise; continue o loop. Depure com JMP sintetico OOB.

---

## CLVM-VFY-STACK-01

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/verify_clvm.py` |
| **Função / âncora** | final de `verify` |
| **Substituir** | raise STACK |
| **Não mexer** | tabela `STACK_EFFECT` |

### Escreva o codigo

Copie o walk de `solutions/verify_clvm.py`.

### Por que funciona

Simula profundidade sem efeitos colaterais.

### Verifique

Esperado: `ok.clvm` sem erros. Depure depth em PRINT.

---

## Relatório de resolução

- TODOs: ___
- Testes / esperado PASS solutions: ___
- Depuracao usada: ___
- Duvidas: ___

Checklist: confirme esperado PASS; depure mensagens INVALID no stderr.
Checklist: rode fixtures ok e bad_checksum.
Checklist: compare com solutions/verify_clvm.py apos tentar.
Checklist: nao altere Dia 01.
Checklist: porte melhorias ao chris-vm verify_clvm.py.

Fim da resolucao guiada do verifier (N2).

Proximo: N3 operador %% no chris-vm, depois N4 v2.
