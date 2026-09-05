# Testes guiados — Graphics black magic: resource states em Vulkan e D3D12

`GFX-STATE-TRANSITION-01`: sequência válida e transição inválida. `GFX-VK-MAP-02`: strings de layout para quatro estados. `GFX-D3D12-MAP-03`: strings de resource state para quatro estados. O teste é portátil e não faz claims de execução Vulkan/D3D12 real.

## Regra de diagnóstico
Se o starter falhar antes de chegar ao comportamento marcado por TODO, isso é defeito de scaffolding. Se compilar/executar e falhar no assert ligado ao TODO, o starter está se comportando como laboratório pedagógico.
