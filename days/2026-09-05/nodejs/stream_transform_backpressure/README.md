# Node.js: Transform stream + backpressure observável

**Objetivo:** Construir Transform que separa linhas preservando chunks arbitrários e observar quando `write()` retorna false.

## Ordem recomendada
1. `TEORIA_PASSO_A_PASSO.md`
2. `PESQUISA_GUIADA.md`
3. starter
4. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`
5. `TESTES_GUIADOS.md`
6. `solutions/` somente como gabarito final

## TODOs auditáveis
- `NODE-XFORM-01`
- `NODE-BACKPRESSURE-02`

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-node-streaming/day03_backpressure` |
| O que levar | backpressure demo + transform |
| Testes a replicar | test.js |
| Milestone | backpressure milestone |
| Commit sugerido | `feat(node): port backpressure from day05 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
