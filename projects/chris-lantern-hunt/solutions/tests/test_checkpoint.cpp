#include "../src/checkpoint.hpp"
#include "../src/game.hpp"

#include <cassert>
#include <iostream>

int main() {
    // PEDAGOGY-TEST: LANTERN-CHK-16 — salvar e restaurar checkpoint
    lantern::GameState state{};
    lantern::game_reset(state, 42u);
    state.player.health = 55.0f;
    state.player.breath = 40.0f;
    state.camera.position = {10.0f, 1.0f, 12.0f};
    state.food_collected = 2;

    lantern::CheckpointData saved{};
    lantern::checkpoint_save(state, saved);
    assert(saved.valid);
    assert(saved.health == 55.0f);

    state.player.health = 5.0f;
    state.camera.position = {0.0f, 0.0f, 0.0f};
    lantern::checkpoint_restore(state, saved);

    assert(state.player.health == 55.0f);
    assert(state.camera.position.x == 10.0f);
    assert(state.food_collected == 2);

    std::cout << "test_checkpoint: PASS\n";
    return 0;
}
