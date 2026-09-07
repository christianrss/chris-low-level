#pragma once

#include "math.hpp"
#include <vector>

struct VerletRope {
    std::vector<Vec3> points;
    std::vector<Vec3> prev_points;
    float segment_length = 1.f;
};

void verlet_init_rope(VerletRope& rope, Vec3 start, Vec3 end, int segments);
void verlet_step(VerletRope& rope, Vec3 gravity, float dt, int constraint_iters);
float verlet_total_length(const VerletRope& rope);
