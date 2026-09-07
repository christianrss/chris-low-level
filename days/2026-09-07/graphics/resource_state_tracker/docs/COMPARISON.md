# Comparação: CPU simulation vs GPU real — resource state tracker

Módulo **headless** (`GFX_VISUAL_EXEMPT`): validação via CTest, sem janela VISUAL-01.

## O que este lab simula

O `Tracker` em C++ mantém estado lógico e uma fila de `Barrier{id, before, after}`. Isso espelha a **parte de bookkeeping** de um render graph ou command list — não executa trabalho na GPU.

## Tabela comparativa

| Etapa | Software / CPU (este lab) | OpenGL (legado) | Vulkan | D3D12 |
|-------|---------------------------|-----------------|--------|-------|
| Estado lógico | `enum class State` em RAM | implícito (bind + FBO) | `VkImageLayout` | `D3D12_RESOURCE_STATE_*` |
| Registro | `register_resource` | `glGenTextures` + bind | `vkCreateImage` | `CreateCommittedResource` |
| Transição explícita | `transition()` → `Barrier` | raro; `glMemoryBarrier` parcial | `vkCmdPipelineBarrier` | `ResourceBarrier` |
| Batch / flush | `flush()` → `vector<Barrier>` | N/A (driver infere menos) | submit command buffer | `ExecuteCommandLists` |
| Redundância | `false` se mesmo estado | binds repetidos custam | validation warning | debug layer |
| Sincronização real | nenhuma (simulação) | `glFinish` / fences GL | semaphores + fences | fences + signals |
| Present | enum `Present` só lógica | `SwapBuffers` | `vkQueuePresentKHR` | `Present` on swapchain |
| Teste | CTest `starter/tests/test.cpp` | não usado neste módulo | não usado neste módulo | não usado neste módulo |
| Visual | não requerido | context + window | swapchain | HWND + swapchain |

## Pipeline mental — upload até present

```text
CPU Tracker                    GPU real (simplificado)
─────────────                  ───────────────────────
register(tex, Undefined)       create image resource
transition(CopyDst)      →     barrier + copy cmd
transition(ShaderRead)   →     barrier + draw/sample
transition(RenderTarget) →     barrier + render pass
transition(Present)      →     barrier + present queue
flush()                  →     submit + GPU execute
```

## Por que não há janela neste módulo

OpenGL e D3D11 costumam esconder transições atrás de binds. Vulkan/D3D12 **exigem** declaração explícita — o skill transferível é a ordem de estados, não pixels na tela. Outros módulos Day 07 (artillery, raster) cobrem apresentação visual; este foca **barrier batching** puro.

## Mapeamento sugerido (futuro)

| `Tracker::State` | Tradução D3D12 | Tradução Vulkan layout |
|------------------|----------------|-------------------------|
| `Undefined` | `D3D12_RESOURCE_STATE_COMMON` | `VK_IMAGE_LAYOUT_UNDEFINED` |
| `CopyDst` | `D3D12_RESOURCE_STATE_COPY_DEST` | `VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL` |
| `ShaderRead` | `D3D12_RESOURCE_STATE_PIXEL_SHADER_RESOURCE` | `VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL` |
| `RenderTarget` | `D3D12_RESOURCE_STATE_RENDER_TARGET` | `VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL` |
| `Present` | `D3D12_RESOURCE_STATE_PRESENT` | `VK_IMAGE_LAYOUT_PRESENT_SRC_KHR` |

Uma barrier educacional `{id, before, after}` expande para dezenas de campos em APIs reais (stage masks, queue family, subresource range). O tracker ensina **quando** emitir; drivers ensinam **como** preencher structs.

## Headless lab vs integração em engine

| Critério | CPU tracker | Engine com GPU |
|----------|-------------|----------------|
| Determinismo | total em teste unitário | depende de timing GPU |
| CI sem GPU | sim | precisa software raster ou skip |
| Bugs visíveis | asserts CTest | artefatos, validation layers |
| Escopo Day 07 | complemento tier-A | módulos visuais separados |

## Leitura cruzada

- Teoria: `TEORIA_PASSO_A_PASSO.md` seções 5–8.
- Resolução: trace `tex` em `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`.
- Módulo irmão com visual: `days/2026-09-05/graphics/vulkan_d3d12_resource_states/`.
