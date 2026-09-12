# Comparacao: pipeline_state_object

| Etapa | Software/CPU | OpenGL |
|---|---|---|
| Estado PSO | `core/pso.cpp` | compartilhado |
| Create/bind/cycle | funções de core | mesmas funções |
| Fill sólido | raster triângulo DIB | `GL_TRIANGLES` |
| Wireframe | Bresenham `LINE_LOOP` CPU | `GL_LINE_LOOP` |
| Cor | RGB do PSO → pixels | `glColor3f` |
| Animação | bob + rotação + cycle ~2s | idêntica |
| Present | `StretchDIBits` | `SwapBuffers` |
