# Comparacao: artilharia 2D

| Etapa | Software/CPU | OpenGL | D3D11 |
|---|---|---|---|
| Fisica | `core/artillery.cpp` | compartilhada | compartilhada |
| Terreno | raster linha + fill CPU | `GL_LINES` + tri fan | line strip HLSL |
| Projétil | círculo CPU | `GL_POINTS` | point list |
| Trilha | polyline DIB | `GL_LINE_STRIP` | line strip |
| Present | `StretchDIBits` | `SwapBuffers` | `Present` |
