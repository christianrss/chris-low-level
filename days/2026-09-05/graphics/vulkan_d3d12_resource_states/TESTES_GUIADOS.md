# Testes guiados

### Caso 1: `test_states` valida pipeline CopyDst → ShaderRead → RenderTarget → Present.
### Caso 2: **Transição inválida:** CopyDst → Present retorna false.
### Caso 3: **Vulkan:** Present → `VK_IMAGE_LAYOUT_PRESENT_SRC_KHR`.
### Caso 4: **D3D12:** RenderTarget → `D3D12_RESOURCE_STATE_RENDER_TARGET`.
### Caso 5: Consulte diagrama de máquina de estados em TEORIA_PASSO_A_PASSO.md.

## GFX-STATE-TRANSITION-01

Invariante protegida pelo teste com `PEDAGOGY-TEST: GFX-STATE-TRANSITION-01`.

## GFX-D3D12-MAP-03

Invariante protegida pelo teste com `PEDAGOGY-TEST: GFX-D3D12-MAP-03`.

## GFX-VK-MAP-02

Invariante protegida pelo teste com `PEDAGOGY-TEST: GFX-VK-MAP-02`.
