#include "collision.hpp"

#include <algorithm>
#include <cmath>

namespace lantern {

Aabb player_aabb(const Vec3& position, float radius, float height) {
    return {
        {position.x - radius, position.y, position.z - radius},
        {position.x + radius, position.y + height, position.z + radius},
    };
}

bool aabb_intersects(const Aabb& a, const Aabb& b) {
    return a.min.x <= b.max.x && a.max.x >= b.min.x && a.min.y <= b.max.y && a.max.y >= b.min.y &&
           a.min.z <= b.max.z && a.max.z >= b.min.z;
}

namespace {

Aabb wall_aabb(int cell_x, int cell_y, float cell_size, float wall_height) {
    const float wx = static_cast<float>(cell_x) * cell_size;
    const float wz = static_cast<float>(cell_y) * cell_size;
    return {
        {wx, 0.0f, wz},
        {wx + cell_size, wall_height, wz + cell_size},
    };
}

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
        if (overlap_x1 < overlap_x2) {
            resolved.x += overlap_x1;
        } else {
            resolved.x -= overlap_x2;
        }
    } else {
        if (overlap_z1 < overlap_z2) {
            resolved.z += overlap_z1;
        } else {
            resolved.z -= overlap_z2;
        }
    }

    return resolved;
}

} // namespace

Vec3 move_with_collision(
    const Dungeon& dungeon,
    const Vec3& position,
    const Vec3& delta,
    float radius,
    float height,
    float cell_size,
    bool /*swimming*/) {
    // TODO [LANTERN-CAM-02]: slide AABB; bloquear WaterDeep sem swimming.
    Vec3 result = position + delta;

    constexpr float kWallHeight = 3.0f;
    constexpr int kPasses = 2;

    for (int pass = 0; pass < kPasses; ++pass) {
        for (int y = 0; y < dungeon.height; ++y) {
            for (int x = 0; x < dungeon.width; ++x) {
                if (dungeon.is_floor(x, y)) {
                    continue;
                }

                const Aabb wall = wall_aabb(x, y, cell_size, kWallHeight);
                Aabb player = player_aabb(result, radius, height);
                result = resolve_axis(player, wall, result);
            }
        }
    }

    return result;
}

bool sphere_hits_aabb(const Vec3& center, float radius, const Aabb& box) {
    const float closest_x = std::clamp(center.x, box.min.x, box.max.x);
    const float closest_y = std::clamp(center.y, box.min.y, box.max.y);
    const float closest_z = std::clamp(center.z, box.min.z, box.max.z);

    const float dx = center.x - closest_x;
    const float dy = center.y - closest_y;
    const float dz = center.z - closest_z;

    return (dx * dx + dy * dy + dz * dz) <= radius * radius;
}

} // namespace lantern
