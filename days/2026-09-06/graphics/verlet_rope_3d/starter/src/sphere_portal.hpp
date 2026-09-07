#pragma once

#include "math.hpp"
#include "portal.hpp"

struct Sphere {
    Vec3 center;
    float radius = 0.5f;
    Vec3 velocity;
};

bool sphere_crosses_portal_plane(const Sphere& sphere, const PortalFrame& frame, float portal_radius);
bool try_sphere_teleport(Sphere& sphere, const PortalPair& pair, bool at_portal_a, float portal_radius);
