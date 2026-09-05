# Teoria passo a passo — Graphics black magic: resource states em Vulkan e D3D12

Em APIs explícitas a GPU não pode adivinhar todas as dependências. Vulkan descreve layouts/stages/access; D3D12 descreve resource states e barriers. Os nomes diferem, mas a pergunta é semelhante: **quem usou o recurso antes, quem usará agora, e que visibilidade/estado é necessário?**

O laboratório é um simulador C++ portátil: `ResourceTracker` guarda estado abstrato `CopyDst`, `ShaderRead`, `RenderTarget`, `Present`. `transition` valida transições permitidas. Funções `to_vulkan()` e `to_d3d12()` mostram o mapeamento mental.

Isso não substitui uma chamada real a `vkCmdPipelineBarrier2` ou `ResourceBarrier`; prepara o raciocínio sem fingir que SDK/GPU foram executados.
