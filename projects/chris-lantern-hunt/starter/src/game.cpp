#include "game.hpp"

#include "collision.hpp"

#include <cmath>

namespace lantern {

Vec3 world_from_cell(int cell_x, int cell_y, float y_offset) {
    return {
        static_cast<float>(cell_x) * kCellSize + kCellSize * 0.5f,
        y_offset,
        static_cast<float>(cell_y) * kCellSize + kCellSize * 0.5f,
    };
}

CellType cell_at_world(const Dungeon& dungeon, const Vec3& position) {
    const int gx = static_cast<int>(std::floor(position.x / kCellSize));
    const int gy = static_cast<int>(std::floor(position.z / kCellSize));
    return dungeon.at(gx, gy);
}

void game_reset(GameState& state, std::uint32_t seed) {
    state = GameState{};
    state.seed = seed;
    state.screen = GameScreen::MainMenu;
    state.dungeon = generate_dungeon(seed);
    // TODO [LANTERN-PLACE-10]: spawn de comida, insetos e altares.
    state.objectives.reset();
}

void game_update(GameState& state, float delta_seconds, bool move_forward, bool move_back, bool move_left,
    bool move_right, bool /*shoot_pressed*/) {
    if (state.screen != GameScreen::Playing) {
        return;
    }

    state.time_seconds += delta_seconds;
    state.interact_pressed = false;

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

    if (move.length() > 0.0f) {
        move = move.normalized() * (4.5f * delta_seconds);
        state.camera.position = move_with_collision(state.dungeon, state.camera.position, move, kPlayerRadius,
            kPlayerHeight, kCellSize, state.player.swimming);
    }

    // TODO [LANTERN-PROJ-05]: disparar projéteis da lanterna.
    // TODO [LANTERN-HIT-06]: colisão projétil x inseto.
    // TODO [LANTERN-AI-07]: patrol de insetos em chão/parede.
    // TODO [LANTERN-PICKUP-09]: coleta de comida e progresso de objetivos.
    // TODO [LANTERN-WATER-12]: natação, respiração e velocidade na água.
    // TODO [LANTERN-SLIME-11]: dano por contato com gosma/insetos.
}

void game_respawn_to_checkpoint(GameState& state) {
    checkpoint_restore(state, state.checkpoint);
}

std::vector<DrawCommand> build_draw_list(const GameState& state) {
    std::vector<DrawCommand> commands;
    for (int y = 0; y < state.dungeon.height; ++y) {
        for (int x = 0; x < state.dungeon.width; ++x) {
            const float wx = static_cast<float>(x) * kCellSize;
            const float wz = static_cast<float>(y) * kCellSize;

            DrawCommand floor_cmd{};
            floor_cmd.model = translate(wx + kCellSize * 0.5f, -0.05f, wz + kCellSize * 0.5f) *
                              scale(kCellSize, 0.1f, kCellSize);
            floor_cmd.surface = SurfaceKind::Floor;
            commands.push_back(floor_cmd);

            if (state.dungeon.is_floor(x, y)) {
                continue;
            }

            DrawCommand wall_cmd{};
            wall_cmd.model = translate(wx + kCellSize * 0.5f, 1.5f, wz + kCellSize * 0.5f) *
                             scale(kCellSize, 3.0f, kCellSize);
            wall_cmd.surface = SurfaceKind::Wall;
            commands.push_back(wall_cmd);
        }
    }
    return commands;
}

} // namespace lantern
