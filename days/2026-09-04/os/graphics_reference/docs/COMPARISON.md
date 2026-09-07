# Comparacao: compositor CPU vs apresentacao GL

| Etapa | Software/CPU | OpenGL (demo) |
|---|---|---|
| Superfície | `Surface` RGBA RAM | textura upload |
| Composição | `alpha_over` + `compose` CPU | blit textura para quad fullscreen |
| Dirty rect | `take_dirty_union` visível | só redesenha região damage |
| Frame pacing | `FrameStats` | vsync `SwapBuffers` |
| Janela | Win32 DIB (`demo_cpu`) | WGL (`demo_gl`) |

O core `graphics.cpp` permanece CPU-first; backends de demo apenas apresentam o resultado.
