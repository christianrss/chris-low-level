# Resolucao guiada — dwarf_line_program

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D9-DWARF-ULEB` | `starter/dwarf_line_program.py` | `read_uleb` |
| `D9-DWARF-SLEB` | `starter/dwarf_line_program.py` | `read_sleb` |
| `D9-DWARF-VM` | `starter/dwarf_line_program.py` | `run_line_program` |


## Baseline

```powershell
cd days/2026-09-11/redteam/dwarf_line_program/starter
python test_dwarf_line_program.py
```

**Esperado antes dos TODOs:** FAIL.


## D9-DWARF-ULEB

### Onde colocar (D9-DWARF-ULEB)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/dwarf_line_program.py` |
| Funcao | `read_uleb` |
| Substituir | corpo sob `TODO [D9-DWARF-ULEB]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-DWARF-ULEB` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-DWARF-ULEB`.

### Escreva o codigo

```python
    value=0;shift=0
    for _ in range(10):
        if off>=len(data): raise ValueError("truncated uleb")
        b=data[off];off+=1;value|=(b&0x7f)<<shift
        if not b&0x80:return value,off
        shift+=7
    raise ValueError("uleb too long")
def read_sleb(data,off):
```

### Por que funciona?
Materializa o contrato numerico de `D9-DWARF-ULEB`.

### Verifique
Baseline parcial; `D9-DWARF-ULEB` PASS.

### Checkpoint
- [ ] `D9-DWARF-ULEB` PASS

## D9-DWARF-SLEB

### Onde colocar (D9-DWARF-SLEB)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/dwarf_line_program.py` |
| Funcao | `read_sleb` |
| Substituir | corpo sob `TODO [D9-DWARF-SLEB]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-DWARF-SLEB` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-DWARF-SLEB`.

### Escreva o codigo

```python
    value=0;shift=0
    for _ in range(10):
        if off>=len(data): raise ValueError("truncated sleb")
        b=data[off];off+=1;value|=(b&0x7f)<<shift;shift+=7
        if not b&0x80:
            if shift<64 and b&0x40:value|=-(1<<shift)
            return value,off
    raise ValueError("sleb too long")
```

### Por que funciona?
Materializa o contrato numerico de `D9-DWARF-SLEB`.

### Verifique
Baseline parcial; `D9-DWARF-SLEB` PASS.

### Checkpoint
- [ ] `D9-DWARF-SLEB` PASS

## D9-DWARF-VM

### Onde colocar (D9-DWARF-VM)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/dwarf_line_program.py` |
| Funcao | `run_line_program` |
| Substituir | corpo sob `TODO [D9-DWARF-VM]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-DWARF-VM` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-DWARF-VM`.

### Escreva o codigo

```python
    pc=0;address=0;line=1;file=1;rows=[]
    while pc<len(data):
        op=data[pc];pc+=1
        if op==0:
            if pc!=len(data): raise ValueError("bytes after end")
            return rows
        if op==1:
            d,pc=read_uleb(data,pc); address+=d
```

### Por que funciona?
Materializa o contrato numerico de `D9-DWARF-VM`.

### Verifique
Baseline parcial; `D9-DWARF-VM` PASS.

### Checkpoint
- [ ] `D9-DWARF-VM` PASS

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
