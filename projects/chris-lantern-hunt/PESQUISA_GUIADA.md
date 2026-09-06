# PESQUISA_GUIADA — Lantern Hunt

Perguntas para investigar **antes** ou **durante** a implementação. Registre respostas em notas próprias (template em `docs/RESEARCH_NOTE_TEMPLATE.md` do repositório raiz, se quiser formalizar).

---

## P1 — Tangent space e normal mapping

**Pergunta:** Por que normal maps são armazenados em tangent space e não em world space? O que acontece com a iluminação se você aplicar `texture2D(u_normal_map).rgb` diretamente em `dot(N, L)` sem TBN?

**Onde olhar no projeto:**
- `starter/src/shaders/scene.vert.glsl` — construção de `v_tbn`
- `starter/src/shaders/scene.frag.glsl` — `LANTERN-NORM-03`

**Links:**
- [LearnOpenGL — Normal Mapping](https://learnopengl.com/Advanced-Lighting/Normal-Mapping)
- [LearnOpenGL — Tangent space](https://learnopengl.com/Advanced-Lighting/Normal-Mapping#tangent-space)

**Critério de compreensão:** você consegue desenhar no papel os vetores T, B, N numa face de cubo e explicar por que Gram-Schmidt em T é necessário.

---

## P2 — Spotlight vs point light

**Pergunta:** Qual a diferença entre `dot(-L, light_dir)` e `dot(N, L)` no fragment shader? Por que `u_spot_cutoff = 0.92` corresponde a um cone estreito (~25°)?

**Onde olhar:**
- `solutions/src/shaders/scene.frag.glsl` — bloco `theta` / `spot`
- `solutions/src/main_win32.cpp` — uniforms `u_ambient`, `u_spot_cutoff`, `u_spot_exponent`

**Links:**
- [LearnOpenGL — Light casters (spotlights)](https://learnopengl.com/Lighting/Light-casters)

**Critério:** calcule `acos(0.92)` em radianos e graus; explique o papel de `pow(theta, exponent)`.

---

## P3 — AABB slide em grid FPS

**Pergunta:** Por que `move_with_collision` faz **dois passes** sobre o grid em vez de um? O que acontece num canto de corredor se você resolver só o eixo X?

**Onde olhar:**
- `starter/src/collision.cpp` — `resolve_axis`, `move_with_collision`
- `solutions/tests/test_collision.cpp`

**Links:**
- [LearnOpenGL — Coordinate Systems (câmera FPS)](https://learnopengl.com/Getting-started/Camera)
- Artigo clássico: *"Simple AABB vs AABB collision"* (busque referências sobre separação de eixos)

**Critério:** trace manualmente posição `(1.1, 0, 1.1)` contra parede em `(1, 0, 1)` com raio `0.32`.

---

## P4 — Procgen determinística com `std::mt19937`

**Pergunta:** Por que ordenar salas por `x` antes de conectar corredores faz parte da **reprodutibilidade**? O que mudaria se você conectasse na ordem de inserção?

**Onde olhar:**
- `starter/src/procgen.cpp` — `generate_dungeon`
- `solutions/tests/test_procgen.cpp` — assert célula a célula

**Links:**
- [cppreference — mt19937](https://en.cppreference.com/w/cpp/numeric/random/mersenne_twister_engine)
- [Roguelike room generation tutorials](https://rogueliketutorials.com/) (conceitos de salas + corredores)

**Critério:** com seed `42`, anote `floor_count`, `rooms.size()` e `water_count` após implementar `LANTERN-WATER-12`.

---

## P5 — miniaudio: stream vs buffer

**Pergunta:** Por que `ambient_dark.wav` usa `MA_SOUND_FLAG_STREAM` e `footstep.wav` não? Qual o trade-off de RAM vs latência?

**Onde olhar:**
- `starter/src/audio.cpp` — `LANTERN-AUDIO-08`
- `third_party/miniaudio.h` — documentação inline de `ma_sound_init_from_file`

**Links:**
- [miniaudio — Getting Started](https://miniaud.io/docs/manual/index.html)
- [miniaudio — High-level API (sounds)](https://miniaud.io/docs/manual/index.html#high-level-api)

**Critério:** explique por que `ma_sound_seek_to_pcm_frame(0)` + `ma_sound_start` implementa one-shot sem realocar.

---

## P6 — Bitmap font vs stb_truetype

**Pergunta:** O projeto usa fonte 5×7 embutida em `font.cpp` em vez de rasterizar TTF. Quando `stb_truetype` valeria a pena? Como a projeção ortográfica mapeia pixels de tela para quads GL?

**Onde olhar:**
- `starter/src/font.cpp` — `LANTERN-FONT-13`
- `third_party/stb_truetype.h` — header-only alternativo

**Links:**
- [stb_truetype — README no repositório nothings/stb](https://github.com/nothings/stb/blob/master/stb_truetype.h)
- [LearnOpenGL — Text Rendering (conceito de atlas)](https://learnopengl.com/In-Practice/Text-Rendering)

**Critério:** descreva `glOrtho(0, width, height, 0, ...)` e por que Y cresce para baixo na tela.

---

## P7 — Mecânica de natação e breath meter

**Pergunta:** Por que `WaterDeep` exige `swimming = true` para `is_walkable`, mas `WaterShallow` não? Como o breath meter evita morte instantânea sem ser irrelevante?

**Onde olhar:**
- `starter/src/procgen.hpp` — `CellType::WaterShallow`, `WaterDeep`
- `solutions/src/game.cpp` — `update_water_state`
- `solutions/src/collision.cpp` — bloqueio de deep water sem natação

**Links:**
- [Game Maker's Toolkit — underwater levels (design)](https://www.youtube.com/results?search_query=gmtk+underwater) (referência de design, não código)
- Busque "oxygen meter game design" para comparar taxas de dreno/recuperação

**Critério:** tabule taxas em `update_water_state` (`breath -= 18`, `+= 25` shallow, `+= 30` ar) e estime segundos até breath zero.

---

## P8 — State machine de objetivos

**Pergunta:** `ObjectiveTracker` é uma máquina de estados implícita (lista ordenada) ou explícita? Por que `on_escape_ready` só completa o último objetivo quando **todos** os anteriores estão `completed`?

**Onde olhar:**
- `starter/src/objectives.cpp` — `LANTERN-OBJ-17`
- `solutions/tests/test_objectives.cpp`

**Links:**
- [Game Programming Patterns — State](https://gameprogrammingpatterns.com/state.html)
- [Game Programming Patterns — Object Pool](https://gameprogrammingpatterns.com/object-pool.html) (paralelo com pool de projéteis)

**Critério:** desenhe diagrama de transições dos 5 objetivos e qual evento dispara cada `on_*`.

---

## P9 — Checkpoints como snapshot de estado

**Pergunta:** O que **não** é salvo em `checkpoint_save` e por quê (ex.: posição de insetos, projéteis ativos)? Quando `game_respawn_to_checkpoint` é preferível a `game_reset`?

**Onde olhar:**
- `starter/src/checkpoint.cpp` — `LANTERN-CHK-16`
- `solutions/src/game.cpp` — `try_activate_altar`, `game_respawn_to_checkpoint`

**Links:**
- [LearnOpenGL — Framebuffers](https://learnopengl.com/Advanced-OpenGL/Framebuffers) (conceito de snapshot; não usado aqui, mas útil para comparar)

**Critério:** liste campos em `CheckpointData` e justifique cada um pedagogicamente.

---

## P10 — WGL e carregamento de extensões OpenGL 2.0

**Pergunta:** Por que `wglGetProcAddress` é necessário para `glCreateShader` mas não para `glClear`? O que falha se `LANTERN_SHADER_DIR` apontar para a pasta errada?

**Onde olhar:**
- `solutions/src/main_win32.cpp` — `load_gl_functions`, `initialize_wgl`
- `projects/chris-renderer/opengl_win32/main.cpp` (referência do portfólio)

**Links:**
- [OpenGL Wiki — Loading OpenGL functions on Windows](https://www.khronos.org/opengl/wiki/Load_OpenGL_Functions)
- [LearnOpenGL — Hello Window](https://learnopengl.com/Getting-started/Hello-Window)

**Critério:** enumere pelo menos 5 funções GL carregadas via `wglGetProcAddress` no projeto.

---

## Como usar esta pesquisa

1. Escolha 2–3 perguntas **antes** de cada bloco de TODOs (ex.: P1+P2 antes de NORM/LIGHT).
2. Escreva 5–10 linhas de resposta com referência ao arquivo que você abriu.
3. Ao terminar o dia, revise: alguma resposta mudou depois de implementar?
