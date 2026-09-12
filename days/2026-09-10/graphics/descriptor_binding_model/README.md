# Descriptor Binding Model — CPU + OpenGL

**Objetivo:** Layout com N slots, bind de tint por slot, sample no draw — três painéis lado a lado que trocam cor via rebind animado.

## Ordem
1. `TEORIA_PASSO_A_PASSO.md`
2. `starter/core/` + `tests/`
3. `software_win32/` → `opengl_win32/`
4. `docs/COMPARISON.md`

## TODOs
- `GFX-DESC-LAYOUT` — `make_layout`
- `GFX-DESC-BIND` — `bind(set, slot, tint)`
- `GFX-DESC-SAMPLE` — `sample(set, slot)`

## Ligação
Espelha o modelo de descriptor sets (Vulkan) / root tables (D3D12) em versão 2D colorida.
