# Comparacao: o que voce implementa vs o que a API faz

| Etapa | Software/CPU | OpenGL |
|---|---|---|
| Janela | Win32 | Win32 |
| Contexto grafico | nao existe | WGL cria contexto OpenGL |
| Vertex buffer | arrays na RAM | VBO na GPU |
| Vertex processing | `project_vertex()` | vertex shader |
| Triangle setup | `tri()` | fixed-function rasterizer da GPU |
| Barycentric coverage | seu loop por pixel | GPU |
| Depth buffer | `std::vector<float>` | depth buffer do framebuffer |
| Fragment shading | `rgb()` + Lambert CPU | fragment shader GLSL |
| Present | `StretchDIBits` | `SwapBuffers` |
| Fisica | compartilhada | compartilhada |
| Animacao | compartilhada | compartilhada |
| Scene graph simples | compartilhada | compartilhada |

A API grafica nao substitui a engine. Ela acelera/abstrai principalmente o caminho de renderizacao e
acesso a GPU. Transformacoes de cena, animacao, fisica, asset management, ECS, gameplay e grande
parte da arquitetura permanecem responsabilidade do programa/engine.
