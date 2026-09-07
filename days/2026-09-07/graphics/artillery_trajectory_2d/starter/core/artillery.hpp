#pragma once
#include <cstddef>
#include <vector>

namespace art2d {

struct Vec2 {
    float x = 0.0f;
    float y = 0.0f;
};

struct Projectile {
    Vec2 pos{};
    Vec2 vel{};
    bool alive = false;
};

struct Terrain {
    std::vector<float> heights;
    float sample(float x) const;
};

struct TrailPoint {
    Vec2 pos{};
};

struct Trail {
    static constexpr std::size_t kCapacity = 128;
    TrailPoint points[kCapacity]{};
    std::size_t count = 0;
};

void fire(Projectile& p, float angle_deg, float power);
void integrate(Projectile& p, float dt, float gravity);
bool terrain_hit(const Projectile& p, const Terrain& t);
void trail_push(Trail& trail, Vec2 pos);
void crater(Terrain& t, float x, float radius, float depth);

}  // namespace art2d
