# Red Team seguro: triagem ELF64

Você vai analisar apenas um header ELF sintético/benigno e o próprio lab target. O objetivo é reconhecer magic/class/endianness/machine/entry offsets e escrever parsing defensivo com casos inválidos.

## Projeto cumulativo
`projects/chris-binary-toolkit`

## Fluxo sugerido
1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Abra `starter/EXERCISE_TODO.md`.
3. Implemente antes de consultar `solutions/`.
4. Rode os testes guiados.
5. Execute o benchmark e registre ambiente/resultados.

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-binary-toolkit` |
| O que levar | ELF64 header triage |
| Testes a replicar | elf64_benchmark.py |
| Milestone | MILESTONES.md — ELF triage |
| Commit sugerido | `feat(toolkit): port elf64 triage from day02 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
