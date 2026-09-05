# Chris OS: primeiro compositor gráfico de referência

Você vai construir surfaces RGBA, clipping e alpha compositing em user space. Esse modelo vira o oráculo de correção para o futuro framebuffer/window server do chris-os.

## Projeto cumulativo
`projects/chris-os`

## Fluxo sugerido
1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Abra `starter/EXERCISE_TODO.md`.
3. Implemente antes de consultar `solutions/`.
4. Rode os testes guiados.
5. Execute o benchmark e registre ambiente/resultados.

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-os` |
| O que levar | software compositor |
| Testes a replicar | pixel compositing tests |
| Milestone | MILESTONES.md — OS graphics ref |
| Commit sugerido | `feat(os): port compositor from day02 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
