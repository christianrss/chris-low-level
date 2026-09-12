# Pipeline State Object — CPU + OpenGL

**Objetivo:** Modelar um PSO mínimo (`topology`, `fill_mode`, cor), criar/bindar/ciclar presets e ver o efeito numa cena animada com o mesmo triângulo em software e OpenGL.

## Ordem
1. `TEORIA_PASSO_A_PASSO.md`
2. `starter/core/` + `tests/`
3. `software_win32/` → `opengl_win32/`
4. `docs/COMPARISON.md`

## TODOs
- `GFX-PSO-CREATE` — `create_default_pso()`
- `GFX-PSO-BIND` — `bind(active, src)`
- `GFX-PSO-CYCLE` — `cycle_pso` pelos 3 presets

## Ligação
Siga o padrão dual-backend de `artillery_trajectory_2d` (Dia 07).
