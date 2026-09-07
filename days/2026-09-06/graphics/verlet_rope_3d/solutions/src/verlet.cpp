// PEDAGOGY-SOLUTION: GFX-PORTAL-04
#include "verlet.hpp"

void verlet_init_rope(VerletRope& rope, Vec3 start, Vec3 end, int segments) {
    rope.points.clear();
    rope.prev_points.clear();
    if (segments < 2) segments = 2;
    rope.segment_length = vec3_length(vec3_sub(end, start)) / static_cast<float>(segments - 1);
    for (int i = 0; i < segments; ++i) {
        float t = static_cast<float>(i) / static_cast<float>(segments - 1);
        Vec3 p = vec3_add(start, vec3_scale(vec3_sub(end, start), t));
        rope.points.push_back(p);
        rope.prev_points.push_back(p);
    }
}

static void constrain_segments(VerletRope& rope) {
    for (size_t i = 0; i + 1 < rope.points.size(); ++i) {
        Vec3 delta = vec3_sub(rope.points[i + 1], rope.points[i]);
        float dist = vec3_length(delta);
        if (dist < 1e-6f) continue;
        float diff = (dist - rope.segment_length) / dist;
        Vec3 correction = vec3_scale(delta, 0.5f * diff);
        if (i > 0) rope.points[i] = vec3_add(rope.points[i], correction);
        if (i + 1 < rope.points.size() - 1) {
            rope.points[i + 1] = vec3_sub(rope.points[i + 1], correction);
        }
    }
}

void verlet_step(VerletRope& rope, Vec3 gravity, float dt, int constraint_iters) {
    const size_t n = rope.points.size();
    if (n < 2) return;

    for (size_t i = 1; i + 1 < n; ++i) {
        Vec3 current = rope.points[i];
        Vec3 velocity = vec3_sub(current, rope.prev_points[i]);
        Vec3 next = vec3_add(vec3_add(current, velocity), vec3_scale(gravity, dt * dt));
        rope.prev_points[i] = current;
        rope.points[i] = next;
    }

    for (int k = 0; k < constraint_iters; ++k) {
        constrain_segments(rope);
    }
}

float verlet_total_length(const VerletRope& rope) {
    float total = 0.f;
    for (size_t i = 0; i + 1 < rope.points.size(); ++i) {
        total += vec3_length(vec3_sub(rope.points[i + 1], rope.points[i]));
    }
    return total;
}
