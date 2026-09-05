# Red Team seguro: ELF entry-point inspector

**Objetivo:** Analisar somente fixtures/binários próprios e localizar classe, endianess, tipo, machine e entry point sem executar o binário.

## Ordem recomendada
1. `TEORIA_PASSO_A_PASSO.md`
2. `PESQUISA_GUIADA.md`
3. starter
4. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`
5. `TESTES_GUIADOS.md`
6. `solutions/` somente como gabarito final

## TODOs auditáveis
- `RT-ELF-HDR-01`
- `RT-ELF-ENTRY-02`

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-binary-toolkit` |
| O que levar | ELF64 entry-point parser |
| Testes a replicar | elf_entry tests |
| Milestone | ELF entry milestone |
| Commit sugerido | `feat(toolkit): port elf entry from day05 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
