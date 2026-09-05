# AI/ML Systems: matrix multiplication + tiling

**Objetivo:** Implementar matmul correta e depois uma versão tiled para entender locality antes de SIMD/GPU.

## Ordem recomendada
1. `TEORIA_PASSO_A_PASSO.md`
2. `PESQUISA_GUIADA.md`
3. starter
4. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`
5. `TESTES_GUIADOS.md`
6. `solutions/` somente como gabarito final

## TODOs auditáveis
- `AI-MM-NAIVE-01`
- `AI-MM-TILED-02`

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-tensor/day03_tiled_matmul` |
| O que levar | tiled matmul + bench |
| Testes a replicar | matmul correctness tests |
| Milestone | day03 tiled matmul milestone |
| Commit sugerido | `feat(tensor): port tiled matmul from day05 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
