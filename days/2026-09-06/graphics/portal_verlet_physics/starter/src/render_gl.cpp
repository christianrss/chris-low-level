// TODO [GFX-PORTAL-06]: WGL init, stencil portal pass, draw room/rope/sphere
#include "render_gl.hpp"

bool portal_gl_init(PortalGlContext& ctx, void* hwnd) {
    (void)ctx;
    (void)hwnd;
    return false;
}

void portal_gl_shutdown(PortalGlContext& ctx) {
    (void)ctx;
}

void portal_gl_resize(PortalGlContext& ctx, int width, int height) {
    ctx.width = width;
    ctx.height = height;
}

Vec3 camera_forward(const Camera& camera) {
    (void)camera;
    return {0.f, 0.f, 1.f};
}

void camera_strafe(Camera& camera, float right, float up, float forward) {
    (void)camera;
    (void)right;
    (void)up;
    (void)forward;
}

Mat4 camera_view_matrix(const Camera& camera) {
    (void)camera;
    return mat4_identity();
}

Camera mirror_camera_through_portal(const Camera& camera, const PortalPair& pair, bool from_a) {
    (void)pair;
    (void)from_a;
    return camera;
}

void portal_gl_render_frame(
    PortalGlContext& ctx,
    const PortalScene& scene,
    const Camera& camera,
    float aspect) {
    (void)ctx;
    (void)scene;
    (void)camera;
    (void)aspect;
}
