# START_HERE — Lantern Hunt (dia intenso estendido)

## Objetivo do dia

Construir um FPS horror **jogável e completo** com:

- dungeon **procedural** determinística (seed reproduzível + opção aleatória no menu);
- paredes/chão com **albedo + normal map** e **lanterna** spotlight;
- **áudio** ambiente, passos e tiro;
- **água** (raso/profundo), **gosma**, dano e partículas;
- **HUD** (vida, respiração, comida, objetivo ativo);
- **menu** (Jogar seed 42 / aleatório / Sair) e pausa;
- **checkpoints** em altares (tecla E);
- **5 objetivos** encadeados → vitória.

Tempo estimado: **18–22 h** focadas (inclui leitura de teoria, 18 TODOs, 4 testes `ctest` e checklist manual).

---

## Ordem de estudo

1. [`README.md`](README.md) — visão geral e controles
2. [`TEORIA_PASSO_A_PASSO.md`](TEORIA_PASSO_A_PASSO.md) — conceitos (≥320 linhas)
3. [`PESQUISA_GUIADA.md`](PESQUISA_GUIADA.md) — 10 perguntas com links
4. [`EXERCICIOS.md`](EXERCICIOS.md) — E1–E18 por dificuldade
5. Implemente em `starter/` seguindo os IDs `LANTERN-*`
6. [`TESTES_GUIADOS.md`](TESTES_GUIADOS.md) — automático + manual
7. Compare com `solutions/` **depois** de tentar
8. [`RESOLUCAO_GUIADA_PASSO_A_PASSO.md`](RESOLUCAO_GUIADA_PASSO_A_PASSO.md) se travar (+ [`RESOLUCAO_APENDICE.md`](RESOLUCAO_APENDICE.md))
9. [`BENCHMARK_GUIADO.md`](BENCHMARK_GUIADO.md) — FPS e timing dos 4 testes

---

## Baseline (antes dos TODOs)

```powershell
cd projects/chris-lantern-hunt
python tools/generate_assets.py
cmake -S . -B build -A x64
cmake --build build --config Release
.\build\Release\test_procgen.exe       # FAIL no starter até LANTERN-PROC-01 (+ WATER-12)
.\build\Release\test_collision.exe     # FAIL até LANTERN-CAM-02
.\build\Release\test_objectives.exe    # FAIL até LANTERN-OBJ-17
.\build\Release\test_checkpoint.exe    # FAIL até LANTERN-CHK-16
.\build\Release\lantern_hunt_starter.exe
```

**Solutions de referência:**

```powershell
.\build\Release\lantern_hunt.exe
cd build
ctest -C Release --output-on-failure
```

---

## Mapa completo — 18 TODOs

| ID | Arquivo(s) principal(is) | Teste / verificação |
|----|--------------------------|---------------------|
| LANTERN-PROC-01 | `starter/src/procgen.cpp` | `test_procgen` (layout) |
| LANTERN-CAM-02 | `starter/src/collision.cpp` | `test_collision` |
| LANTERN-TEX-02 | `starter/src/texture.cpp` | chão texturizado |
| LANTERN-NORM-03 | `starter/src/shaders/scene.frag.glsl` | relevo na parede |
| LANTERN-LIGHT-04 | `starter/src/main_win32.cpp` + shader | cone estreito |
| LANTERN-PROJ-05 | `starter/src/game.cpp` | disparo bolinha |
| LANTERN-HIT-06 | `starter/src/game.cpp` | inseto eliminado |
| LANTERN-AI-07 | `starter/src/game.cpp` | patrol + dano |
| LANTERN-AUDIO-08 | `starter/src/audio.cpp` | ambiente + passos |
| LANTERN-PICKUP-09 | `starter/src/game.cpp` | COMIDA x/5 |
| LANTERN-PLACE-10 | `starter/src/game.cpp` | spawn entidades |
| LANTERN-SLIME-11 | `starter/src/game.cpp`, `starter/src/hud.cpp` | overlay verde |
| LANTERN-WATER-12 | `procgen.cpp`, `game.cpp`, `collision.cpp` | `water_count` no teste |
| LANTERN-FONT-13 | `starter/src/font.cpp` | texto no menu |
| LANTERN-HUD-14 | `starter/src/hud.cpp` | barras vida/respiração |
| LANTERN-MENU-15 | `hud.cpp`, `main_win32.cpp` | `GameScreen` |
| LANTERN-CHK-16 | `starter/src/checkpoint.cpp` | `test_checkpoint` |
| LANTERN-OBJ-17 | `starter/src/objectives.cpp` | `test_objectives` |

---

## Cronograma sugerido (~18–22 h)

| Bloco | Horas | Conteúdo |
|-------|-------|----------|
| Manhã 1 | 3–4 | Teoria + PROC-01 + CAM-02 + ctest parcial |
| Manhã 2 | 3–4 | TEX-02, NORM-03, LIGHT-04, render jogável |
| Tarde 1 | 3–4 | AUDIO-08, PROJ/HIT/AI, PLACE, PICKUP |
| Tarde 2 | 3–4 | WATER-12, SLIME-11, test_procgen completo |
| Noite 1 | 3–4 | FONT-13, HUD-14, MENU-15 |
| Noite 2 | 2–3 | CHK-16, OBJ-17, ctest 4/4, checklist manual, benchmark |

---

## Quatro comandos ctest

Execute na pasta `build` após build Release:

```powershell
ctest -C Release -R lantern_procgen_seed42 --output-on-failure
ctest -C Release -R lantern_collision_slide --output-on-failure
ctest -C Release -R lantern_objectives_flow --output-on-failure
ctest -C Release -R lantern_checkpoint_save --output-on-failure
```

Ou todos de uma vez:

```powershell
ctest -C Release --output-on-failure
```

---

## Critério de “dia completo”

- [ ] Os **4** testes `ctest` passam no target `starter` (ou você documentou divergência consciente)
- [ ] `lantern_hunt_starter.exe`: texturas, normais, som, água, HUD, menu
- [ ] Vitória após completar **todos** os objetivos (não só 5 comidas)
- [ ] Altar salva checkpoint; morte pode restaurar progresso
- [ ] FPS estável (>45 em dungeon 32×32) — ver `docs/BENCHMARK_GUIADO.md`

---

## Controles (referência rápida)

| Tecla | Ação |
|-------|------|
| WASD | Movimento |
| Mouse | Olhar |
| Clique esquerdo | Disparar |
| E | Ativar altar (checkpoint) |
| Esc | Pausar / continuar (em jogo) |
| Setas / W-S | Menu (navegação) |
| Enter | Confirmar menu / voltar após Game Over |
| R | Regenerar dungeon (em jogo, se implementado) |

---

## Próximo passo após o dia

- Instancing / mesh merge (`BENCHMARK_GUIADO` motivação)
- Pathfinding nos insetos
- Portar bootstrap WGL para o padrão `chris-renderer` com GL 3.3+
