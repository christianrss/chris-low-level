# Resolução guiada passo a passo

Abra `starter/resource_state.cpp`.

## Transições - GFX-STATE-TRANSITION-01
Permita apenas `CopyDst->ShaderRead`, `ShaderRead->RenderTarget`, `RenderTarget->Present` e `Present->RenderTarget`. Rejeite `from == to` e outras arestas. Atualize `state_` somente depois de validar.

## Vulkan - GFX-VK-MAP-02
Mapeie CopyDst, ShaderRead, RenderTarget e Present para os layouts especificados na teoria.

## D3D12 - GFX-D3D12-MAP-03
Mapeie para `COPY_DEST`, `PIXEL_SHADER_RESOURCE`, `RENDER_TARGET` e `PRESENT`.

Build/test portátil:
```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

Depois abra `starter/shaders/debug_uv.vert.glsl`, `debug_uv.frag.glsl` e `debug_uv.hlsl`. O fragment/pixel shader transforma UV em RGB.

Debug conceitual para textura preta: verifique conteúdo/upload -> descriptor -> estado/layout -> sincronização -> shader, nessa ordem de evidências.

## Mapa de consistência auditada
- `GFX-STATE-TRANSITION-01` - starter -> resolução -> teste -> solution.
- `GFX-VK-MAP-02` - starter -> resolução -> teste -> solution.
- `GFX-D3D12-MAP-03` - starter -> resolução -> teste -> solution.
