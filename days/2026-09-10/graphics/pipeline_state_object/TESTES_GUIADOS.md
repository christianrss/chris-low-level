# Testes guiados — pipeline_state_object

### Caso 1: `GFX-PSO-CREATE`
`create_default_pso()` devolve fill sólido com componente vermelho dominante. Rode `ctest` — PEDAGOGY-TEST cobre o ID.

### Caso 2: `GFX-PSO-BIND`
`bind` copia `topology`, `fill_mode` e `r,g,b` de `src` para `active`.

### Caso 3: `GFX-PSO-CYCLE`
Três chamadas a `cycle_pso` percorrem índices 1 → 2 → 0 e aplicam os presets wire/azul/sólido.

### Caso manual — VISUAL-01
Abra `pso_sw` e `pso_gl`. Deve aparecer um triângulo a rodar/oscilar suavemente; a cada ~2 segundos a aparência muda entre fill vermelho, wireframe verde e fill azul. Esc fecha a janela. Ambos os backends mostram a mesma sequência de estados.
