# shader_stage_fsm

**Trilha:** `graphics` · **Dia:** 2026-09-08 · **Linguagem:** C++17 (CMake)

## O que voce constroi

FSM pedagogica do ciclo de shader `EDIT → COMPILE → LINK → READY`, com backends **CPU** (`software_win32`) e **OpenGL** (`opengl_win32`) mostrando o mesmo triangulo rotativo colorido por estagio + HUD de barras.

**TODOs:** `GFX-SH-ADVANCE`, `GFX-SH-RESET`, `GFX-SH-COLOR`

## Como rodar

```powershell
cd days/2026-09-08/graphics/shader_stage_fsm/starter
cmake -S . -B build_ci -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
# opcional visual:
# .\build_ci\shader_fsm_sw.exe
# .\build_ci\shader_fsm_gl.exe
```

Starter: `ctest` FAIL ate completar TODOs. Solutions: PASS.

## Ordem de estudo

1. `TEORIA_PASSO_A_PASSO.md`
2. Checkpoint em `../../ATIVIDADES.md`
3. `EXERCICIOS.md` → codigo em `starter/core/`
4. `TESTES_GUIADOS.md` / `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` se travar
5. `BENCHMARK_GUIADO.md` + Relatorio
6. Compare CPU vs OpenGL em `docs/COMPARISON.md`
