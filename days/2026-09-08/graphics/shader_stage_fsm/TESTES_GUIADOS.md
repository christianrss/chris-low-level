# Testes guiados — shader_stage_fsm

### Caso 1: `GFX-SH-ADVANCE`
Rode `ctest` — PEDAGOGY-TEST cobre `GFX-SH-ADVANCE`.
`advance` percorre Edit→Compile→Link→Ready→Edit.

### Caso 2: `GFX-SH-RESET`
Rode `ctest` — PEDAGOGY-TEST cobre `GFX-SH-RESET`.
Apos estar em Link, `reset()` volta a Edit.

### Caso 3: `GFX-SH-COLOR`
Rode `ctest` — PEDAGOGY-TEST cobre `GFX-SH-COLOR`.
RGB de cada estagio bate com a tabela da TEORIA.

### Caso manual — VISUAL-01
Abra `shader_fsm_sw` (titulo “CPU”) e `shader_fsm_gl` (titulo “OpenGL”).
Voce deve ver: triangulo rotativo cujo fill muda de cor a cada ~1.5s (amarelo→azul→roxo→verde), quatro barras HUD a esquerda (a ativa mais larga), fundo escuro. Esc fecha; R reseta para amarelo.
