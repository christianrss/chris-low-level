# Chris Debugger: protocolo remoto v1

Você vai desenhar framing binário versionado para o futuro kernel debugger: magic, versão, command, request id, length, checksum e payload. Ainda não há código privilegiado.

## Projeto cumulativo
`projects/chris-debugger`

## Fluxo sugerido
1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Abra `starter/EXERCISE_TODO.md`.
3. Implemente antes de consultar `solutions/`.
4. Rode os testes guiados.
5. Execute o benchmark e registre ambiente/resultados.

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-debugger` |
| O que levar | debugger wire protocol v1 |
| Testes a replicar | encode/decode roundtrip |
| Milestone | MILESTONES.md — protocol v1 |
| Commit sugerido | `feat(debugger): port protocol from day02 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
