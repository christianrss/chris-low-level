# Resolucao guiada — wasm_binary_triage

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D6-WASM-ULEB` | `starter/wasm_triage.py` | `read_u32_leb` |
| `D6-WASM-HEADER` | `starter/wasm_triage.py` | `read_u32_leb` |
| `D6-WASM-SECTIONS` | `starter/wasm_triage.py` | `parse_sections` |


## Baseline

```powershell
cd days/2026-09-08/redteam/wasm_binary_triage/starter
python test_wasm_triage.py
```

**Esperado antes dos TODOs:** FAIL.


## D6-WASM-ULEB

### Onde colocar (D6-WASM-ULEB)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/wasm_triage.py` |
| Funcao | `read_u32_leb` |
| Substituir | corpo sob `TODO [D6-WASM-ULEB]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-WASM-ULEB` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-WASM-ULEB` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```python
PEDAGOGY-SOLUTION: D6-WASM-ULEB
    value=0; shift=0
    for _ in range(5):
        if offset>=len(data): raise ValueError("truncated ULEB128")
        b=data[offset]; offset+=1; value |= (b&0x7f)<<shift
        if not (b&0x80): return value,offset
        shift+=7
    raise ValueError("ULEB128 too long")
def parse_sections(data):
    # 
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-WASM-ULEB`.

### Verifique
Rode o baseline; o caminho de `D6-WASM-ULEB` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-WASM-ULEB` PASS
- [ ] Nao alterei o teste

## D6-WASM-HEADER

### Onde colocar (D6-WASM-HEADER)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/wasm_triage.py` |
| Funcao | `read_u32_leb` |
| Substituir | corpo sob `TODO [D6-WASM-HEADER]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-WASM-HEADER` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-WASM-HEADER` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```python
PEDAGOGY-SOLUTION: D6-WASM-HEADER
    if len(data)<8 or data[:4]!=b"\0asm" or data[4:8]!=b"\x01\0\0\0": raise ValueError("bad WASM header")
    # 
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-WASM-HEADER`.

### Verifique
Rode o baseline; o caminho de `D6-WASM-HEADER` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-WASM-HEADER` PASS
- [ ] Nao alterei o teste

## D6-WASM-SECTIONS

### Onde colocar (D6-WASM-SECTIONS)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/wasm_triage.py` |
| Funcao | `parse_sections` |
| Substituir | corpo sob `TODO [D6-WASM-SECTIONS]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-WASM-SECTIONS` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-WASM-SECTIONS` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```python
PEDAGOGY-SOLUTION: D6-WASM-SECTIONS
    out=[]; cur=8
    while cur<len(data):
        h=cur; sid=data[cur]; cur+=1
        size,cur=read_u32_leb(data,cur); end=cur+size
        if end>len(data): raise ValueError("truncated section")
        out.append({"id":sid,"header_offset":h,"payload_offset":cur,"payload_size":size})
        cur=end
    return out
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-WASM-SECTIONS`.

### Verifique
Rode o baseline; o caminho de `D6-WASM-SECTIONS` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-WASM-SECTIONS` PASS
- [ ] Nao alterei o teste

## Debug

| Sintoma | Causa | Correcao |
|---------|-------|----------|
| stub | corpo intacto | cole o bloco do TODO |
| off-by-one | size/indice | refaca o trace |
| 2o caso falha | estado residual | reset |

## Relatorio de resolucao

- TODOs concluidos:
- Comandos + saida:
- Invariantes:
- Edge cases:
- Benchmark: nao executado / preencher
