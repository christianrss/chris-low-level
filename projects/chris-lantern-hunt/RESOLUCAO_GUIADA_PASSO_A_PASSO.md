# RESOLUCAO_GUIADA_PASSO_A_PASSO — Lantern Hunt

Passo a passo operacional para os **18 TODOs** do projeto. Use **depois** de tentar em `starter/`; compare sempre com `solutions/` para nuances.

---

## Mapa exato starter → solutions

| TODO ID | starter | solutions |
|---------|---------|-----------|
| LANTERN-PROC-01 | `starter/src/procgen.cpp` | `solutions/src/procgen.cpp` |
| LANTERN-CAM-02 | `starter/src/collision.cpp` | `solutions/src/collision.cpp` |
| LANTERN-TEX-02 | `starter/src/texture.cpp` | `solutions/src/texture.cpp` |
| LANTERN-NORM-03 | `starter/src/shaders/scene.frag.glsl` | `solutions/src/shaders/scene.frag.glsl` |
| LANTERN-LIGHT-04 | `starter/src/main_win32.cpp` + shader | `solutions/src/main_win32.cpp` |
| LANTERN-PROJ-05 | `starter/src/game.cpp` | `solutions/src/game.cpp` |
| LANTERN-HIT-06 | `starter/src/game.cpp` | `solutions/src/game.cpp` |
| LANTERN-AI-07 | `starter/src/game.cpp` | `solutions/src/game.cpp` |
| LANTERN-AUDIO-08 | `starter/src/audio.cpp` | `solutions/src/audio.cpp` |
| LANTERN-PICKUP-09 | `starter/src/game.cpp` | `solutions/src/game.cpp` |
| LANTERN-PLACE-10 | `starter/src/game.cpp` | `solutions/src/game.cpp` |
| LANTERN-SLIME-11 | `starter/src/game.cpp`, `starter/src/hud.cpp` | `solutions/src/game.cpp`, `solutions/src/hud.cpp` |
| LANTERN-WATER-12 | `starter/src/procgen.cpp`, `starter/src/game.cpp`, `starter/src/collision.cpp` | idem em `solutions/` |
| LANTERN-FONT-13 | `starter/src/font.cpp` | `solutions/src/font.cpp` |
| LANTERN-HUD-14 | `starter/src/hud.cpp`, `starter/src/font.cpp` | `solutions/src/hud.cpp` |
| LANTERN-MENU-15 | `starter/src/hud.cpp`, `starter/src/main_win32.cpp` | `solutions/src/hud.cpp`, `main_win32.cpp` |
| LANTERN-CHK-16 | `starter/src/checkpoint.cpp`, `starter/src/game.cpp` | `solutions/src/checkpoint.cpp` |
| LANTERN-OBJ-17 | `starter/src/objectives.cpp`, `starter/src/game.cpp` | `solutions/src/objectives.cpp` |

---

## Baseline (antes dos TODOs)

```powershell
cd days/2026-09-06/graphics/lantern_hunt
python tools/generate_assets.py
cmake -S . -B build -A x64
cmake --build build --config Release
```

**Saída esperada no starter (FAIL parcial):**

| Comando | Starter | Solutions |
|---------|---------|-----------|
| `.\build\Release\test_procgen.exe` | FAIL (grid só parede ou layout vazio) | `PASS seed=42 floors=... rooms=...` |
| `.\build\Release\test_collision.exe` | FAIL se colisão stub | `PASS` |
| `.\build\Release\test_objectives.exe` | FAIL | `PASS` |
| `.\build\Release\test_checkpoint.exe` | FAIL | `PASS` |
| `.\build\Release\lantern_hunt_starter.exe` | Abre; cinza, sem gameplay completo | Jogo completo |

**CTest (4 testes):**

```powershell
cd build
ctest -C Release --output-on-failure
```

Nomes: `lantern_procgen_seed42`, `lantern_collision_slide`, `lantern_objectives_flow`, `lantern_checkpoint_save`.

---

## LANTERN-PROC-01 — Procgen determinística

**Arquivo:** `starter/src/procgen.cpp`  
**Localizar:** função `generate_dungeon(std::uint32_t seed)` — substituir stub que deixa grid só com uma sala central.

**Código completo (núcleo):**

```cpp
Dungeon generate_dungeon(std::uint32_t seed) {
    Dungeon dungeon{};
    dungeon.seed = seed;
    dungeon.width = kDungeonWidth;
    dungeon.height = kDungeonHeight;
    dungeon.cells.assign(static_cast<std::size_t>(dungeon.width * dungeon.height), CellType::Wall);

    std::mt19937 rng(seed);
    std::uniform_int_distribution<int> room_w_dist(4, 7);
    std::uniform_int_distribution<int> room_h_dist(4, 7);
    std::uniform_int_distribution<int> x_dist(1, dungeon.width - 8);
    std::uniform_int_distribution<int> y_dist(1, dungeon.height - 8);

    constexpr int kTargetRooms = 8;
    constexpr int kMaxAttempts = 120;

    for (int attempt = 0; attempt < kMaxAttempts && static_cast<int>(dungeon.rooms.size()) < kTargetRooms; ++attempt) {
        Room room{};
        room.w = room_w_dist(rng);
        room.h = room_h_dist(rng);
        room.x = x_dist(rng);
        room.y = y_dist(rng);
        if (room.x + room.w >= dungeon.width - 1 || room.y + room.h >= dungeon.height - 1) {
            continue;
        }
        bool blocked = false;
        for (const Room& existing : dungeon.rooms) {
            if (overlaps(room, existing, 2)) {
                blocked = true;
                break;
            }
        }
        if (blocked) {
            continue;
        }
        carve_room(dungeon, room);
        dungeon.rooms.push_back(room);
    }

    std::sort(dungeon.rooms.begin(), dungeon.rooms.end(),
        [](const Room& a, const Room& b) { return a.x < b.x; });

    for (std::size_t i = 1; i < dungeon.rooms.size(); ++i) {
        const Room& prev = dungeon.rooms[i - 1];
        const Room& current = dungeon.rooms[i];
        const int prev_cx = prev.x + prev.w / 2;
        const int prev_cy = prev.y + prev.h / 2;
        const int cur_cx = current.x + current.w / 2;
        const int cur_cy = current.y + current.h / 2;
        if (rng() % 2 == 0) {
            carve_h_corridor(dungeon, prev_cx, cur_cx, prev_cy);
            carve_v_corridor(dungeon, prev_cy, cur_cy, cur_cx);
        } else {
            carve_v_corridor(dungeon, prev_cy, cur_cy, prev_cx);
            carve_h_corridor(dungeon, prev_cx, cur_cx, cur_cy);
        }
    }
    return dungeon;
}
```

Implemente também `carve_h_corridor`, `carve_v_corridor`, `carve_room`, `overlaps` no namespace anônimo (copie estrutura de `solutions/src/procgen.cpp`).

**Por que funciona?** `mt19937(seed)` gera a mesma sequência de retângulos e decisões L; `std::sort` por `x` fixa ordem de corredores — duas chamadas com seed `42` produzem `cells` idênticos byte a byte.

**Verificação:**

```powershell
cmake --build build --config Release --target test_procgen
.\build\Release\test_procgen.exe
```

**Checkpoint:** saída `test_procgen: PASS seed=42 floors=... rooms=...` (≥6 salas, ≥180 floors). Água ainda pode falhar até `LANTERN-WATER-12`.

---

## LANTERN-CAM-02 — Colisão AABB slide

**Arquivo:** `starter/src/collision.cpp`  
**Localizar:** `move_with_collision`, `resolve_axis`, `player_aabb`, `sphere_hits_aabb`.

**Código completo (`resolve_axis` + loop principal):**

```cpp
Vec3 resolve_axis(const Aabb& player, const Aabb& wall, const Vec3& position) {
    Vec3 resolved = position;
    if (!aabb_intersects(player, wall)) {
        return resolved;
    }
    const float overlap_x1 = wall.max.x - player.min.x;
    const float overlap_x2 = player.max.x - wall.min.x;
    const float overlap_z1 = wall.max.z - player.min.z;
    const float overlap_z2 = player.max.z - wall.min.z;

    if (std::min(overlap_x1, overlap_x2) < std::min(overlap_z1, overlap_z2)) {
        resolved.x += (overlap_x1 < overlap_x2) ? overlap_x1 : -overlap_x2;
    } else {
        resolved.z += (overlap_z1 < overlap_z2) ? overlap_z1 : -overlap_z2;
    }
    return resolved;
}

Vec3 move_with_collision(const Dungeon& dungeon, const Vec3& position, const Vec3& delta,
    float radius, float height, float cell_size, bool swimming) {
    Vec3 result = position + delta;
    constexpr float kWallHeight = 3.0f;
    constexpr int kPasses = 2;

    for (int pass = 0; pass < kPasses; ++pass) {
        for (int y = 0; y < dungeon.height; ++y) {
            for (int x = 0; x < dungeon.width; ++x) {
                const CellType cell = dungeon.at(x, y);
                if (cell != CellType::Wall) {
                    if (cell == CellType::WaterDeep && !swimming) {
                        Aabb block = wall_aabb(x, y, cell_size, kWallHeight);
                        result = resolve_axis(player_aabb(result, radius, height), block, result);
                    }
                    continue;
                }
                Aabb wall = wall_aabb(x, y, cell_size, kWallHeight);
                result = resolve_axis(player_aabb(result, radius, height), wall, result);
            }
        }
    }
    return result;
}
```

**Por que funciona?** Resolver o eixo de **menor penetração** empurra o jogador para fora da parede sem cancelar movimento perpendicular — dois passes corrigem cantos.

**Verificação:** `.\build\Release\test_collision.exe` → `test_collision: PASS`.

**Checkpoint:** no executável, ande em diagonal contra canto — não atravessa, desliza.

---

## LANTERN-TEX-02 — Texturas stb_image

**Arquivo:** `starter/src/texture.cpp`  
**Localizar:** `load_texture_2d`.

**Código completo:**

```cpp
#define STB_IMAGE_IMPLEMENTATION
#include "../../third_party/stb_image.h"

unsigned int load_texture_2d(const std::string& path, bool srgb_repeat) {
    int width = 0, height = 0, channels = 0;
    stbi_set_flip_vertically_on_load(1);
    unsigned char* pixels = stbi_load(path.c_str(), &width, &height, &channels, 4);
    if (pixels == nullptr) {
        std::cerr << "Failed to load texture: " << path << '\n';
        return 0;
    }
    unsigned int texture_id = 0;
    glGenTextures(1, &texture_id);
    glBindTexture(GL_TEXTURE_2D, texture_id);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, srgb_repeat ? GL_REPEAT : GL_CLAMP);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, srgb_repeat ? GL_REPEAT : GL_CLAMP);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels);
    stbi_image_free(pixels);
    return texture_id;
}
```

**Por que funciona?** CPU decodifica PNG; GPU armazena texels; fragment shader sample por `v_uv` com unidade `GL_TEXTURE0`.

**Verificação:** rode `lantern_hunt_starter.exe` — chão/parede com padrão, não cinza uniforme.

**Checkpoint:** stderr sem `Failed to load texture` (assets gerados).

---

## LANTERN-NORM-03 — Normal map + TBN

**Arquivo:** `starter/src/shaders/scene.frag.glsl`  
**Localizar:** comentário `TODO LANTERN-NORM-03`.

**Código completo (substituir uso de `v_normal` plano):**

```glsl
vec3 tangent_normal = texture2D(u_normal_map, v_uv).rgb * 2.0 - 1.0;
vec3 N = normalize(v_tbn * tangent_normal);

vec3 L = normalize(u_light_pos - v_world_pos);
float theta = dot(-L, normalize(u_light_dir));
float spot = (theta > u_spot_cutoff) ? pow(theta, u_spot_exponent) : 0.0;
float diff = max(dot(N, L), 0.0) * spot;
vec3 lighting = u_ambient + diff * u_light_color;
gl_FragColor = vec4(albedo * lighting, 1.0);
```

Vertex shader `scene.vert.glsl` já monta `v_tbn` — não altere se igual ao starter.

**Por que funciona?** `v_tbn` leva perturbação do espaço tangente para mundo; `dot(N,L)` reage ao relevo falso do normal map.

**Verificação:** aponte lanterna para parede — rachaduras do `wall_normal.png` visíveis no cone.

**Checkpoint:** compare com `u_normal_map` desligado (comentar sample) — parede fica lisa.

---

## LANTERN-LIGHT-04 — Spotlight + ambiente escuro

**Arquivo:** `starter/src/main_win32.cpp` (loop de render)  
**Localizar:** uniforms após `pglUseProgram`.

**Código completo:**

```cpp
const lantern::Vec3 light_pos = g_game.camera.position;
const lantern::Vec3 light_dir = g_game.camera.forward();
pglUniform3f(light_pos_uniform, light_pos.x, light_pos.y, light_pos.z);
pglUniform3f(light_dir_uniform, light_dir.x, light_dir.y, light_dir.z);
pglUniform3f(light_color_uniform, 1.0f, 0.92f, 0.72f);
pglUniform3f(view_pos_uniform, g_game.camera.position.x, g_game.camera.position.y, g_game.camera.position.z);
pglUniform1f(ambient_uniform, 0.03f);
pglUniform1f(cutoff_uniform, 0.92f);
pglUniform1f(exponent_uniform, 48.0f);
```

**Por que funciona?** `theta = dot(-L, light_dir)` mede alinhamento com o cone; `cutoff` alto + `exponent` grande estreitam o feixe; `ambient` baixo mantém horror.

**Verificação:** olhe corredor lateral sem girar câmera — quase preto.

**Checkpoint:** `acos(0.92) ≈ 23°` semiângulo — anote no caderno.

---

## LANTERN-PROJ-05 — Pool de projéteis

**Arquivo:** `starter/src/game.cpp`  
**Localizar:** `fire_projectile`, `acquire_projectile`, chamada em `game_update` quando `shoot_pressed`.

**Código completo:**

```cpp
Projectile* acquire_projectile(GameState& state) {
    for (Projectile& projectile : state.projectiles) {
        if (!projectile.active) {
            return &projectile;
        }
    }
    return nullptr;
}

void fire_projectile(GameState& state) {
    Projectile* projectile = acquire_projectile(state);
    if (projectile == nullptr) {
        return;
    }
    const Vec3 dir = state.camera.forward();
    projectile->active = true;
    projectile->position = state.camera.position + dir * 0.4f;
    projectile->velocity = dir * 14.0f;
    projectile->lifetime = 2.5f;
}
```

Em `update_projectiles` (criar se ausente): mover `position += velocity * dt`, decrementar `lifetime`, desativar se `cell == Wall`.

**Por que funciona?** Pool fixo `kMaxProjectiles` evita alocação; direção da câmera alinha “bolinha de gude” com mira FPS.

**Verificação:** clique esquerdo — esfera amarela sai da lanterna; para na parede.

**Checkpoint:** dispare 20 vezes rápido — no máximo 16 ativos (pool).

---

## LANTERN-HIT-06 — Projétil × inseto

**Arquivo:** `starter/src/game.cpp` — dentro de `update_projectiles`, loop sobre `state.bugs`.

**Código completo:**

```cpp
const Aabb bug_box{
    {bug.position.x - 0.35f, bug.position.y - 0.35f, bug.position.z - 0.35f},
    {bug.position.x + 0.35f, bug.position.y + 0.35f, bug.position.z + 0.35f},
};
if (sphere_hits_aabb(projectile.position, 0.12f, bug_box)) {
    bug.alive = false;
    projectile.active = false;
    ++state.bugs_killed;
    state.objectives.on_bug_killed(state.bugs_killed);
    spawn_slime_particles(state, bug.position);
    break;
}
```

**Por que funciona?** `sphere_hits_aabb` (em `collision.cpp`) testa distância ao ponto mais próximo do AABB — barato e suficiente para hitbox de inseto.

**Verificação:** acerte inseto — some, contador de objetivos “Elimine 4 insetos” avança.

**Checkpoint:** `test_collision` já valida `sphere_hits_aabb` indiretamente via link.

---

## LANTERN-AI-07 — Patrol + dano por contato

**Arquivo:** `starter/src/game.cpp` — `update_bugs`.

**Código completo:**

```cpp
void update_bugs(GameState& state, float delta_seconds) {
    for (Bug& bug : state.bugs) {
        if (!bug.alive) continue;
        bug.t += delta_seconds * 0.35f;
        const float blend = 0.5f + 0.5f * std::sin(bug.t * 6.28318f);
        bug.position = bug.patrol_a * (1.0f - blend) + bug.patrol_b * blend;

        const float dx = state.camera.position.x - bug.position.x;
        const float dz = state.camera.position.z - bug.position.z;
        if (dx * dx + dz * dz < 0.7f * 0.7f) {
            state.player.health -= 12.0f * delta_seconds;
            state.player.slime_slow = 1.0f;
            state.slime_overlay = 1.0f;
            spawn_slime_particles(state, bug.position);
        }
    }
}
```

Em `spawn_entities` (`PLACE-10`), para `i % 3 == 0` configure `BugSurface::WallNorth` etc. com posição na face da célula.

**Por que funciona?** Interpolação senoidal entre `patrol_a` e `patrol_b` dá movimento ida-e-volta; distância 2D ignora Y para contato “no chão”.

**Verificação:** seed 42 — pelo menos 3 insetos em paredes; encoste — vida cai.

**Checkpoint:** mate 4 insetos para objetivo `KillBugs`.

---

## LANTERN-AUDIO-08 — miniaudio

**Arquivo:** `starter/src/audio.cpp`  
**Localizar:** `AudioEngine::initialize`, `play_footstep`, `update_movement_cooldown`.

**Código completo (`initialize` + footstep):**

```cpp
#define MINIAUDIO_IMPLEMENTATION
#include "../../third_party/miniaudio.h"

constexpr float kFootstepCooldownSeconds = 0.35f;

bool AudioEngine::initialize(const std::string& ambient_path,
    const std::string& footstep_path, const std::string& shoot_path) {
    if (ma_engine_init(nullptr, &engine) != MA_SUCCESS) {
        return false;
    }
    if (ma_sound_init_from_file(&engine, ambient_path.c_str(), MA_SOUND_FLAG_STREAM,
            nullptr, nullptr, &ambient_sound) != MA_SUCCESS) {
        ma_engine_uninit(&engine);
        return false;
    }
    ma_sound_set_looping(&ambient_sound, MA_TRUE);
    ma_sound_start(&ambient_sound);
    ma_sound_init_from_file(&engine, footstep_path.c_str(), 0, nullptr, nullptr, &footstep_sound);
    ma_sound_init_from_file(&engine, shoot_path.c_str(), 0, nullptr, nullptr, &shoot_sound);
    initialized_ = true;
    return true;
}

void AudioEngine::play_footstep() {
    if (!initialized_ || footstep_cooldown_ > 0.0f) return;
    ma_sound_seek_to_pcm_frame(&footstep_sound, 0);
    ma_sound_start(&footstep_sound);
    footstep_cooldown_ = kFootstepCooldownSeconds;
}
```

**Por que funciona?** Stream para ambiente longo; seek+start reutiliza buffer de passo; cooldown limita taxa.

**Verificação:** abrir jogo — rugido + passos ao WASD (~2–3/s máx).

**Checkpoint:** `assets/audio/ambient_dark.wav` existe após `generate_assets.py`.

---

## Relatório de resolução

Preencha o template em [`RESOLUCAO_APENDICE.md`](RESOLUCAO_APENDICE.md) após concluir os TODOs.

---

As seções **LANTERN-PICKUP-09** até **LANTERN-OBJ-17**, debug e relatório detalhado continuam em [`RESOLUCAO_APENDICE.md`](RESOLUCAO_APENDICE.md).
