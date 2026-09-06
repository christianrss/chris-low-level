// PEDAGOGY-SOLUTION: GFX-PORTAL-02
// PEDAGOGY-SOLUTION: GFX-PORTAL-03
#include "portal.hpp"

Mat4 make_frame_matrix(const PortalFrame& frame) {
    Vec3 f = vec3_normalize(frame.forward);
    Vec3 r = vec3_normalize({f.y * frame.up.z - f.z * frame.up.y,
                             f.z * frame.up.x - f.x * frame.up.z,
                             f.x * frame.up.y - f.y * frame.up.x});
    Vec3 u = vec3_normalize({r.y * f.z - r.z * f.y, r.z * f.x - r.x * f.z, r.x * f.y - r.y * f.x});

    Mat4 m = mat4_identity();
    m.m[0] = r.x;
    m.m[1] = r.y;
    m.m[2] = r.z;
    m.m[4] = u.x;
    m.m[5] = u.y;
    m.m[6] = u.z;
    m.m[8] = f.x;
    m.m[9] = f.y;
    m.m[10] = f.z;
    m.m[12] = frame.position.x;
    m.m[13] = frame.position.y;
    m.m[14] = frame.position.z;
    return m;
}

static Mat4 portal_link_matrix(const Mat4& a, const Mat4& b) {
    return mat4_multiply(b, mat4_inverse_rigid(a));
}

PortalPair make_portal_pair(PortalFrame a, PortalFrame b) {
    PortalPair pair{};
    pair.portal_a = a;
    pair.portal_b = b;
    Mat4 frame_a = make_frame_matrix(a);
    Mat4 frame_b = make_frame_matrix(b);
    pair.world_to_a = mat4_inverse_rigid(frame_a);
    pair.world_to_b = mat4_inverse_rigid(frame_b);
    pair.a_to_b = portal_link_matrix(frame_a, frame_b);
    pair.b_to_a = portal_link_matrix(frame_b, frame_a);
    return pair;
}

Vec3 portal_transport_position(const PortalPair& pair, bool from_a, Vec3 world_pos) {
    const Mat4& link = from_a ? pair.a_to_b : pair.b_to_a;
    return mat4_transform_point(link, world_pos);
}

Vec3 portal_transport_velocity(const PortalPair& pair, bool from_a, Vec3 world_vel) {
    const Mat4& link = from_a ? pair.a_to_b : pair.b_to_a;
    return mat4_transform_direction(link, world_vel);
}
