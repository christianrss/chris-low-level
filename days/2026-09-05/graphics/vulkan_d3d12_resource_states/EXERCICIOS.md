# Exercícios — Vulkan/D3D12 resource states

## Fácil — GFX-STATE-TRANSITION-01
Liste as 4 transições válidas do `ResourceTracker` em ordem de frame típico.

## Médio — GFX-STATE-TRANSITION-01
Implemente `transition()` rejeitando self-transition e arestas inválidas.

## Médio — GFX-VK-MAP-02
Implemente `to_vulkan()` com os quatro layouts do lab.

## Médio — GFX-D3D12-MAP-03
Implemente `to_d3d12()` com os quatro resource states do lab.

## Difícil
Adicione estado `DepthWrite` e transição `RenderTarget -> DepthWrite -> Present`.

## Reflexão
Por que Vulkan separa layout de imagem de access mask na barreira?
