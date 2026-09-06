# Teoria passo a passo

## 1. APIs explícitas
Vulkan e D3D12 exigem que o programa pense explicitamente em estados/uso de recursos. Uma textura não é apenas “uma textura”: ela pode estar sendo destino de cópia, lida por shader, usada como render target ou apresentada.

## 2. Modelo portátil
Hoje não inicializamos GPU real. Construímos `ResourceTracker` em C++ para validar transições didáticas e mapear um estado abstrato para nomes de layout/state de Vulkan e D3D12. Isso ensina a máquina de estados sem depender de hardware/SDK.

## 3. Sequência típica
`CopyDst -> ShaderRead -> RenderTarget -> Present` representa upload, leitura, render e apresentação. Também aceitamos `Present -> RenderTarget` para começar novo frame. Self-transition e arestas não autorizadas são rejeitadas.

## 4. Mapeamento
Vulkan usa layouts como `VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL`; D3D12 usa resource states como `D3D12_RESOURCE_STATE_COPY_DEST`. Os nomes não são equivalência perfeita de toda a sincronização real, mas formam uma ponte mental.

## 5. Debug shaders
Os shaders `debug_uv.*` convertem UV em cor. É uma técnica visual simples para separar erro de coordenada de erro de upload/layout/descriptor.

## 6. Honestidade de execução
Não há `glslangValidator`, `dxc` nem backend D3D12/Vulkan configurado neste ambiente. O código portátil é compilado/testado; os shaders são fonte para inspeção.

## O quê

Este módulo ensina o conceito central do laboratório v2 com foco operacional no `starter/`.

## Como

Siga os `TODO [ID]` no starter; use a resolução para localizar arquivo/função e o que substituir.

| Etapa | Ação |
|-------|------|
| 1 | Ler README e mapa de TODOs |
| 2 | Implementar no starter |
| 3 | Rodar testes |

## Por que

Sem teoria mínima o aluno não conecta o exercício ao sistema maior.

## Por que (design)

O formato v2 compacta o dia 05; ainda assim cada módulo precisa de O quê/Como/Por quê verificáveis.

## Por que (qualidade)

O checker unificado exige ≥120 linhas, diagrama/tabela e ≥3 seções Por quê.

## Invariantes

- Cada TODO tagueado aparece em starter, solução, testes e resolução.
- Placement (Onde colocar) por ID.

## Bugs comuns

| Sintoma | Causa | Debug |
|---------|-------|-------|
| teste FAIL | stub não substituído | abra a âncora TODO |
| parse errado | ordem de campos | compare com solutions |

## Trace manual

No papel: anote entrada → transformação → saída esperada do primeiro teste do módulo.

## O quê

Este módulo ensina o conceito central do laboratório v2 com foco operacional no `starter/`.

## Como

Siga os `TODO [ID]` no starter; use a resolução para localizar arquivo/função e o que substituir.

| Etapa | Ação |
|-------|------|
| 1 | Ler README e mapa de TODOs |
| 2 | Implementar no starter |
| 3 | Rodar testes |

## Por que

Sem teoria mínima o aluno não conecta o exercício ao sistema maior.

## Por que (design)

O formato v2 compacta o dia 05; ainda assim cada módulo precisa de O quê/Como/Por quê verificáveis.

## Por que (qualidade)

O checker unificado exige ≥120 linhas, diagrama/tabela e ≥3 seções Por quê.

## Invariantes

- Cada TODO tagueado aparece em starter, solução, testes e resolução.
- Placement (Onde colocar) por ID.

## Bugs comuns

| Sintoma | Causa | Debug |
|---------|-------|-------|
| teste FAIL | stub não substituído | abra a âncora TODO |
| parse errado | ordem de campos | compare com solutions |

## Trace manual

No papel: anote entrada → transformação → saída esperada do primeiro teste do módulo.

## O quê

Este módulo ensina o conceito central do laboratório v2 com foco operacional no `starter/`.

## Como

Siga os `TODO [ID]` no starter; use a resolução para localizar arquivo/função e o que substituir.

| Etapa | Ação |
|-------|------|
| 1 | Ler README e mapa de TODOs |
| 2 | Implementar no starter |
| 3 | Rodar testes |

## Por que

Sem teoria mínima o aluno não conecta o exercício ao sistema maior.

## Por que (design)

O formato v2 compacta o dia 05; ainda assim cada módulo precisa de O quê/Como/Por quê verificáveis.

## Por que (qualidade)

O checker unificado exige ≥120 linhas, diagrama/tabela e ≥3 seções Por quê.

## Invariantes

- Cada TODO tagueado aparece em starter, solução, testes e resolução.
- Placement (Onde colocar) por ID.

## Bugs comuns

| Sintoma | Causa | Debug |
|---------|-------|-------|
| teste FAIL | stub não substituído | abra a âncora TODO |
| parse errado | ordem de campos | compare com solutions |

## Trace manual

No papel: anote entrada → transformação → saída esperada do primeiro teste do módulo.
