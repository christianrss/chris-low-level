# Comparacao: shader_stage_fsm

| Etapa | Software/CPU | OpenGL |
|---|---|---|
| FSM | `core/shader_fsm.cpp` (`advance`/`reset`/`stage_color`) | compartilhada |
| Cor do fill | `stage_color()` → pixels DIB | `stage_color()` → `glColor3f` |
| Triangulo | raster CPU + rotacao por tempo | `GL_TRIANGLES` + rotacao |
| HUD de estagios | barras `fill_rect` | barras `GL_QUADS` |
| Auto-advance | timer 1.5s no loop | mesmo timer |
| Present | `StretchDIBits` | `SwapBuffers` |
