// PEDAGOGY-TEST: GFX-PORTAL-06: OpenGL demo (manual GPU — Caso 6)
// PEDAGOGY-SOLUTION: GFX-PORTAL-06
#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif

#include "portal.hpp"
#include "render_gl.hpp"
#include "sphere_portal.hpp"
#include "verlet.hpp"

#include <windows.h>

#include <chrono>
#include <cmath>
#include <cstring>

namespace {

constexpr int kWidth = 1280;
constexpr int kHeight = 720;

PortalGlContext g_gl;
PortalScene g_scene;
Camera g_camera;
bool g_keys[256]{};
bool g_have_mouse = false;
POINT g_last_mouse{};
float g_throw_cooldown = 0.f;

PortalScene make_default_scene() {
    PortalScene scene{};
    scene.portals = make_portal_pair(
        PortalFrame{{0.f, 2.f, -4.f}, {0.f, 0.f, 1.f}, {0.f, 1.f, 0.f}},
        PortalFrame{{0.f, 2.f, 4.f}, {0.f, 0.f, -1.f}, {0.f, 1.f, 0.f}});
    verlet_init_rope(scene.rope, {2.f, 4.f, 0.f}, {2.f, 1.5f, 0.f}, 10);
    scene.sphere = Sphere{{0.f, 1.5f, 2.f}, 0.35f, {0.f, 0.f, 0.f}};
    return scene;
}

void throw_sphere() {
    Vec3 f = camera_forward(g_camera);
    g_scene.sphere.velocity = vec3_add(g_scene.sphere.velocity, vec3_scale(f, 8.f));
    g_scene.sphere.center = vec3_add(g_scene.sphere.center, vec3_scale(f, 0.2f));
    g_throw_cooldown = 0.35f;
}

void simulate(float dt) {
    verlet_step(g_scene.rope, {0.f, -9.8f, 0.f}, dt, 6);
    sphere_step(g_scene.sphere, {0.f, -9.8f, 0.f}, dt, 0.f);
    if (try_sphere_teleport(g_scene.sphere, g_scene.portals, true, g_scene.portal_radius)) {
    } else {
        try_sphere_teleport(g_scene.sphere, g_scene.portals, false, g_scene.portal_radius);
    }
    if (g_throw_cooldown > 0.f) {
        g_throw_cooldown -= dt;
    }
}

void handle_input(float dt) {
    const float speed = 4.f * dt;
    if (g_keys['W']) camera_strafe(g_camera, 0.f, 0.f, speed);
    if (g_keys['S']) camera_strafe(g_camera, 0.f, 0.f, -speed);
    if (g_keys['A']) camera_strafe(g_camera, -speed, 0.f, 0.f);
    if (g_keys['D']) camera_strafe(g_camera, speed, 0.f, 0.f);
    if (g_keys[VK_SPACE] && g_throw_cooldown <= 0.f) {
        throw_sphere();
    }
}

LRESULT CALLBACK window_proc(HWND window, UINT message, WPARAM wparam, LPARAM lparam) {
    switch (message) {
    case WM_SIZE:
        portal_gl_resize(g_gl, LOWORD(lparam), HIWORD(lparam));
        return 0;
    case WM_KEYDOWN:
        g_keys[wparam & 0xFF] = true;
        if (wparam == VK_ESCAPE) {
            DestroyWindow(window);
        }
        return 0;
    case WM_KEYUP:
        g_keys[wparam & 0xFF] = false;
        return 0;
    case WM_LBUTTONDOWN:
        if (g_throw_cooldown <= 0.f) {
            throw_sphere();
        }
        return 0;
    case WM_MOUSEMOVE: {
        const POINT current{static_cast<short>(LOWORD(lparam)), static_cast<short>(HIWORD(lparam))};
        if (g_have_mouse) {
            constexpr float sens = 0.004f;
            g_camera.yaw += (current.x - g_last_mouse.x) * sens;
            g_camera.pitch -= (current.y - g_last_mouse.y) * sens;
            if (g_camera.pitch > 1.45f) g_camera.pitch = 1.45f;
            if (g_camera.pitch < -1.45f) g_camera.pitch = -1.45f;
        }
        g_last_mouse = current;
        g_have_mouse = true;
        return 0;
    }
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    default:
        break;
    }
    return DefWindowProcA(window, message, wparam, lparam);
}

} // namespace

int WINAPI WinMain(HINSTANCE instance, HINSTANCE, LPSTR, int) {
    WNDCLASSA wc{};
    wc.lpfnWndProc = window_proc;
    wc.hInstance = instance;
    wc.lpszClassName = "PortalVerletDemo";
    wc.hCursor = LoadCursorA(nullptr, IDC_ARROW);
    wc.style = CS_OWNDC;
    RegisterClassA(&wc);

    HWND window = CreateWindowExA(
        0, wc.lpszClassName, "Portal Verlet Physics — WASD move, mouse look, click/Space throw",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE, CW_USEDEFAULT, CW_USEDEFAULT, kWidth, kHeight,
        nullptr, nullptr, instance, nullptr);
    if (!window) return 1;

    if (!portal_gl_init(g_gl, window)) {
        MessageBoxA(window, "WGL init failed (need stencil buffer).", "portal_demo", MB_ICONERROR);
        return 2;
    }
    portal_gl_resize(g_gl, kWidth, kHeight);
    g_scene = make_default_scene();

    auto prev = std::chrono::steady_clock::now();
    MSG msg{};
    bool running = true;
    while (running) {
        while (PeekMessageA(&msg, nullptr, 0, 0, PM_REMOVE)) {
            if (msg.message == WM_QUIT) {
                running = false;
            }
            TranslateMessage(&msg);
            DispatchMessageA(&msg);
        }
        const auto now = std::chrono::steady_clock::now();
        const float dt = std::min(0.05f, std::chrono::duration<float>(now - prev).count());
        prev = now;
        handle_input(dt);
        simulate(dt);
        portal_gl_render_frame(g_gl, g_scene, g_camera, static_cast<float>(g_gl.width) / g_gl.height);
    }

    portal_gl_shutdown(g_gl);
    return 0;
}
