# Graphics black magic: resource states em Vulkan e D3D12

**Objetivo:** Modelar transições de uma textura de upload → shader read → render target e entender por que APIs explícitas exigem sincronização/estado.

## Ordem recomendada
1. `TEORIA_PASSO_A_PASSO.md`
2. `PESQUISA_GUIADA.md`
3. starter
4. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`
5. `TESTES_GUIADOS.md`
6. `solutions/` somente como gabarito final

## TODOs auditáveis
- `GFX-STATE-TRANSITION-01`
- `GFX-VK-MAP-02`
- `GFX-D3D12-MAP-03`

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-gpu-state/day03` |
| O que levar | resource state machine |
| Testes a replicar | state transition tests |
| Milestone | GPU state sim milestone |
| Commit sugerido | `feat(gpu): port resource states from day05 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
