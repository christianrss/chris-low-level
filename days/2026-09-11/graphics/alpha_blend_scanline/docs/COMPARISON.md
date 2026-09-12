# Comparacao: alpha_blend_scanline

| Etapa | Software/CPU | OpenGL |
|---|---|---|
| blend_pixel / scanline | `core/blend.cpp` | equivalente via `GL_BLEND` |
| Fundo | checkerboard no framebuffer | quads checker |
| Sprites | blit + `blend_scanline` | `glColor4f` + src-over |
| Bounce | `update_sprite` core | mesma função |
| Present | `StretchDIBits` | `SwapBuffers` |
