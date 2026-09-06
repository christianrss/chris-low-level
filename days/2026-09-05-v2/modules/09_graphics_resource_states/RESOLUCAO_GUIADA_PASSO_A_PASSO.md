## Mapa exato starter → resolução

| TODO ID | Starter |
|---------|--------|
| — | — |

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
## Relatório de resolução

- **TODOs concluídos:** (liste os IDs implementados)
- **Comandos de teste:**
  ```bash
  # cole aqui o comando exato usado
  ```
- **Saída esperada:** PASS nos testes do módulo
- **Invariantes verificadas:** (liste)
- **Edge cases testados:** (liste)
- **Benchmark:** hipótese + resultado ou declaração honesta de skip
- **Toolchain não executada:** (se aplicável)

### 4. Por que funciona

O stub no âncora TODO é substituído pelo comportamento testado.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.


## `GFX-STATE-01`

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/resource_state.cpp` |
| **Função / âncora** | `TODO [GFX-STATE-01]` |
| **Substituir** | stub marcado por esse TODO |
| **Não mexer** | outros arquivos até este ID passar |

### Escreva o código

```text
# Implemente conforme starter/resource_state.cpp e compare solutions/resource_state.cpp
```

### Por que funciona

A edição no arquivo certo faz o `PEDAGOGY-TEST: GFX-STATE-01` passar.
