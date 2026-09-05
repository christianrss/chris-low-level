# Linux kernel: lifecycle de char device + módulo real para revisão

**Objetivo:** Entender open/read/write/release e ownership antes de carregar qualquer módulo; validar a máquina de estados em userspace e revisar um módulo de kernel real sem executá-lo neste ambiente.

## Ordem recomendada
1. `TEORIA_PASSO_A_PASSO.md`
2. `PESQUISA_GUIADA.md`
3. starter
4. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`
5. `TESTES_GUIADOS.md`
6. `solutions/` somente como gabarito final

## TODOs auditáveis
- `KMOD-MODEL-OPEN-01`
- `KMOD-MODEL-IO-02`
- `KMOD-SOURCE-REVIEW-03`

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-linux-module-lab/day03` |
| O que levar | device_model userspace + review notes |
| Testes a replicar | test_device_model |
| Milestone | kmod lab milestone |
| Commit sugerido | `feat(kmod): port device model from day05 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
