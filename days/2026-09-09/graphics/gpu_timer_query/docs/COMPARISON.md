# Comparacao — gpu_timer_query

| Etapa | CPU (`software_win32`) | OpenGL (`opengl_win32`) |
|-------|------------------------|-------------------------|
| Estado | `core/` | mesmo `core/` |
| Raster | StretchDIBits | glBegin/glEnd + SwapBuffers |
| Animacao | steady_clock | steady_clock |
| Validacao | CTest | CTest + VISUAL-01 |
