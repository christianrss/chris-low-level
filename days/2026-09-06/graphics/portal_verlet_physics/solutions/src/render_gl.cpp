// PEDAGOGY-SOLUTION: GFX-PORTAL-06
#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif

#include "render_gl.hpp"

#include <windows.h>
#include <GL/gl.h>

#include <algorithm>
#include <cmath>
#include <cstring>

namespace {

void load_matrix(const Mat4& m) {
    glLoadMatrixf(m.m);
}

void multiply_matrix(const Mat4& m) {
    glMultMatrixf(m.m);
}

void set_color(float r, float g, float b, float a = 1.f) {
    glColor4f(r, g, b, a);
}

void draw_floor() {
    set_color(0.25f, 0.28f, 0.32f);
    glBegin(GL_QUADS);
    glVertex3f(-8.f, 0.f, -8.f);
    glVertex3f(8.f, 0.f, -8.f);
    glVertex3f(8.f, 0.f, 8.f);
    glVertex3f(-8.f, 0.f, 8.f);
    glEnd();

    set_color(0.35f, 0.2f, 0.2f);
    glBegin(GL_QUADS);
    glVertex3f(-8.f, 0.f, -8.f);
    glVertex3f(-8.f, 4.f, -8.f);
    glVertex3f(8.f, 4.f, -8.f);
    glVertex3f(8.f, 0.f, -8.f);
    glEnd();

    set_color(0.2f, 0.35f, 0.22f);
    glBegin(GL_QUADS);
    glVertex3f(-8.f, 0.f, 8.f);
    glVertex3f(-8.f, 4.f, 8.f);
    glVertex3f(8.f, 4.f, 8.f);
    glVertex3f(8.f, 0.f, 8.f);
    glEnd();

    set_color(0.22f, 0.22f, 0.38f);
    glBegin(GL_QUADS);
    glVertex3f(-8.f, 0.f, -8.f);
    glVertex3f(-8.f, 4.f, -8.f);
    glVertex3f(-8.f, 4.f, 8.f);
    glVertex3f(-8.f, 0.f, 8.f);
    glEnd();

    set_color(0.3f, 0.3f, 0.18f);
    glBegin(GL_QUADS);
    glVertex3f(8.f, 0.f, -8.f);
    glVertex3f(8.f, 4.f, -8.f);
    glVertex3f(8.f, 4.f, 8.f);
    glVertex3f(8.f, 0.f, 8.f);
    glEnd();
}

void draw_portal_quad(const PortalFrame& frame, float radius, float r, float g, float b) {
    glPushMatrix();
    multiply_matrix(make_frame_matrix(frame));
    set_color(r, g, b, 0.85f);
    glBegin(GL_QUADS);
    glVertex3f(-radius, -radius, 0.f);
    glVertex3f(radius, -radius, 0.f);
    glVertex3f(radius, radius, 0.f);
    glVertex3f(-radius, radius, 0.f);
    glEnd();
    glPopMatrix();
}

void draw_rope(const VerletRope& rope) {
    if (rope.points.size() < 2) return;
    set_color(0.9f, 0.85f, 0.5f);
    glBegin(GL_LINE_STRIP);
    for (const Vec3& p : rope.points) {
        glVertex3f(p.x, p.y, p.z);
    }
    glEnd();
}

void draw_sphere(const Sphere& sphere) {
    set_color(0.95f, 0.35f, 0.2f);
    const int slices = 12;
    const int stacks = 8;
    for (int i = 0; i < stacks; ++i) {
        const float v0 = static_cast<float>(i) / stacks;
        const float v1 = static_cast<float>(i + 1) / stacks;
        const float phi0 = v0 * 3.14159265f;
        const float phi1 = v1 * 3.14159265f;
        glBegin(GL_TRIANGLE_STRIP);
        for (int j = 0; j <= slices; ++j) {
            const float u = static_cast<float>(j) / slices;
            const float theta = u * 2.f * 3.14159265f;
            const float x0 = std::sin(phi0) * std::cos(theta);
            const float y0 = std::cos(phi0);
            const float z0 = std::sin(phi0) * std::sin(theta);
            const float x1 = std::sin(phi1) * std::cos(theta);
            const float y1 = std::cos(phi1);
            const float z1 = std::sin(phi1) * std::sin(theta);
            glVertex3f(sphere.center.x + x0 * sphere.radius, sphere.center.y + y0 * sphere.radius,
                sphere.center.z + z0 * sphere.radius);
            glVertex3f(sphere.center.x + x1 * sphere.radius, sphere.center.y + y1 * sphere.radius,
                sphere.center.z + z1 * sphere.radius);
        }
        glEnd();
    }
}

void setup_projection(float aspect) {
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    load_matrix(mat4_perspective(60.f * 3.14159265f / 180.f, aspect, 0.1f, 100.f));
    glMatrixMode(GL_MODELVIEW);
}

void setup_view(const Camera& camera) {
    glLoadIdentity();
    load_matrix(camera_view_matrix(camera));
}

void draw_scene_content(const PortalScene& scene, bool draw_portal_frames) {
    draw_floor();
    draw_rope(scene.rope);
    draw_sphere(scene.sphere);
    if (draw_portal_frames) {
        draw_portal_quad(scene.portals.portal_a, scene.portal_radius, 0.2f, 0.7f, 1.f);
        draw_portal_quad(scene.portals.portal_b, scene.portal_radius, 1.f, 0.5f, 0.15f);
    }
}

void render_through_portal(
    PortalGlContext& ctx,
    const PortalScene& scene,
    const Camera& camera,
    bool from_a,
    float aspect) {
    const PortalFrame& src = from_a ? scene.portals.portal_a : scene.portals.portal_b;

    glEnable(GL_STENCIL_TEST);
    glStencilMask(0xFF);
    glClear(GL_STENCIL_BUFFER_BIT);

    glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE);
    glDepthMask(GL_FALSE);
    glStencilFunc(GL_ALWAYS, 1, 0xFF);
    glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE);

    setup_projection(aspect);
    setup_view(camera);
    draw_portal_quad(src, scene.portal_radius, 1.f, 1.f, 1.f);

    glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE);
    glDepthMask(GL_TRUE);
    glStencilFunc(GL_EQUAL, 1, 0xFF);
    glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP);

    const Camera mirrored = mirror_camera_through_portal(camera, scene.portals, from_a);
    setup_projection(aspect);
    setup_view(mirrored);
    draw_scene_content(scene, false);

    glDisable(GL_STENCIL_TEST);
    ++ctx.stencil_passes;
}

} // namespace

bool portal_gl_init(PortalGlContext& ctx, void* hwnd) {
    HWND window = static_cast<HWND>(hwnd);
    HDC hdc = GetDC(window);
    if (!hdc) return false;

    PIXELFORMATDESCRIPTOR pfd{};
    pfd.nSize = sizeof(pfd);
    pfd.nVersion = 1;
    pfd.dwFlags = PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL | PFD_DOUBLEBUFFER;
    pfd.iPixelType = PFD_TYPE_RGBA;
    pfd.cColorBits = 32;
    pfd.cDepthBits = 24;
    pfd.cStencilBits = 8;

    const int pf = ChoosePixelFormat(hdc, &pfd);
    if (pf == 0 || !SetPixelFormat(hdc, pf, &pfd)) {
        ReleaseDC(window, hdc);
        return false;
    }

    HGLRC rc = wglCreateContext(hdc);
    if (!rc || !wglMakeCurrent(hdc, rc)) {
        if (rc) wglDeleteContext(rc);
        ReleaseDC(window, hdc);
        return false;
    }

    ctx.hdc = hdc;
    ctx.hglrc = rc;
    ctx.hwnd = hwnd;

    glEnable(GL_DEPTH_TEST);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    return true;
}

void portal_gl_shutdown(PortalGlContext& ctx) {
    if (ctx.hglrc) {
        wglMakeCurrent(nullptr, nullptr);
        wglDeleteContext(static_cast<HGLRC>(ctx.hglrc));
        ctx.hglrc = nullptr;
    }
    if (ctx.hdc && ctx.hwnd) {
        ReleaseDC(static_cast<HWND>(ctx.hwnd), static_cast<HDC>(ctx.hdc));
        ctx.hdc = nullptr;
    }
}

void portal_gl_resize(PortalGlContext& ctx, int width, int height) {
    ctx.width = std::max(1, width);
    ctx.height = std::max(1, height);
    glViewport(0, 0, ctx.width, ctx.height);
}

Vec3 camera_forward(const Camera& camera) {
    const float cy = std::cos(camera.yaw);
    const float sy = std::sin(camera.yaw);
    const float cp = std::cos(camera.pitch);
    const float sp = std::sin(camera.pitch);
    return vec3_normalize({sy * cp, sp, cy * cp});
}

void camera_strafe(Camera& camera, float right, float up, float forward) {
    Vec3 f = camera_forward(camera);
    Vec3 world_up{0.f, 1.f, 0.f};
    Vec3 r = vec3_normalize({f.z, 0.f, -f.x});
    camera.eye = vec3_add(camera.eye, vec3_scale(r, right));
    camera.eye = vec3_add(camera.eye, vec3_scale(world_up, up));
    camera.eye = vec3_add(camera.eye, vec3_scale(f, forward));
}

Mat4 camera_view_matrix(const Camera& camera) {
    Vec3 f = camera_forward(camera);
    Vec3 target = vec3_add(camera.eye, f);
    return mat4_look_at(camera.eye, target, {0.f, 1.f, 0.f});
}

Camera mirror_camera_through_portal(const Camera& camera, const PortalPair& pair, bool from_a) {
    Camera out = camera;
    out.eye = portal_transport_position(pair, from_a, camera.eye);
    Vec3 f = camera_forward(camera);
    Vec3 target = vec3_add(camera.eye, vec3_scale(f, 3.f));
    Vec3 mirrored_target = portal_transport_position(pair, from_a, target);
    Vec3 mirrored_up = portal_transport_velocity(pair, from_a, {0.f, 1.f, 0.f});
    Vec3 new_f = vec3_normalize(vec3_sub(mirrored_target, out.eye));
    out.yaw = std::atan2(new_f.x, new_f.z);
    out.pitch = std::asin(std::clamp(new_f.y, -1.f, 1.f));
    (void)mirrored_up;
    return out;
}

void portal_gl_render_frame(
    PortalGlContext& ctx,
    const PortalScene& scene,
    const Camera& camera,
    float aspect) {
    ctx.stencil_passes = 0;
    glClearColor(0.05f, 0.06f, 0.1f, 1.f);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT);

    setup_projection(aspect);
    setup_view(camera);
    draw_scene_content(scene, false);

    render_through_portal(ctx, scene, camera, true, aspect);
    render_through_portal(ctx, scene, camera, false, aspect);

    setup_projection(aspect);
    setup_view(camera);
    draw_portal_quad(scene.portals.portal_a, scene.portal_radius, 0.15f, 0.75f, 1.f);
    draw_portal_quad(scene.portals.portal_b, scene.portal_radius, 1.f, 0.45f, 0.1f);

    SwapBuffers(static_cast<HDC>(ctx.hdc));
}
