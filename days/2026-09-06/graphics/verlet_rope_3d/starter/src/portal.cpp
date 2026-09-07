#include "portal.hpp"

Mat4 make_frame_matrix(const PortalFrame& frame) {
    // TODO [GFX-PORTAL-02]
    (void)frame;
    return mat4_identity();
}

PortalPair make_portal_pair(PortalFrame a, PortalFrame b) {
    // TODO [GFX-PORTAL-02]
    PortalPair pair{};
    pair.portal_a = a;
    pair.portal_b = b;
    return pair;
}

Vec3 portal_transport_position(const PortalPair& pair, bool from_a, Vec3 world_pos) {
    // TODO [GFX-PORTAL-03]
    (void)pair;
    (void)from_a;
    return world_pos;
}

Vec3 portal_transport_velocity(const PortalPair& pair, bool from_a, Vec3 world_vel) {
    // TODO [GFX-PORTAL-03]
    (void)pair;
    (void)from_a;
    return world_vel;
}
