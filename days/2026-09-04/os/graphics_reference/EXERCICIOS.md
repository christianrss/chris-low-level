# Exercícios — Surface, dirty-rect e frame pacing

## Fácil

- **D2-GFX-INDEX:** valide coordenadas e converta `(x,y)` em `y*width+x`.
- Calcule índice para width=8 nos pontos (0,0), (7,0) e (3,2).

## Médio

- **D2-GFX-FILL-RECT:** recorte retângulo aos limites da surface antes de preencher pixels; marque dirty só na interseção.
- Trace clipping manual de `fill_rect(-2,1,5,3)` em surface 6x4 e anote o `Rect` dirty.

## Difícil

- **D2-GFX-ALPHA-OVER:** implemente mistura inteira com arredondamento `+127`.
- **D2-GFX-COMPOSE:** percorra layers com offset, clipping por pixel, alpha-over acumulativo e dirty do footprint.
- **D2-GFX-DIRTY-RECT:** implemente `DirtyTracker::mark_dirty` / `take_dirty_union` (união AABB).
- **D2-GFX-FRAME-PACE:** `compose_with_damage` só na região dirty; preencha `FrameStats {pixels_touched, dirty_area}`.

## Desafio

- Rode o benchmark full vs damage (640×360 / 40 frames). Registre FPS e `pixels_touched`. Explique a razão damage/full.
- Simule no papel um sprite que se move 4 px: mostre por que marcar só a posição nova deixa fantasma.
- Compare resultado visual com e sem gamma; descreva artefato em borda de sprite (conceito).
