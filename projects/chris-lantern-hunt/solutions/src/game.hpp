#pragma once

#include "checkpoint.hpp"
#include "math.hpp"
#include "objectives.hpp"
#include "procgen.hpp"

#include <cstdint>
#include <vector>

namespace lantern {

constexpr float kCellSize = 2.0f;
constexpr float kPlayerRadius = 0.32f;
constexpr float kPlayerHeight = 1.65f;
constexpr int kFoodToWin = 5;
constexpr int kMaxBugs = 12;
constexpr int kMaxProjectiles = 16;
constexpr int kMaxSlimeParticles = 48;

enum class GameScreen {
    MainMenu,
    Playing,
    Paused,
    GameOver,
    Victory,
};

enum class WaterState {
    None,
    Shallow,
    Deep,
};

enum class SurfaceKind {
    Floor,
    Wall,
    Bug,
    Food,
    Water,
    Slime,
    Altar,
};

enum class BugSurface {
    Floor,
    WallNorth,
    WallSouth,
    WallEast,
    WallWest,
};

struct PlayerStats {
    float health = 100.0f;
    float breath = 100.0f;
    float slime_slow = 0.0f;
    WaterState water = WaterState::None;
    bool swimming = false;
};

struct Projectile {
    bool active = false;
    Vec3 position{};
    Vec3 velocity{};
    float lifetime = 0.0f;
};

struct Bug {
    bool alive = true;
    Vec3 position{};
    Vec3 patrol_a{};
    Vec3 patrol_b{};
    float t = 0.0f;
    BugSurface surface = BugSurface::Floor;
};

struct FoodPickup {
    bool collected = false;
    Vec3 position{};
};

struct Altar {
    Vec3 position{};
    bool activated = false;
};

struct SlimeParticle {
    bool active = false;
    Vec3 position{};
    Vec3 velocity{};
    float lifetime = 0.0f;
};

struct DrawCommand {
    Mat4 model{};
    SurfaceKind surface = SurfaceKind::Floor;
    bool emissive = false;
};

struct GameState {
    std::uint32_t seed = 42;
    GameScreen screen = GameScreen::MainMenu;
    Dungeon dungeon{};
    FpsCamera camera{};
    PlayerStats player{};
    CheckpointData checkpoint{};
    ObjectiveTracker objectives;
    std::vector<Bug> bugs;
    std::vector<FoodPickup> foods;
    std::vector<Altar> altars;
    SlimeParticle slime_particles[kMaxSlimeParticles]{};
    Projectile projectiles[kMaxProjectiles]{};
    int food_collected = 0;
    int bugs_killed = 0;
    int rooms_visited = 0;
    int last_room_index = -1;
    float slime_overlay = 0.0f;
    bool won = false;
    bool quit_requested = false;
    float time_seconds = 0.0f;
    bool interact_pressed = false;
    int menu_selection = 0;
};

void game_reset(GameState& state, std::uint32_t seed);

void game_update(GameState& state, float delta_seconds, bool move_forward, bool move_back, bool move_left,
    bool move_right, bool shoot_pressed);

void game_respawn_to_checkpoint(GameState& state);

std::vector<DrawCommand> build_draw_list(const GameState& state);

Vec3 world_from_cell(int cell_x, int cell_y, float y_offset = 0.0f);

CellType cell_at_world(const Dungeon& dungeon, const Vec3& position);

} // namespace lantern
