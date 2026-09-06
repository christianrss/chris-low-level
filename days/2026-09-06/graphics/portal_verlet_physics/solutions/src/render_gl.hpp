#pragma once

#include "math.hpp"
#include "portal.hpp"
#include "sphere_portal.hpp"
#include "verlet.hpp"

struct Camera {
    Vec3 eye{0.f, 1.6f, 6.f};
    float yaw = 0.f;
    float pitch = 0.f;
};

struct PortalScene {
    PortalPair portals;
    VerletRope rope;
    Sphere sphere;
    float portal_radius = 1.2f;
};

struct PortalGlContext {
    void* hwnd = nullptr;
    void* hdc = nullptr;
    void* hglrc = nullptr;
    int width = 1280;
    int height = 720;
    int stencil_passes = 0;
};

bool portal_gl_init(PortalGlContext& ctx, void* hwnd);
void portal_gl_shutdown(PortalGlContext& ctx);
void portal_gl_resize(PortalGlContext& ctx, int width, int height);

Vec3 camera_forward(const Camera& camera);
void camera_strafe(Camera& camera, float right, float up, float forward);
Mat4 camera_view_matrix(const Camera& camera);
Camera mirror_camera_through_portal(const Camera& camera, const PortalPair& pair, bool from_a);

void portal_gl_render_frame(
    PortalGlContext& ctx,
    const PortalScene& scene,
    const Camera& camera,
    float aspect);
