#pragma once

#include "math.hpp"

#include <cstdint>

namespace lantern {

struct CheckpointData {
    bool valid = false;
    std::uint32_t seed = 0;
    Vec3 position{};
    float health = 100.0f;
    float breath = 100.0f;
    int food_collected = 0;
    int bugs_killed = 0;
    int rooms_visited = 0;
};

struct GameState;

void checkpoint_save(const GameState& state, CheckpointData& out);
void checkpoint_restore(GameState& state, const CheckpointData& data);

} // namespace lantern
