#pragma once

#include "math.hpp"

struct PortalFrame {
    Vec3 position;
    Vec3 forward;
    Vec3 up;
};

struct PortalPair {
    PortalFrame portal_a;
    PortalFrame portal_b;
    Mat4 world_to_a;
    Mat4 world_to_b;
    Mat4 a_to_b;
    Mat4 b_to_a;
};

PortalPair make_portal_pair(PortalFrame a, PortalFrame b);
Mat4 make_frame_matrix(const PortalFrame& frame);
Vec3 portal_transport_position(const PortalPair& pair, bool from_a, Vec3 world_pos);
Vec3 portal_transport_velocity(const PortalPair& pair, bool from_a, Vec3 world_vel);
