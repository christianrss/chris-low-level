# Comparacao: o que voce implementa vs o que a API faz (v2 — +D3D11)

| Etapa | Software/CPU | OpenGL | D3D11 (extensão) |
|---|---|---|---|
| Janela | Win32 | Win32 | Win32 |
| Contexto grafico | nao existe | WGL cria contexto OpenGL | `D3D11CreateDevice` + swapchain |
| Vertex buffer | arrays na RAM | VBO na GPU | `ID3D11Buffer` dynamic |
| Vertex processing | `project_vertex()` | vertex shader GLSL | vertex shader HLSL |
| Triangle setup | `tri()` | rasterizer GPU | IA + VS |
| Barycentric coverage | seu loop por pixel | GPU | GPU |
| Depth buffer | `std::vector<float>` | framebuffer depth | depth/stencil view |
| Fragment shading | `rgb()` + Lambert CPU | fragment shader GLSL | PS Lambert HLSL |
| Present | `StretchDIBits` | `SwapBuffers` | `IDXGISwapChain::Present` |
| Fisica | compartilhada | compartilhada | compartilhada |

A API grafica nao substitui a engine. Ela acelera/abstrai principalmente o caminho de renderizacao.

**Extensão opcional:** `d3d11_win32/` — TODOs `GFX-D3D11-CTX-01`, `GFX-D3D11-DRAW-02` documentados em `RESOLUCAO_APENDICE.md`.
