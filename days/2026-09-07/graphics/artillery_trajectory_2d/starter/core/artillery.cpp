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
    // TODO [GFX-ART-PHYS-01]
    (void)p;
    (void)dt;
    (void)gravity;
}

bool terrain_hit(const Projectile& p, const Terrain& t) {
    // TODO [GFX-ART-TERRAIN-02]
    (void)p;
    (void)t;
    return false;
}

void trail_push(Trail& trail, Vec2 pos) {
    // TODO [GFX-ART-TRAIL-03]
    (void)trail;
    (void)pos;
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
