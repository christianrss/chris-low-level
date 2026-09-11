# Resolucao guiada — tlb_page_walk

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D8-TLB-LOOKUP` | `starter/tlb_page_walk.py` | `lookup` |
| `D8-TLB-WALK` | `starter/tlb_page_walk.py` | `walk` |
| `D8-TLB-FILL` | `starter/tlb_page_walk.py` | `fill` |


## Baseline

```powershell
cd days/2026-09-10/architecture/tlb_page_walk/starter
python test_tlb_page_walk.py
```

**Esperado antes dos TODOs:** FAIL.


## D8-TLB-LOOKUP

### Onde colocar (D8-TLB-LOOKUP)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/tlb_page_walk.py` |
| Funcao | `lookup` |
| Substituir | corpo sob `TODO [D8-TLB-LOOKUP]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-TLB-LOOKUP` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-TLB-LOOKUP`.

### Escreva o codigo

```python
        vpn = vaddr // PAGE
        return self.entries.get(vpn)
    def walk(self, vaddr, page_table):
        vpn = vaddr // PAGE
        if vpn not in page_table:
            raise KeyError("fault")
        return page_table[vpn]
    def fill(self, vpn, pfn):
```

### Por que funciona?
Materializa o contrato numerico de `D8-TLB-LOOKUP`.

### Verifique
Baseline parcial; `D8-TLB-LOOKUP` PASS.

### Checkpoint
- [ ] `D8-TLB-LOOKUP` PASS

## D8-TLB-WALK

### Onde colocar (D8-TLB-WALK)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/tlb_page_walk.py` |
| Funcao | `walk` |
| Substituir | corpo sob `TODO [D8-TLB-WALK]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-TLB-WALK` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-TLB-WALK`.

### Escreva o codigo

```python
        vpn = vaddr // PAGE
        if vpn not in page_table:
            raise KeyError("fault")
        return page_table[vpn]
    def fill(self, vpn, pfn):
        self.entries[vpn] = pfn
```

### Por que funciona?
Materializa o contrato numerico de `D8-TLB-WALK`.

### Verifique
Baseline parcial; `D8-TLB-WALK` PASS.

### Checkpoint
- [ ] `D8-TLB-WALK` PASS

## D8-TLB-FILL

### Onde colocar (D8-TLB-FILL)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/tlb_page_walk.py` |
| Funcao | `fill` |
| Substituir | corpo sob `TODO [D8-TLB-FILL]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D8-TLB-FILL` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D8-TLB-FILL`.

### Escreva o codigo

```python
        self.entries[vpn] = pfn
result = handle_d8_tlb_fill(state)
assert result is not None  # D8-TLB-FILL
return result
```

### Por que funciona?
Materializa o contrato numerico de `D8-TLB-FILL`.

### Verifique
Baseline parcial; `D8-TLB-FILL` PASS.

### Checkpoint
- [ ] `D8-TLB-FILL` PASS

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
