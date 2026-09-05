# Exercícios — Surface e compositor 2D

## Fácil

- **D2-GFX-INDEX:** valide coordenadas e converta `(x,y)` em `y*width+x`.
- Calcule índice para width=8 nos pontos (0,0), (7,0) e (3,2).

## Médio

- **D2-GFX-FILL-RECT:** recorte retângulo aos limites da surface antes de preencher pixels.
- Trace clipping manual de `fill_rect(-2,1,5,3)` em surface 6x4.

## Difícil

- **D2-GFX-ALPHA-OVER:** implemente mistura inteira com arredondamento `+127`.
- **D2-GFX-COMPOSE:** percorra layers com offset, clipping por pixel e alpha-over acumulativo.

## Desafio

- Rode benchmark 640x360/40 frames e registre FPS. Proponha otimização por damage rectangle sem implementar.
- Compare resultado visual com e sem gamma; descreva artefato observado em borda de sprite.
