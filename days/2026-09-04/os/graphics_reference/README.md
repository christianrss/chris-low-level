# Chris OS: compositor de referência com damage e frame pacing

Você vai construir surfaces RGBA, clipping, alpha compositing, **dirty rectangles** e **compose_with_damage** em user space. Esse modelo vira o oráculo de correção (e de custo em pixels) para o futuro framebuffer/window server do chris-os.

## Projeto cumulativo
`projects/chris-os`

## Fluxo sugerido
1. Leia `TEORIA_PASSO_A_PASSO.md` (inclui dirty-rect e vsync/pacing).
2. Implemente os seis TODOs em `starter/` (`EXERCICIOS.md` + `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`).
3. Use `RESOLUCAO_APENDICE.md` para fantasma de sprite e debug de `FrameStats`.
4. Rode `TESTES_GUIADOS.md` até PASS.
5. Execute o benchmark full vs damage e registre ambiente/resultados.

## TODOs

| ID | Tema |
|----|------|
| `D2-GFX-INDEX` | índice row-major |
| `D2-GFX-FILL-RECT` | clip + fill |
| `D2-GFX-ALPHA-OVER` | source-over inteiro |
| `D2-GFX-COMPOSE` | layers + z-order |
| `D2-GFX-DIRTY-RECT` | união AABB / `take_dirty_union` |
| `D2-GFX-FRAME-PACE` | damage compose + `FrameStats` |

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-os` |
| O que levar | software compositor + dirty/pace |
| Testes a replicar | pixel compositing + damage stats |
| Milestone | MILESTONES.md — OS graphics ref |
| Commit sugerido | `feat(os): port damage compositor from day02 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
