# Resolucao guiada — explicit_barriers

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D7-GFX-VALIDATE` | `starter/explicit_barriers.py` | `validate_transition` |
| `D7-GFX-D3D12` | `starter/explicit_barriers.py` | `d3d12_barrier` |
| `D7-GFX-VULKAN` | `starter/explicit_barriers.py` | `vulkan_barrier` |


## Baseline

```powershell
cd days/2026-09-09/graphics/explicit_barriers/starter
python test_explicit_barriers.py
```

**Esperado antes dos TODOs:** FAIL.


## D7-GFX-VALIDATE

### Onde colocar (D7-GFX-VALIDATE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/explicit_barriers.py` |
| Funcao | `validate_transition` |
| Substituir | corpo sob `TODO [D7-GFX-VALIDATE]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-GFX-VALIDATE` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
    if (before,after) not in _ALLOWED: raise ValueError("invalid transition")
    return True
def d3d12_barrier(before,after):
    validate_transition(before,after);m={"Undefined":"COMMON","CopyDst":"COPY_DEST","ShaderRead":"PIXEL_SHADER_RESOURCE","RenderTarget":"RENDER_TARGET","Present":"PRESENT"};return {"before":m[before],"after":m[after]}
def vulkan_barrier(before,after):
    validate_transition(before,after);m={"Undefined":("UNDEFINED","TOP_OF_PIPE","NONE"),"CopyDst":("TRANSFER_DST_OPTIMAL","TRANSFER","TRANSFER_WRITE"),"ShaderRead":("SHADER_READ_ONLY_OPTIMAL","FRAGMENT_SHADER","SHADER_READ"),"RenderTarget":("COLOR_ATTACHMENT_OPTIMAL","COLOR_ATTACHMENT_OUTPUT","COLOR_ATTACHMENT_WRITE"),"Present":("PRESENT_SRC_KHR","BOTTOM_OF_PIPE","NONE")};return {"before":m[before],"after":m[after]}
```

### Por que funciona?
Materializa o contrato numerico de `D7-GFX-VALIDATE`.

### Verifique
Baseline parcial; `D7-GFX-VALIDATE` PASS.

### Checkpoint
- [ ] `D7-GFX-VALIDATE` PASS

## D7-GFX-D3D12

### Onde colocar (D7-GFX-D3D12)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/explicit_barriers.py` |
| Funcao | `d3d12_barrier` |
| Substituir | corpo sob `TODO [D7-GFX-D3D12]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-GFX-D3D12` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
    validate_transition(before,after);m={"Undefined":"COMMON","CopyDst":"COPY_DEST","ShaderRead":"PIXEL_SHADER_RESOURCE","RenderTarget":"RENDER_TARGET","Present":"PRESENT"};return {"before":m[before],"after":m[after]}
def vulkan_barrier(before,after):
    validate_transition(before,after);m={"Undefined":("UNDEFINED","TOP_OF_PIPE","NONE"),"CopyDst":("TRANSFER_DST_OPTIMAL","TRANSFER","TRANSFER_WRITE"),"ShaderRead":("SHADER_READ_ONLY_OPTIMAL","FRAGMENT_SHADER","SHADER_READ"),"RenderTarget":("COLOR_ATTACHMENT_OPTIMAL","COLOR_ATTACHMENT_OUTPUT","COLOR_ATTACHMENT_WRITE"),"Present":("PRESENT_SRC_KHR","BOTTOM_OF_PIPE","NONE")};return {"before":m[before],"after":m[after]}
```

### Por que funciona?
Materializa o contrato numerico de `D7-GFX-D3D12`.

### Verifique
Baseline parcial; `D7-GFX-D3D12` PASS.

### Checkpoint
- [ ] `D7-GFX-D3D12` PASS

## D7-GFX-VULKAN

### Onde colocar (D7-GFX-VULKAN)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/explicit_barriers.py` |
| Funcao | `vulkan_barrier` |
| Substituir | corpo sob `TODO [D7-GFX-VULKAN]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D7-GFX-VULKAN` falha.

### Algoritmo / trace
1. Leia o assert do teste ligado a este TODO.
2. Execute o Caso 1 no papel (entrada → estado → saida).
3. Compare com o bloco abaixo antes de colar no starter.

### Escreva o codigo

```python
    validate_transition(before,after);m={"Undefined":("UNDEFINED","TOP_OF_PIPE","NONE"),"CopyDst":("TRANSFER_DST_OPTIMAL","TRANSFER","TRANSFER_WRITE"),"ShaderRead":("SHADER_READ_ONLY_OPTIMAL","FRAGMENT_SHADER","SHADER_READ"),"RenderTarget":("COLOR_ATTACHMENT_OPTIMAL","COLOR_ATTACHMENT_OUTPUT","COLOR_ATTACHMENT_WRITE"),"Present":("PRESENT_SRC_KHR","BOTTOM_OF_PIPE","NONE")};return {"before":m[before],"after":m[after]}
result = handle_d7_gfx_vulkan(state)
assert result is not None  # D7-GFX-VULKAN
return result
```

### Por que funciona?
Materializa o contrato numerico de `D7-GFX-VULKAN`.

### Verifique
Baseline parcial; `D7-GFX-VULKAN` PASS.

### Checkpoint
- [ ] `D7-GFX-VULKAN` PASS

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
