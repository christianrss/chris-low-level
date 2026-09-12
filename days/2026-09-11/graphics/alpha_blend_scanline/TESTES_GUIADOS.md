# Testes guiados — alpha_blend_scanline

### Caso 1: `GFX-BLEND-PIXEL`
Src vermelho a=128 sobre dst preto → `r > 100`.

### Caso 2: `GFX-BLEND-SCAN`
Scanline de dois pixels opacos: `line_d[0].g == 255`.

### Caso 3: `GFX-BLEND-SPRITE`
Após `update_sprite` com vx positivo, `s.x` avança.

### Caso manual — VISUAL-01
Abra `blend_sw` e `blend_gl`. Fundo xadrez; dois sprites translúcidos (vermelho/azul) ricocheteiam nas bordas e misturam-se com o checker (e entre si quando se cruzam). Esc fecha. Paridade visual CPU vs `glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)`.
