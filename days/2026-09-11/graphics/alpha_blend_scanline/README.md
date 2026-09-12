# Alpha Blend Scanline — CPU + OpenGL

**Objetivo:** Porter-Duff src-over (`blend_pixel` / `blend_scanline`), sprites com bounce (`update_sprite`), mesma cena em DIB e OpenGL (`GL_BLEND`).

## Ordem
1. `TEORIA_PASSO_A_PASSO.md`
2. `starter/core/` + `tests/`
3. `software_win32/` → `opengl_win32/`
4. `docs/COMPARISON.md`

## TODOs
- `GFX-BLEND-PIXEL`
- `GFX-BLEND-SCAN`
- `GFX-BLEND-SPRITE`

## Build
```powershell
cmake -S starter -B starter/build_ci
cmake --build starter/build_ci
ctest --test-dir starter/build_ci --output-on-failure
```
Demos: `blend_sw.exe` / `blend_gl.exe`.
