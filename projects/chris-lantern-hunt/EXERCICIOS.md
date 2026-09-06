# EXERCICIOS — Lantern Hunt

Quatro níveis de dificuldade. Cada exercício mapeia a um ou mais `TODO [LANTERN-*]`.

---

## Fácil

### E1 — Seed reproduzível (`LANTERN-PROC-01`)
Implemente `generate_dungeon` em `starter/src/procgen.cpp` até `test_procgen` passar com seed `42`.

**Critério:** duas chamadas com mesma seed produzem `cells` idênticos.

### E2 — Carregar uma textura (`LANTERN-TEX-02`)
Carregue `floor_albedo.png` com `stbi_load` e exiba no chão.

**Critério:** chão não é mais cinza sólido.

### E3 — Ambiente em loop (`LANTERN-AUDIO-08`)
Inicialize `ma_engine` e toque `ambient_dark.wav` em loop.

**Critério:** rugido audível ao abrir o jogo.

### E12 — Texto no menu (`LANTERN-FONT-13`)
Implemente `FontRenderer::draw_text` com a fonte 5×7 embutida.

**Critério:** título “LANTERN HUNT” legível no menu principal.

---

## Médio

### E4 — Normal mapping (`LANTERN-NORM-03`)
Complete o fragment shader com sample de `u_normal_map` via `v_tbn`.

**Critério:** relevo visível nas paredes sob a lanterna.

### E5 — Lanterna estreita (`LANTERN-LIGHT-04`)
Ajuste `u_ambient`, `u_spot_cutoff`, `u_spot_exponent` para cone ~25°.

**Critério:** corredores fora do cone ficam quase pretos.

### E6 — Colisão slide (`LANTERN-CAM-02`)
Implemente `move_with_collision` e confirme que o jogador não atravessa paredes nos cantos.

**Critério:** `test_collision` passa.

### E13 — Barra de vida (`LANTERN-HUD-14`)
Desenhe barra de vida com `FontRenderer::draw_bar` no canto inferior.

**Critério:** vida diminui ao encostar em inseto; barra reflete `player.health`.

### E14 — Menu jogável (`LANTERN-MENU-15`)
Três entradas: seed 42, aleatório, sair; navegação por setas.

**Critério:** boot abre em `MainMenu`; Enter inicia partida sem crash.

---

## Difícil

### E7 — Bolinha de gude (`LANTERN-PROJ-05` + `LANTERN-HIT-06`)
Pool de projéteis + eliminação de insetos.

**Critério:** inseto some ao acerto; projétil para na parede.

### E8 — Insetos em parede (`LANTERN-AI-07`)
Patrol em superfícies chão e parede (4 orientações).

**Critério:** pelo menos 3 insetos em paredes em seed `42`.

### E9 — Comida e progresso (`LANTERN-PICKUP-09` + `LANTERN-PLACE-10`)
5 pickups com distância mínima do spawn; contador no HUD.

**Critério:** `COMIDA 5/5` após coletar tudo.

### E15 — Lago procedural (`LANTERN-WATER-12`)
`carve_water_pool` + breath meter + bloqueio de deep sem natação.

**Critério:** `test_procgen` assert `water_count() >= 8`; barra RESPIRACAO na água.

### E16 — Gosma e overlay (`LANTERN-SLIME-11`)
Dano em células `Slime`, lentidão e `draw_slime_overlay`.

**Critério:** poça verde reduz velocidade; overlay verde ao tomar dano de inseto.

### E17 — Altar e checkpoint (`LANTERN-CHK-16`)
Tecla E salva posição, vida, breath e contadores.

**Critério:** `test_checkpoint` passa; altar emissivo após ativação.

---

## Desafio

### E10 — Benchmark FPS
Medir FPS médio 60 s em dungeon 32×32; documentar em `docs/BENCHMARK_GUIADO.md`.

**Meta dia 1:** ≥ 45 FPS em GPU integrada (sem contar overhead de HUD documentado).

### E11 — Nova seed com R
`R` regenera dungeon + respawn sem reiniciar processo.

**Critério:** layout diferente, sem crash de áudio/texturas.

### E18 — Vitória por objetivos (`LANTERN-OBJ-17`)
Cinco objetivos encadeados; vitória só quando todos completos.

**Critério:** `test_objectives` passa; tela `VITORIA` após explore + comida + insetos + altar + escape.

---

## Tabela exercício → TODO

| Exercício | TODO(s) |
|-----------|---------|
| E1 | PROC-01 |
| E2 | TEX-02 |
| E3 | AUDIO-08 |
| E4 | NORM-03 |
| E5 | LIGHT-04 |
| E6 | CAM-02 |
| E7 | PROJ-05, HIT-06 |
| E8 | AI-07 |
| E9 | PICKUP-09, PLACE-10 |
| E10 | (benchmark) |
| E11 | (game_reset) |
| E12 | FONT-13 |
| E13 | HUD-14 |
| E14 | MENU-15 |
| E15 | WATER-12 |
| E16 | SLIME-11 |
| E17 | CHK-16 |
| E18 | OBJ-17 |
