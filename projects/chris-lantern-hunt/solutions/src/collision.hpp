#pragma once

#include "math.hpp"
#include "procgen.hpp"

namespace lantern {

struct Aabb {
    Vec3 min{};
    Vec3 max{};
};

Aabb player_aabb(const Vec3& position, float radius, float height);

bool aabb_intersects(const Aabb& a, const Aabb& b);

// LANTERN-CAM-02: desliza o jogador contra células Wall do grid.
Vec3 move_with_collision(
    const Dungeon& dungeon,
    const Vec3& position,
    const Vec3& delta,
    float radius,
    float height,
    float cell_size,
    bool swimming);

bool sphere_hits_aabb(const Vec3& center, float radius, const Aabb& box);

} // namespace lantern
