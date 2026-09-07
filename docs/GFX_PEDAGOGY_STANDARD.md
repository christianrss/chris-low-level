# Padrão pedagógico — Gráficos (CPU + GPU)

Módulos em `*/graphics/*` e `*/os/graphics_reference` seguem o modelo **dual-backend** do Dia 01 ([`dual_backend_3d`](../days/2026-09-03/graphics/dual_backend_3d)).

## Regras estruturais

1. **CPU primeiro** — `software_win32/` ou `software_2d/` implementa raster/simulação na CPU antes de qualquer API gráfica.
2. **Mesma cena** — OpenGL e (quando aplicável) D3D11 exibem a mesma simulação; física e estado vivem em `core/` ou `common/`.
3. **`docs/COMPARISON.md`** — tabela obrigatória: etapa | CPU | OpenGL | (D3D11).
4. **Separação** — backends só apresentam; não duplicam física/raster pedagógico no shader sem passar pelo CPU.
5. **TESTES_GUIADOS** — casos automatizados + **Caso manual — VISUAL-01** (o que o aluno deve ver na tela).
6. **RESOLUCAO** — padrão anti-resumo: `## Baseline`, placement por TODO, código integral, sem delegar a `solutions/`.
7. **Profundidade** — trace numérico ou pixel-a-pixel no TEORIA antes do código.
8. **VISUAL obrigatório em `solutions/`** — todo executável Win32 (`software_win32`, `opengl_win32`, `d3d11_win32`, `extension` com `wWinMain`) **deve** abrir janela (`CreateWindow`) e apresentar pixels (`StretchDIBits`, `glClear`+`SwapBuffers`, ou `Present` D3D). `MessageBox` só para erros fatais de init — **nunca** como demo. Starters podem manter stub + `TODO`.

## Layout de pastas (3D / 2D com janela)

```text
<modulo>/
├── docs/COMPARISON.md
├── starter/
│   ├── core/ ou common/
│   ├── software_win32/
│   ├── opengl_win32/
│   ├── d3d11_win32/          # opcional ou extensão
│   └── tests/
└── solutions/                # espelho
```

## IDs de TODO

Prefixo sugerido: `GFX-<AREA>-<NN>`. Extensões opcionais (D3D11, depth) usam arquivos/pastas separados para não invalidar starters resolvidos.

## Checker

`scripts/pedagogy_check_unified.py` valida `COMPARISON.md`, `VISUAL-01` em `TESTES_GUIADOS.md`, e **`check_gfx_visual_solutions()`** (janela + present em `solutions/`, sem MessageBox-demo). Módulos excluídos do gate Win32: `graphics_reference`, `vulkan_d3d12_resource_states`.

## Trilha

Ver `docs/LEARNING_PATHS.md` §6.
