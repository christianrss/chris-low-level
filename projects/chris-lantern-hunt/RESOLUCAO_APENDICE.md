# RESOLUCAO_APENDICE — Lantern Hunt (TODOs 09–17 + debug)

Continuação de RESOLUCAO_GUIADA_PASSO_A_PASSO.md (seções LANTERN-PICKUP-09 em diante).

---

## LANTERN-PICKUP-09 â€” Coleta de comida

**Arquivo:** `starter/src/game.cpp` â€” `update_pickups`.

**CÃ³digo completo:**

```cpp
void update_pickups(GameState& state) {
    for (FoodPickup& food : state.foods) {
        if (food.collected) continue;
        const float dx = state.camera.position.x - food.position.x;
        const float dy = state.camera.position.y - food.position.y;
        const float dz = state.camera.position.z - food.position.z;
        if (dx * dx + dy * dy + dz * dz < 0.9f * 0.9f) {
            food.collected = true;
            ++state.food_collected;
            state.objectives.on_food_collected(state.food_collected);
        }
    }
}
```

**Por que funciona?** Esfera de raio `0.9m` em torno do pickup; incrementa contador e notifica tracker de objetivos.

**VerificaÃ§Ã£o:** HUD `COMIDA x/5` incrementa ao passar perto do cubo emissivo.

**Checkpoint:** 5 coletas â†’ objetivo `CollectFood` completo.

---

## LANTERN-PLACE-10 â€” Spawn comida, insetos, altares

**Arquivo:** `starter/src/game.cpp` â€” `spawn_entities`, chamada de `game_reset`.

**CÃ³digo completo (estrutura):**

```cpp
void spawn_entities(GameState& state, std::mt19937& rng) {
    const auto floors = collect_spawn_cells(state.dungeon);
    std::uniform_int_distribution<std::size_t> floor_dist(0, floors.size() - 1);
    const auto spawn_cell = floors[floor_dist(rng)];
    state.camera.position = world_from_cell(spawn_cell.first, spawn_cell.second, kPlayerHeight * 0.5f);

    std::vector<std::pair<int, int>> food_candidates;
    for (const auto& cell : floors) {
        if (manhattan(cell.first, cell.second, spawn_cell.first, spawn_cell.second) >= 4) {
            food_candidates.push_back(cell);
        }
    }
    std::shuffle(food_candidates.begin(), food_candidates.end(), rng);
    for (int i = 0; i < kFoodToWin && i < static_cast<int>(food_candidates.size()); ++i) {
        FoodPickup food{};
        food.position = world_from_cell(food_candidates[i].first, food_candidates[i].second, 0.55f);
        state.foods.push_back(food);
    }
    // bugs: loop kMaxBugs, i%3==0 â†’ parede (ver LANTERN-AI-07)
    // altars: 2 primeiras salas, centro da room
}
```

**Por que funciona?** Manhattan â‰¥ 4 evita comida no spawn; shuffle com `rng` derivado de `seed ^ 0xA5A5A5A5` em `game_reset` separa layout de entidades.

**VerificaÃ§Ã£o:** nova partida seed 42 â€” 5 comidas, 12 insetos, 2 altares visÃ­veis.

**Checkpoint:** comida nÃ£o nasce em cima do jogador.

---

## LANTERN-SLIME-11 â€” Gosma, dano, overlay, partÃ­culas

**Arquivos:** `starter/src/game.cpp`, `starter/src/hud.cpp`  
**Localizar:** `update_water_state` case `Slime`, `spawn_slime_particles`, `update_slime_particles`, `draw_slime_overlay`.

**CÃ³digo completo (gosma no chÃ£o + overlay):**

```cpp
// game.cpp â€” case CellType::Slime em update_water_state
state.player.health -= 8.0f * delta_seconds;
state.player.slime_slow = 1.0f;
state.slime_overlay = 1.0f;

// hud.cpp
void draw_slime_overlay(float intensity) {
    if (intensity <= 0.01f) return;
    glDisable(GL_DEPTH_TEST);
    // ortho 0..1, quad fullscreen, glColor4f(0.1, 0.55, 0.15, intensity * 0.45)
    glEnable(GL_DEPTH_TEST);
}
```

Chame `draw_slime_overlay(g_game.slime_overlay)` em `main_win32.cpp` **antes** do HUD, apÃ³s cena 3D.

**Por que funciona?** Estado `slime_overlay` decai em `update_slime_particles`; overlay comunica dano quando lanterna nÃ£o mostra UI clara.

**VerificaÃ§Ã£o:** pise cÃ©lula verde (`Slime` no procgen) â€” tela verde, movimento lento.

**Checkpoint:** partÃ­culas ao matar inseto (`spawn_slime_particles`).

---

## LANTERN-WATER-12 â€” Ãgua, nataÃ§Ã£o, breath

**Arquivos:** `starter/src/procgen.cpp` (`carve_water_pool`, `is_walkable`), `starter/src/game.cpp` (`update_water_state`), `starter/src/collision.cpp` (deep block).

**CÃ³digo completo (`carve_water_pool`):**

```cpp
void carve_water_pool(Dungeon& dungeon, std::mt19937& rng) {
    if (dungeon.rooms.empty()) return;
    const Room& room = dungeon.rooms[rng() % dungeon.rooms.size()];
    const int pool_w = std::max(3, room.w / 2);
    const int pool_h = std::max(3, room.h / 2);
    const int start_x = room.x + (room.w - pool_w) / 2;
    const int start_y = room.y + (room.h - pool_h) / 2;
    for (int y = start_y; y < start_y + pool_h; ++y) {
        for (int x = start_x; x < start_x + pool_w; ++x) {
            const bool deep = x > start_x && x < start_x + pool_w - 1 &&
                              y > start_y && y < start_y + pool_h - 1;
            dungeon.cells[y * dungeon.width + x] = deep ? CellType::WaterDeep : CellType::WaterShallow;
        }
    }
}
```

Chame ao final de `generate_dungeon` (apÃ³s corredores). `update_water_state` conforme teoria (breath, `swimming`, `y=0.9`).

**Por que funciona?** Anel shallow permite entrar; miolo deep forÃ§a `swimming`; colisÃ£o bloqueia deep sem swim.

**VerificaÃ§Ã£o:** `test_procgen` assert `water_count() >= 8`.

**Checkpoint:** mergulhe â€” barra RESPIRACAO no HUD (`LANTERN-HUD-14`).

---

## LANTERN-FONT-13 â€” Fonte bitmap + ortho

**Arquivo:** `starter/src/font.cpp`  
**Localizar:** `FontRenderer::begin_frame`, `draw_text`, array `font5x7`.

**CÃ³digo completo (`begin_frame` + desenho de glyph):**

```cpp
void FontRenderer::begin_frame(int width, int height) {
    width_ = width;
    height_ = height;
    glMatrixMode(GL_PROJECTION);
    glPushMatrix();
    glLoadIdentity();
    glOrtho(0.0, static_cast<double>(width_), static_cast<double>(height_), 0.0, -1.0, 1.0);
    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    glLoadIdentity();
    glDisable(GL_DEPTH_TEST);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
}

void FontRenderer::draw_text(float x, float y, float scale, const char* text, float r, float g, float b) const {
    float cursor_x = x;
    const float pixel = 2.0f * scale;
    glColor4f(r, g, b, 1.0f);
    for (const char* ch = text; *ch; ++ch) {
        for (int row = 0; row < 7; ++row) {
            for (int col = 0; col < 5; ++col) {
                if (!glyph_pixel(*ch, col, row)) continue;
                float px = cursor_x + col * pixel;
                float py = y + row * pixel;
                glBegin(GL_QUADS);
                glVertex2f(px, py);
                glVertex2f(px + pixel, py);
                glVertex2f(px + pixel, py + pixel);
                glVertex2f(px, py + pixel);
                glEnd();
            }
        }
        cursor_x += (5 + 1) * pixel;
    }
}
```

Copie tabela `font5x7` de `solutions/src/font.cpp` (ASCII 32â€“90).

**Por que funciona?** OrtogrÃ¡fico alinha pixels da janela; cada bit do glyph vira quad â€” sem textura de fonte.

**VerificaÃ§Ã£o:** menu mostra â€œLANTERN HUNTâ€ legÃ­vel.

**Checkpoint:** `draw_bar` para barras (usado no HUD-14).

---

## LANTERN-HUD-14 â€” Vida, respiraÃ§Ã£o, objetivos

**Arquivo:** `starter/src/hud.cpp` â€” `HudRenderer::draw`.

**CÃ³digo completo:**

```cpp
void HudRenderer::draw(const GameState& state, FontRenderer& font, int width, int height) const {
    font.begin_frame(width, height);
    font.draw_bar(20.0f, static_cast<float>(height) - 40.0f, 220.0f, 18.0f,
        state.player.health / 100.0f, 0.85f, 0.2f, 0.2f);
    font.draw_text(24.0f, static_cast<float>(height) - 58.0f, 1.0f, "VIDA", 1, 1, 1);
    if (state.player.water != WaterState::None) {
        font.draw_bar(20.0f, static_cast<float>(height) - 78.0f, 220.0f, 18.0f,
            state.player.breath / 100.0f, 0.2f, 0.5f, 0.95f);
        font.draw_text(24.0f, static_cast<float>(height) - 96.0f, 1.0f, "RESPIRACAO", 0.8f, 0.9f, 1);
    }
    char food_line[64];
    std::snprintf(food_line, sizeof(food_line), "COMIDA %d/%d", state.food_collected, kFoodToWin);
    font.draw_text(20.0f, 20.0f, 1.2f, food_line, 1.0f, 0.9f, 0.5f);
    if (const Objective* active = state.objectives.active_objective()) {
        font.draw_text(20.0f, 48.0f, 1.1f, active->description, 0.95f, 0.95f, 0.95f);
    }
    font.end_frame();
}
```

**Por que funciona?** HUD lÃª apenas `GameState` â€” desacoplado da simulaÃ§Ã£o; objetivo ativo guia o jogador sem minimapa.

**VerificaÃ§Ã£o:** texto do objetivo atual muda ao completar cada etapa.

**Checkpoint:** entre na Ã¡gua â€” barra azul aparece.

---

## LANTERN-MENU-15 â€” GameScreen e menu principal

**Arquivos:** `starter/src/hud.cpp` (`MenuRenderer`), `starter/src/main_win32.cpp` (input + render branch).

**CÃ³digo completo (menu draw + seleÃ§Ã£o):**

```cpp
void MenuRenderer::draw_main_menu(const GameState& state, FontRenderer& font, int width, int height) const {
    font.begin_frame(width, height);
    font.draw_text(width * 0.32f, 120.0f, 2.0f, "LANTERN HUNT", 1.0f, 0.92f, 0.6f);
    const char* items[] = {"Jogar (seed 42)", "Jogar aleatorio", "Sair"};
    for (int i = 0; i < 3; ++i) {
        float y = 260.0f + i * 48.0f;
        float r = state.menu_selection == i ? 1.0f : 0.7f;
        font.draw_text(180.0f, y, 1.4f, items[i], r, r, 0.9f);
    }
    font.end_frame();
}
```

Em `main_win32.cpp`: se `screen == MainMenu`, desenhe menu e processe setas; Enter em item 0 â†’ `game_reset(g_game, 42)`; item 1 â†’ seed aleatÃ³ria; item 2 â†’ `quit_requested`.

**Por que funciona?** `game_update` retorna cedo se `screen != Playing` â€” simulaÃ§Ã£o pausada no menu.

**VerificaÃ§Ã£o:** boot mostra menu; Esc no jogo pausa (`draw_paused`).

**Checkpoint:** vitÃ³ria â†’ tela â€œVITORIA!â€ â†’ Enter â†’ menu.

---

## LANTERN-CHK-16 â€” Checkpoint nos altares

**Arquivos:** `starter/src/checkpoint.cpp`, `starter/src/game.cpp` (`try_activate_altar`).

**CÃ³digo completo:**

```cpp
void checkpoint_save(const GameState& state, CheckpointData& out) {
    out.valid = true;
    out.seed = state.seed;
    out.position = state.camera.position;
    out.health = state.player.health;
    out.breath = state.player.breath;
    out.food_collected = state.food_collected;
    out.bugs_killed = state.bugs_killed;
    out.rooms_visited = state.rooms_visited;
}

void try_activate_altar(GameState& state) {
    if (!state.interact_pressed) return;
    for (Altar& altar : state.altars) {
        float dx = state.camera.position.x - altar.position.x;
        float dz = state.camera.position.z - altar.position.z;
        if (dx * dx + dz * dz > 1.2f * 1.2f) continue;
        altar.activated = true;
        checkpoint_save(state, state.checkpoint);
        state.objectives.on_checkpoint_activated();
        break;
    }
}
```

Input: tecla `E` seta `interact_pressed = true` uma vez por frame.

**Por que funciona?** Snapshot mÃ­nimo restaura progresso sem serializar dungeon inteira (seed jÃ¡ fixa layout).

**VerificaÃ§Ã£o:** `.\build\Release\test_checkpoint.exe` â†’ `PASS`.

**Checkpoint:** morra apÃ³s altar â€” respawn com vida salva (`game_respawn_to_checkpoint`).

---

## LANTERN-OBJ-17 â€” Tracker e vitÃ³ria

**Arquivo:** `starter/src/objectives.cpp` + `game.cpp` (`update_victory_state`).

**CÃ³digo completo (`reset` + callbacks):**

```cpp
void ObjectiveTracker::reset() {
    objectives_ = {
        {ObjectiveId::ExploreRooms, "Explore 3 salas distintas", 3, 0, false},
        {ObjectiveId::CollectFood, "Colete 5 comidas", 5, 0, false},
        {ObjectiveId::KillBugs, "Elimine 4 insetos", 4, 0, false},
        {ObjectiveId::ActivateCheckpoint, "Ative um altar (tecla E)", 1, 0, false},
        {ObjectiveId::Escape, "Complete todos os objetivos", 1, 0, false},
    };
}

void ObjectiveTracker::on_escape_ready(bool ready) {
    if (objectives_.size() > 4) {
        objectives_[4].progress = ready ? 1 : 0;
    }
    advance_if_needed();
}
```

Em `update_victory_state`:

```cpp
const bool ready = state.objectives.all_complete();
state.objectives.on_escape_ready(ready);
if (ready) {
    state.won = true;
    state.screen = GameScreen::Victory;
}
```

Dispare `on_room_entered`, `on_food_collected`, etc. nos pontos jÃ¡ listados nos TODOs anteriores.

**Por que funciona?** Cadeia ordenada forÃ§a explorar antes de â€œescaparâ€; `all_complete` exige todos `completed`.

**VerificaÃ§Ã£o:** `.\build\Release\test_objectives.exe` â†’ `PASS`.

**Checkpoint:** partida completa manual â€” tela Victory apÃ³s 5 objetivos.

---

## Debug â€” mensagens tÃ­picas

| Erro | CorreÃ§Ã£o |
|------|----------|
| Shader files not found | Rebuild CMake (`LANTERN_SHADER_DIR`) |
| Failed to load texture | `python tools/generate_assets.py` |
| miniaudio init failed | Verifique `assets/audio/*.wav` |
| test_procgen FAIL water | Implemente `carve_water_pool` + `water_count()` |
| test_procgen FAIL cells | OrdenaÃ§Ã£o de salas ou RNG diferente da soluÃ§Ã£o |
| HUD invisÃ­vel | `g_hud.draw` apÃ³s cena 3D; `font.initialize()` |
| Menu nÃ£o responde | Tratar `WM_KEYDOWN` sÃ³ quando `screen == MainMenu` |
| VitÃ³ria instantÃ¢nea | NÃ£o chamar `on_escape_ready(true)` antes dos outros objetivos |

---

## RelatÃ³rio de resoluÃ§Ã£o (template)

```markdown
## Lantern Hunt â€” resoluÃ§Ã£o
- Data: ___
- Seed testada: 42
- test_procgen: PASS/FAIL
- test_collision: PASS/FAIL
- test_objectives: PASS/FAIL
- test_checkpoint: PASS/FAIL
- ctest -C Release: PASS/FAIL
- FPS mÃ©dio 60s: ___
- TODO que mais custou tempo: ___
- PrÃ³ximo passo: instancing / PBR / pathfinding
```

---

## Ordem sugerida de implementaÃ§Ã£o

1. PROC-01 â†’ test_procgen (parcial)
2. CAM-02 â†’ test_collision
3. TEX-02 + NORM-03 + LIGHT-04 â†’ render legÃ­vel
4. AUDIO-08 â†’ feedback sonoro
5. PROJ-05 â†’ HIT-06 â†’ AI-07 â†’ PLACE-10 â†’ PICKUP-09
6. WATER-12 â†’ test_procgen completo
7. FONT-13 â†’ HUD-14 â†’ MENU-15
8. SLIME-11 â†’ polish combate
9. CHK-16 â†’ test_checkpoint
10. OBJ-17 â†’ test_objectives â†’ playthrough vitÃ³ria

Cada checkpoint intermediÃ¡rio evita depurar 18 sistemas simultÃ¢neos no fim do dia.
