# COMPARISON — explicit_barriers

| Aspecto | CPU/software (lab) | OpenGL | D3D12/Vulkan |
|---------|-------------------|--------|--------------|
| Modelo | tabela de arestas | implícito | barreiras explícitas |
| Validação | set `_ALLOWED` | driver | app + validation layers |

Headless exempt: contrato de estados, sem janela.
