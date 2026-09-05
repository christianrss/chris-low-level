# Resolução guiada passo a passo — Graphics black magic: resource states em Vulkan e D3D12

Abra `starter/resource_state.cpp`.

## 1. transition
Permita a sequência didática `CopyDst -> ShaderRead -> RenderTarget -> Present` e também `Present -> RenderTarget`. Rejeite self-transition e arestas não listadas. Atualize `state_` apenas depois da validação.

## 2. Vulkan mapping
Mapeie:
- CopyDst → `VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL`
- ShaderRead → `VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL`
- RenderTarget → `VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL`
- Present → `VK_IMAGE_LAYOUT_PRESENT_SRC_KHR`

## 3. D3D12 mapping
Mapeie aos nomes `D3D12_RESOURCE_STATE_COPY_DEST`, `PIXEL_SHADER_RESOURCE`, `RENDER_TARGET`, `PRESENT`.

Build/test C++ portátil normalmente. Depois abra `shaders/debug_uv.vert.glsl` e `debug_uv.frag.glsl`; o fragment shader colore `UV` como RGB, um modo visual útil para detectar UVs incorretos. O HLSL equivalente mostra a mesma ideia para D3D12.

Debug conceitual: se uma textura aparece preta em API real, verifique primeiro conteúdo/upload, depois descriptor, depois estado/layout e sincronização; não culpe o shader sem evidência.

## Mapa de consistência auditada
- `GFX-STATE-TRANSITION-01` — starter → resolução → teste → solution.
- `GFX-VK-MAP-02` — starter → resolução → teste → solution.
- `GFX-D3D12-MAP-03` — starter → resolução → teste → solution.
