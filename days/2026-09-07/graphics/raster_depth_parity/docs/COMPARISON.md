# Comparacao: depth parity

| Etapa | Software/CPU | OpenGL |
|---|---|---|
| Depth storage | `std::vector<float>` | framebuffer depth |
| Clear | `fill(1.0f)` | `glClear(DEPTH)` |
| Per-pixel test | `depth < z[i]` | GPU fixed function |
| Paridade | hash região central | screenshot equivalente |
