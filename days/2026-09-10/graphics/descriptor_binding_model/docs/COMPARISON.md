# Comparacao: descriptor_binding_model

| Etapa | Software/CPU | OpenGL |
|---|---|---|
| Layout / bind / sample | `core/descriptor.cpp` | compartilhado |
| Painéis 0..2 | retângulos DIB tintados | `GL_QUADS` + `glColor3f` |
| Animação | bob + rebind a cada ~1.5s | idêntica |
| Present | `StretchDIBits` | `SwapBuffers` |
