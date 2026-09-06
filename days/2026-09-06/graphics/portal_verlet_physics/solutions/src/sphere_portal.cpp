// PEDAGOGY-SOLUTION: GFX-PORTAL-05
#include "sphere_portal.hpp"

static float signed_distance_to_plane(Vec3 point, const PortalFrame& frame) {
    return vec3_dot(vec3_sub(point, frame.position), vec3_normalize(frame.forward));
}

static bool inside_portal_disc(Vec3 point, const PortalFrame& frame, float portal_radius) {
    Vec3 local = mat4_transform_point(mat4_inverse_rigid(make_frame_matrix(frame)), point);
    return std::sqrt(local.x * local.x + local.y * local.y) <= portal_radius;
}

bool sphere_crosses_portal_plane(const Sphere& sphere, const PortalFrame& frame, float portal_radius) {
    float dist = signed_distance_to_plane(sphere.center, frame);
    if (dist + sphere.radius < 0.f) return false;
    if (!inside_portal_disc(sphere.center, frame, portal_radius)) return false;
    return dist <= sphere.radius;
}

bool try_sphere_teleport(Sphere& sphere, const PortalPair& pair, bool at_portal_a, float portal_radius) {
    const PortalFrame& src = at_portal_a ? pair.portal_a : pair.portal_b;
    if (!sphere_crosses_portal_plane(sphere, src, portal_radius)) {
        return false;
    }

    sphere.center = portal_transport_position(pair, at_portal_a, sphere.center);
    sphere.velocity = portal_transport_velocity(pair, at_portal_a, sphere.velocity);
    return true;
}

void sphere_step(Sphere& sphere, Vec3 gravity, float dt, float floor_y) {
    sphere.velocity = vec3_add(sphere.velocity, vec3_scale(gravity, dt));
    sphere.center = vec3_add(sphere.center, vec3_scale(sphere.velocity, dt));
    if (sphere.center.y - sphere.radius < floor_y) {
        sphere.center.y = floor_y + sphere.radius;
        sphere.velocity.y = -sphere.velocity.y * 0.55f;
        sphere.velocity.x *= 0.98f;
        sphere.velocity.z *= 0.98f;
    }
}
