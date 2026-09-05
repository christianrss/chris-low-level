# .NET/CLR: tiny CIL decoder

**Objetivo:** Decodificar um subconjunto de bytecode CIL e conectar bytes de método ao modelo de stack machine.

## Ordem recomendada
1. `TEORIA_PASSO_A_PASSO.md`
2. `PESQUISA_GUIADA.md`
3. starter
4. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`
5. `TESTES_GUIADOS.md`
6. `solutions/` somente como gabarito final

## TODOs auditáveis
- `CLR-IL-OPCODE-01`
- `CLR-IL-OPERAND-02`

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-dotnet-ilvm/day03` |
| O que levar | CIL opcode decoder |
| Testes a replicar | dotnet run on fixtures |
| Milestone | IL decoder milestone |
| Commit sugerido | `feat(ilvm): port CIL decoder from day05 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
