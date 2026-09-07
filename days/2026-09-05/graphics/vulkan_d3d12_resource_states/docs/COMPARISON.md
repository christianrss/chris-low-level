# Comparacao: estados de recurso vs frame graph

| Etapa | CPU (tracker) | Vulkan | D3D12 |
|---|---|---|---|
| Estado lógico | `ResourceTracker::State` | `VK_IMAGE_LAYOUT_*` | `D3D12_RESOURCE_STATE_*` |
| Transição | `transition()` | barriers | ResourceBarrier |
| Visualização | `state_visualizer` (extensão) | cor por layout | cor por state |
| Shader debug | GLSL `debug_uv` (OpenGL ref) | SPIR-V | HLSL |
| Cena referência | frame artilharia Day07 N9 | mesmo UV debug | mesmo HLSL debug |

Ver `extension/frame_graph.hpp` para ordem de passes ligada à artilharia 2D.
