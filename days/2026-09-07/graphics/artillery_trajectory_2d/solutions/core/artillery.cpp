#include "artillery.hpp"
#include <cmath>

namespace art2d {

float Terrain::sample(float x) const {
    if (heights.empty()) {
        return 0.0f;
    }
    const float idx = x * 0.1f;
    const std::size_t i = static_cast<std::size_t>(idx);
    if (i >= heights.size() - 1) {
        return heights.back();
    }
    const float frac = idx - static_cast<float>(i);
    return heights[i] * (1.0f - frac) + heights[i + 1] * frac;
}

void fire(Projectile& p, float angle_deg, float power) {
    const float rad = angle_deg * 3.14159265f / 180.0f;
    p.pos = {0.0f, 0.0f};
    p.vel = {std::cos(rad) * power, std::sin(rad) * power};
    p.alive = true;
}

void integrate(Projectile& p, float dt, float gravity) {
    // PEDAGOGY-SOLUTION: GFX-ART-PHYS-01
    if (!p.alive) {
        return;
    }
    p.vel.y -= gravity * dt;
    p.pos.x += p.vel.x * dt;
    p.pos.y += p.vel.y * dt;
}

bool terrain_hit(const Projectile& p, const Terrain& t) {
    // PEDAGOGY-SOLUTION: GFX-ART-TERRAIN-02
    if (!p.alive) {
        return false;
    }
    return p.pos.y <= t.sample(p.pos.x);
}

void trail_push(Trail& trail, Vec2 pos) {
    // PEDAGOGY-SOLUTION: GFX-ART-TRAIL-03
    if (trail.count < Trail::kCapacity) {
        trail.points[trail.count++].pos = pos;
    } else {
        for (std::size_t i = 1; i < Trail::kCapacity; ++i) {
            trail.points[i - 1] = trail.points[i];
        }
        trail.points[Trail::kCapacity - 1].pos = pos;
    }
}

void crater(Terrain& terrain, float x, float radius, float depth) {
    for (std::size_t i = 0; i < terrain.heights.size(); ++i) {
        const float px = static_cast<float>(i) * 10.0f;
        const float d = std::fabs(px - x);
        if (d < radius) {
            const float factor = 1.0f - d / radius;
            terrain.heights[i] -= depth * factor;
        }
    }
}

}  // namespace art2d
