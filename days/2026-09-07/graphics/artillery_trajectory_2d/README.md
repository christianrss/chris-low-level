# Artillery trajectory 2D — CPU + OpenGL + D3D11

**Objetivo:** Física de projétil 2D (ângulo + potência), colisão com terreno 1D, trilha e cratera — mesma cena em três backends.

## Ordem
1. `TEORIA_PASSO_A_PASSO.md`
2. `starter/core/` + `tests/`
3. `software_win32/` → `opengl_win32/` → `d3d11_win32/`
4. `docs/COMPARISON.md`

## TODOs
- `GFX-ART-PHYS-01` — integração Euler do projétil
- `GFX-ART-TERRAIN-02` — colisão com `terrain.sample(x)`
- `GFX-ART-TRAIL-03` — buffer circular de trilha
- `GFX-ART-SW-04` — raster CPU Win32+DIB
- `GFX-ART-GL-05` — OpenGL ortho 2D
- `GFX-ART-D3D-06` — D3D11 swapchain

## Ligação
Faça após revisar `days/2026-09-03/graphics/dual_backend_3d`.
