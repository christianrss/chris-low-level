# Tensor, strides e matrix multiplication

Você vai representar uma matriz como armazenamento contíguo + shape + strides, criar uma transpose view sem cópia e implementar matmul ingênuo. Isso prepara cache blocking, SIMD e kernels de ML.

## Projeto cumulativo
`projects/chris-tensor`

## Fluxo sugerido
1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Abra `starter/EXERCISE_TODO.md`.
3. Implemente antes de consultar `solutions/`.
4. Rode os testes guiados.
5. Execute o benchmark e registre ambiente/resultados.

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-tensor` |
| O que levar | strided tensor views + matmul |
| Testes a replicar | tensor shape tests |
| Milestone | MILESTONES.md — tensor core |
| Commit sugerido | `feat(tensor): port strides from day02 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
