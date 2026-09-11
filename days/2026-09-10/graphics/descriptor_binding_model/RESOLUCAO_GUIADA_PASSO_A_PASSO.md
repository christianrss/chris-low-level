# Resolucao guiada — descriptor_binding_model

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D8-GFX-BIND` | `starter/descriptor_binding_model.py` | `bind` |
| `D8-GFX-SET` | `starter/descriptor_binding_model.py` | `validate_set` |
| `D8-GFX-LAYOUT` | `starter/descriptor_binding_model.py` | `layout_of` |


## Baseline

```powershell
cd days/2026-09-10/graphics/descriptor_binding_model/starter
python test_descriptor_binding_model.py
```

**Esperado antes dos TODOs:** FAIL.


## D8-GFX-BIND

### Onde colocar (D8-GFX-BIND)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/descriptor_binding_model.py` |
| Funcao | `bind` |
| Substituir | corpo sob `TODO [D8-GFX-BIND]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-GFX-BIND` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-GFX-BIND`.

### Escreva o codigo

```python
    if binding not in layout["bindings"]:
        raise KeyError(binding)
    return {"set": set_id, "binding": binding, "resource": resource}
def validate_set(layout, set_id, table):
    for b in layout["bindings"]:
        if b not in table:
            raise KeyError(f"missing {b}")
    return True
```

### Por que funciona?
Materializa o contrato numerico de `D8-GFX-BIND`.

### Verifique
Baseline parcial; `D8-GFX-BIND` PASS.

### Checkpoint
- [ ] `D8-GFX-BIND` PASS

## D8-GFX-SET

### Onde colocar (D8-GFX-SET)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/descriptor_binding_model.py` |
| Funcao | `validate_set` |
| Substituir | corpo sob `TODO [D8-GFX-SET]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-GFX-SET` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-GFX-SET`.

### Escreva o codigo

```python
    for b in layout["bindings"]:
        if b not in table:
            raise KeyError(f"missing {b}")
    return True
```

### Por que funciona?
Materializa o contrato numerico de `D8-GFX-SET`.

### Verifique
Baseline parcial; `D8-GFX-SET` PASS.

### Checkpoint
- [ ] `D8-GFX-SET` PASS

## D8-GFX-LAYOUT

### Onde colocar (D8-GFX-LAYOUT)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/descriptor_binding_model.py` |
| Funcao | `layout_of` |
| Substituir | corpo sob `TODO [D8-GFX-LAYOUT]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-GFX-LAYOUT` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-GFX-LAYOUT`.

### Escreva o codigo

```python
    return {"bindings": list(bindings)}
def bind(layout, set_id, binding, resource):
    if binding not in layout["bindings"]:
        raise KeyError(binding)
    return {"set": set_id, "binding": binding, "resource": resource}
def validate_set(layout, set_id, table):
    for b in layout["bindings"]:
        if b not in table:
```

### Por que funciona?
Materializa o contrato numerico de `D8-GFX-LAYOUT`.

### Verifique
Baseline parcial; `D8-GFX-LAYOUT` PASS.

### Checkpoint
- [ ] `D8-GFX-LAYOUT` PASS

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
