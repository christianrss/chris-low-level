#include "game.hpp"

#include "checkpoint.hpp"
#include "collision.hpp"

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <random>

namespace lantern {

CellType cell_at_world(const Dungeon& dungeon, const Vec3& position) {
    const int cell_x = static_cast<int>(position.x / kCellSize);
    const int cell_y = static_cast<int>(position.z / kCellSize);
    return dungeon.at(cell_x, cell_y);
}

Vec3 world_from_cell(int cell_x, int cell_y, float y_offset) {
    return {
        static_cast<float>(cell_x) * kCellSize + kCellSize * 0.5f,
        y_offset,
        static_cast<float>(cell_y) * kCellSize + kCellSize * 0.5f,
    };
}

namespace {

std::vector<std::pair<int, int>> collect_spawn_cells(const Dungeon& dungeon) {
    std::vector<std::pair<int, int>> cells;
    for (int y = 0; y < dungeon.height; ++y) {
        for (int x = 0; x < dungeon.width; ++x) {
            if (dungeon.is_floor(x, y)) {
                cells.emplace_back(x, y);
            }
        }
    }
    return cells;
}

int manhattan(int ax, int ay, int bx, int by) {
    return std::abs(ax - bx) + std::abs(ay - by);
}

void spawn_entities(GameState& state, std::mt19937& rng) {
    // PEDAGOGY-SOLUTION: LANTERN-PLACE-10
    const auto floors = collect_spawn_cells(state.dungeon);
    if (floors.empty()) {
        return;
    }

    std::uniform_int_distribution<std::size_t> floor_dist(0, floors.size() - 1);
    const auto spawn_cell = floors[floor_dist(rng)];
    state.camera.position = world_from_cell(spawn_cell.first, spawn_cell.second, kPlayerHeight * 0.5f);

    std::vector<std::pair<int, int>> food_candidates;
    for (const auto& cell : floors) {
        if (manhattan(cell.first, cell.second, spawn_cell.first, spawn_cell.second) >= 4) {
            food_candidates.push_back(cell);
        }
    }
    if (food_candidates.empty()) {
        food_candidates = floors;
    }

    std::shuffle(food_candidates.begin(), food_candidates.end(), rng);
    state.foods.clear();
    for (int i = 0; i < kFoodToWin && i < static_cast<int>(food_candidates.size()); ++i) {
        FoodPickup food{};
        food.position = world_from_cell(food_candidates[i].first, food_candidates[i].second, 0.55f);
        state.foods.push_back(food);
    }

    state.bugs.clear();
    std::uniform_real_distribution<float> patrol(0.0f, 1.0f);
    for (int i = 0; i < kMaxBugs; ++i) {
        const auto cell = floors[floor_dist(rng)];
        Bug bug{};
        bug.position = world_from_cell(cell.first, cell.second, 0.35f);
        bug.patrol_a = bug.position;
        bug.patrol_b = bug.position + Vec3{(patrol(rng) - 0.5f) * 3.0f, 0.0f, (patrol(rng) - 0.5f) * 3.0f};
        bug.t = patrol(rng);
        bug.surface = BugSurface::Floor;

        if (i % 3 == 0) {
            bug.surface = static_cast<BugSurface>(1 + (i % 4));
            const float wx = static_cast<float>(cell.first) * kCellSize;
            const float wz = static_cast<float>(cell.second) * kCellSize;
            switch (bug.surface) {
            case BugSurface::WallNorth:
                bug.position = {wx + kCellSize * 0.5f, 1.2f, wz + 0.15f};
                bug.patrol_a = bug.position;
                bug.patrol_b = bug.position + Vec3{1.5f, 0.0f, 0.0f};
                break;
            case BugSurface::WallSouth:
                bug.position = {wx + kCellSize * 0.5f, 1.2f, wz + kCellSize - 0.15f};
                bug.patrol_a = bug.position;
                bug.patrol_b = bug.position + Vec3{-1.5f, 0.0f, 0.0f};
                break;
            case BugSurface::WallEast:
                bug.position = {wx + kCellSize - 0.15f, 1.2f, wz + kCellSize * 0.5f};
                bug.patrol_a = bug.position;
                bug.patrol_b = bug.position + Vec3{0.0f, 0.0f, 1.5f};
                break;
            case BugSurface::WallWest:
                bug.position = {wx + 0.15f, 1.2f, wz + kCellSize * 0.5f};
                bug.patrol_a = bug.position;
                bug.patrol_b = bug.position + Vec3{0.0f, 0.0f, -1.5f};
                break;
            default:
                break;
            }
        }
        state.bugs.push_back(bug);
    }

    state.altars.clear();
    for (std::size_t i = 0; i < state.dungeon.rooms.size() && i < 2; ++i) {
        const Room& room = state.dungeon.rooms[i];
        Altar altar{};
        altar.position = world_from_cell(room.x + room.w / 2, room.y + room.h / 2, 0.6f);
        state.altars.push_back(altar);
    }
}

Projectile* acquire_projectile(GameState& state) {
    for (Projectile& projectile : state.projectiles) {
        if (!projectile.active) {
            return &projectile;
        }
    }
    return nullptr;
}

void fire_projectile(GameState& state) {
    // PEDAGOGY-SOLUTION: LANTERN-PROJ-05
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

void spawn_slime_particles(GameState& state, const Vec3& origin) {
    for (int i = 0; i < 6; ++i) {
        for (SlimeParticle& particle : state.slime_particles) {
            if (particle.active) {
                continue;
            }
            particle.active = true;
            particle.position = origin;
            particle.velocity = Vec3{
                (static_cast<float>(i) - 3.0f) * 0.4f,
                0.5f + static_cast<float>(i) * 0.05f,
                (static_cast<float>(i) - 2.0f) * 0.3f,
            };
            particle.lifetime = 0.6f;
            break;
        }
    }
}

void update_projectiles(GameState& state, float delta_seconds) {
    for (Projectile& projectile : state.projectiles) {
        if (!projectile.active) {
            continue;
        }

        projectile.lifetime -= delta_seconds;
        projectile.position += projectile.velocity * delta_seconds;

        if (projectile.lifetime <= 0.0f) {
            projectile.active = false;
            continue;
        }

        for (Bug& bug : state.bugs) {
            if (!bug.alive) {
                continue;
            }

            const Aabb bug_box{
                {bug.position.x - 0.35f, bug.position.y - 0.35f, bug.position.z - 0.35f},
                {bug.position.x + 0.35f, bug.position.y + 0.35f, bug.position.z + 0.35f},
            };

            if (sphere_hits_aabb(projectile.position, 0.12f, bug_box)) {
                // PEDAGOGY-SOLUTION: LANTERN-HIT-06
                bug.alive = false;
                projectile.active = false;
                ++state.bugs_killed;
                state.objectives.on_bug_killed(state.bugs_killed);
                spawn_slime_particles(state, bug.position);
                break;
            }
        }

        if (!projectile.active) {
            continue;
        }

        const CellType cell = cell_at_world(state.dungeon, projectile.position);
        if (cell == CellType::Wall) {
            projectile.active = false;
        }
    }
}

void update_bugs(GameState& state, float delta_seconds) {
    // PEDAGOGY-SOLUTION: LANTERN-AI-07 — patrol + dano por contato
    for (Bug& bug : state.bugs) {
        if (!bug.alive) {
            continue;
        }

        bug.t += delta_seconds * 0.35f;
        const float blend = 0.5f + 0.5f * std::sin(bug.t * 6.28318f);
        bug.position = bug.patrol_a * (1.0f - blend) + bug.patrol_b * blend;

        const float dx = state.camera.position.x - bug.position.x;
        const float dz = state.camera.position.z - bug.position.z;
        const float dist_sq = dx * dx + dz * dz;
        if (dist_sq < 0.7f * 0.7f) {
            state.player.health -= 12.0f * delta_seconds;
            state.player.slime_slow = 1.0f;
            state.slime_overlay = 1.0f;
            spawn_slime_particles(state, bug.position);
        }
    }
}

void update_slime_particles(GameState& state, float delta_seconds) {
    for (SlimeParticle& particle : state.slime_particles) {
        if (!particle.active) {
            continue;
        }
        particle.lifetime -= delta_seconds;
        particle.position += particle.velocity * delta_seconds;
        particle.velocity.y -= 2.0f * delta_seconds;
        if (particle.lifetime <= 0.0f) {
            particle.active = false;
        }
    }
    state.slime_overlay = std::max(0.0f, state.slime_overlay - delta_seconds * 0.8f);
    state.player.slime_slow = std::max(0.0f, state.player.slime_slow - delta_seconds * 0.5f);
}

void update_water_state(GameState& state, float delta_seconds) {
    // PEDAGOGY-SOLUTION: LANTERN-WATER-12
    const CellType cell = cell_at_world(state.dungeon, state.camera.position);
    switch (cell) {
    case CellType::WaterShallow:
        state.player.water = WaterState::Shallow;
        state.player.swimming = false;
        state.player.breath = std::min(100.0f, state.player.breath + 25.0f * delta_seconds);
        break;
    case CellType::WaterDeep:
        state.player.water = WaterState::Deep;
        state.player.swimming = true;
        state.camera.position.y = 0.9f;
        state.player.breath -= 18.0f * delta_seconds;
        break;
    case CellType::Slime:
        // PEDAGOGY-SOLUTION: LANTERN-SLIME-11
        state.player.water = WaterState::None;
        state.player.swimming = false;
        state.player.health -= 8.0f * delta_seconds;
        state.player.slime_slow = 1.0f;
        state.slime_overlay = 1.0f;
        break;
    default:
        state.player.water = WaterState::None;
        state.player.swimming = false;
        state.player.breath = std::min(100.0f, state.player.breath + 30.0f * delta_seconds);
        if (!state.player.swimming) {
            state.camera.position.y = kPlayerHeight * 0.5f;
        }
        break;
    }

    if (state.player.breath <= 0.0f) {
        state.player.health -= 20.0f * delta_seconds;
    }
}

void track_room_visit(GameState& state) {
    const int cell_x = static_cast<int>(state.camera.position.x / kCellSize);
    const int cell_y = static_cast<int>(state.camera.position.z / kCellSize);

    for (std::size_t i = 0; i < state.dungeon.rooms.size(); ++i) {
        const Room& room = state.dungeon.rooms[i];
        if (cell_x >= room.x && cell_x < room.x + room.w && cell_y >= room.y && cell_y < room.y + room.h) {
            if (state.last_room_index != static_cast<int>(i)) {
                state.last_room_index = static_cast<int>(i);
                ++state.rooms_visited;
                state.objectives.on_room_entered(state.rooms_visited);
            }
            break;
        }
    }
}

void update_pickups(GameState& state) {
    // PEDAGOGY-SOLUTION: LANTERN-PICKUP-09
    for (FoodPickup& food : state.foods) {
        if (food.collected) {
            continue;
        }

        const float dx = state.camera.position.x - food.position.x;
        const float dy = state.camera.position.y - food.position.y;
        const float dz = state.camera.position.z - food.position.z;
        const float dist_sq = dx * dx + dy * dy + dz * dz;

        if (dist_sq < 0.9f * 0.9f) {
            food.collected = true;
            ++state.food_collected;
            state.objectives.on_food_collected(state.food_collected);
        }
    }
}

void try_activate_altar(GameState& state) {
    // PEDAGOGY-SOLUTION: LANTERN-CHK-16
    if (!state.interact_pressed) {
        return;
    }

    for (Altar& altar : state.altars) {
        const float dx = state.camera.position.x - altar.position.x;
        const float dz = state.camera.position.z - altar.position.z;
        if (dx * dx + dz * dz > 1.2f * 1.2f) {
            continue;
        }

        altar.activated = true;
        checkpoint_save(state, state.checkpoint);
        state.objectives.on_checkpoint_activated();
        break;
    }
}

void update_victory_state(GameState& state) {
    // PEDAGOGY-SOLUTION: LANTERN-OBJ-17
    const bool ready = state.objectives.all_complete();
    state.objectives.on_escape_ready(ready);
    if (ready) {
        state.won = true;
        state.screen = GameScreen::Victory;
    }
}

} // namespace

void game_reset(GameState& state, std::uint32_t seed) {
    state = GameState{};
    state.seed = seed;
    state.screen = GameScreen::Playing;
    state.dungeon = generate_dungeon(seed);
    state.objectives.reset();
    std::mt19937 rng(seed ^ 0xA5A5A5A5u);
    spawn_entities(state, rng);
}

void game_respawn_to_checkpoint(GameState& state) {
    if (state.checkpoint.valid) {
        checkpoint_restore(state, state.checkpoint);
    } else {
        game_reset(state, state.seed);
    }
    state.screen = GameScreen::Playing;
    state.player.health = std::max(state.player.health, 25.0f);
}

void game_update(GameState& state, float delta_seconds, bool move_forward, bool move_back, bool move_left,
    bool move_right, bool shoot_pressed) {
    if (state.screen != GameScreen::Playing) {
        return;
    }

    state.time_seconds += delta_seconds;

    Vec3 move{};
    const Vec3 forward_flat = Vec3{state.camera.forward().x, 0.0f, state.camera.forward().z}.normalized();
    const Vec3 right_flat = Vec3{state.camera.right().x, 0.0f, state.camera.right().z}.normalized();

    if (move_forward) {
        move += forward_flat;
    }
    if (move_back) {
        move -= forward_flat;
    }
    if (move_left) {
        move -= right_flat;
    }
    if (move_right) {
        move += right_flat;
    }

    float speed = 4.5f;
    if (state.player.slime_slow > 0.1f) {
        speed *= 0.55f;
    }
    if (state.player.water == WaterState::Shallow) {
        speed *= 0.6f;
    }
    if (state.player.swimming) {
        speed *= 0.75f;
    }

    if (move.length() > 0.0f) {
        move = move.normalized() * (speed * delta_seconds);
        state.camera.position = move_with_collision(state.dungeon, state.camera.position, move, kPlayerRadius,
            kPlayerHeight, kCellSize, state.player.swimming);
    }

    if (shoot_pressed) {
        fire_projectile(state);
    }

    update_water_state(state, delta_seconds);
    track_room_visit(state);
    update_projectiles(state, delta_seconds);
    update_bugs(state, delta_seconds);
    update_slime_particles(state, delta_seconds);
    update_pickups(state);
    try_activate_altar(state);
    update_victory_state(state);
    state.interact_pressed = false;

    if (state.player.health <= 0.0f) {
        state.screen = GameScreen::GameOver;
    }
}

std::vector<DrawCommand> build_draw_list(const GameState& state) {
    std::vector<DrawCommand> commands;
    commands.reserve(1024);

    for (int y = 0; y < state.dungeon.height; ++y) {
        for (int x = 0; x < state.dungeon.width; ++x) {
            const float wx = static_cast<float>(x) * kCellSize;
            const float wz = static_cast<float>(y) * kCellSize;
            const CellType cell = state.dungeon.at(x, y);

            DrawCommand floor_cmd{};
            floor_cmd.model = translate(wx + kCellSize * 0.5f, -0.05f, wz + kCellSize * 0.5f) *
                              scale(kCellSize, 0.1f, kCellSize);
            floor_cmd.surface = SurfaceKind::Floor;
            commands.push_back(floor_cmd);

            if (cell == CellType::WaterShallow || cell == CellType::WaterDeep) {
                DrawCommand water_cmd{};
                water_cmd.model = translate(wx + kCellSize * 0.5f, cell == CellType::WaterDeep ? -0.2f : 0.02f,
                    wz + kCellSize * 0.5f) * scale(kCellSize, 0.12f, kCellSize);
                water_cmd.surface = SurfaceKind::Water;
                commands.push_back(water_cmd);
                continue;
            }

            if (cell == CellType::Slime) {
                DrawCommand slime_cmd{};
                slime_cmd.model = translate(wx + kCellSize * 0.5f, 0.02f, wz + kCellSize * 0.5f) *
                                  scale(kCellSize, 0.08f, kCellSize);
                slime_cmd.surface = SurfaceKind::Slime;
                commands.push_back(slime_cmd);
                continue;
            }

            if (cell == CellType::Floor) {
                continue;
            }

            DrawCommand wall_cmd{};
            wall_cmd.model = translate(wx + kCellSize * 0.5f, 1.5f, wz + kCellSize * 0.5f) *
                             scale(kCellSize, 3.0f, kCellSize);
            wall_cmd.surface = SurfaceKind::Wall;
            commands.push_back(wall_cmd);
        }
    }

    for (const Altar& altar : state.altars) {
        DrawCommand altar_cmd{};
        altar_cmd.model = translate(altar.position.x, altar.position.y, altar.position.z) * scale(0.5f, 0.8f, 0.5f);
        altar_cmd.surface = SurfaceKind::Altar;
        altar_cmd.emissive = altar.activated;
        commands.push_back(altar_cmd);
    }

    for (const Bug& bug : state.bugs) {
        if (!bug.alive) {
            continue;
        }
        DrawCommand bug_cmd{};
        bug_cmd.model = translate(bug.position.x, bug.position.y, bug.position.z) * scale(0.7f, 0.35f, 0.9f);
        bug_cmd.surface = SurfaceKind::Bug;
        commands.push_back(bug_cmd);
    }

    for (const FoodPickup& food : state.foods) {
        if (food.collected) {
            continue;
        }
        DrawCommand food_cmd{};
        food_cmd.model = translate(food.position.x, food.position.y, food.position.z) * scale(0.35f, 0.35f, 0.35f);
        food_cmd.surface = SurfaceKind::Food;
        food_cmd.emissive = true;
        commands.push_back(food_cmd);
    }

    for (const Projectile& projectile : state.projectiles) {
        if (!projectile.active) {
            continue;
        }
        DrawCommand marble_cmd{};
        marble_cmd.model =
            translate(projectile.position.x, projectile.position.y, projectile.position.z) * scale(0.12f, 0.12f, 0.12f);
        marble_cmd.surface = SurfaceKind::Food;
        commands.push_back(marble_cmd);
    }

    for (const SlimeParticle& particle : state.slime_particles) {
        if (!particle.active) {
            continue;
        }
        DrawCommand slime_particle{};
        slime_particle.model =
            translate(particle.position.x, particle.position.y, particle.position.z) * scale(0.15f, 0.15f, 0.15f);
        slime_particle.surface = SurfaceKind::Slime;
        commands.push_back(slime_particle);
    }

    return commands;
}

} // namespace lantern
