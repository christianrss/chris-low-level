#include "checkpoint.hpp"
#include "game.hpp"

namespace lantern {

void checkpoint_save(const GameState& state, CheckpointData& out) {
    // PEDAGOGY-SOLUTION: LANTERN-CHK-16
    out.valid = true;
    out.seed = state.seed;
    out.position = state.camera.position;
    out.health = state.player.health;
    out.breath = state.player.breath;
    out.food_collected = state.food_collected;
    out.bugs_killed = state.bugs_killed;
    out.rooms_visited = state.rooms_visited;
}

void checkpoint_restore(GameState& state, const CheckpointData& data) {
    if (!data.valid) {
        return;
    }

    state.camera.position = data.position;
    state.player.health = data.health;
    state.player.breath = data.breath;
    state.food_collected = data.food_collected;
    state.bugs_killed = data.bugs_killed;
    state.rooms_visited = data.rooms_visited;
    state.checkpoint = data;
    state.player.slime_slow = 0.0f;
    state.slime_overlay = 0.0f;
    state.player.water = WaterState::None;
    state.player.swimming = false;
}

} // namespace lantern
