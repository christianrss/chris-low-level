# Linux terminal: ANSI parser como preparação para PTY/TTY

**Objetivo:** Evoluir o terminal para interpretar SGR de cor e cursor, preparando a futura integração com PTY real e shell próprio.

## Ordem recomendada
1. `TEORIA_PASSO_A_PASSO.md`
2. `PESQUISA_GUIADA.md`
3. starter
4. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`
5. `TESTES_GUIADOS.md`
6. `solutions/` somente como gabarito final

## TODOs auditáveis
- `TERM-ANSI-SGR-01`
- `TERM-CURSOR-02`

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-linux-terminal/day03_ansi` |
| O que levar | ANSI parser for terminal |
| Testes a replicar | test_ansi.py |
| Milestone | linux terminal milestone |
| Commit sugerido | `feat(terminal): port ANSI parser from day05 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
