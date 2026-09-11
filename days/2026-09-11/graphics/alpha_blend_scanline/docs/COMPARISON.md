# COMPARISON — alpha_blend_scanline

| Aspecto | CPU/software (este lab) | OpenGL | D3D/GPU blend |
|---------|-------------------------|--------|---------------|
| Formula | (d*(255-a)+s*a)/255 | glBlendFunc | BlendState |
| Scanline | loop C++ | fragment | ROP |
| Visual | headless exempt | framebuffer | swap chain |

Headless de proposito: o numero 128 e o mesmo contrato.
