#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif

#include <windows.h>
#include <GL/gl.h>

#include <chrono>
#include <cmath>
#include <vector>

#include "artillery.hpp"

// PEDAGOGY-SOLUTION: GFX-ART-GL-05

using namespace art2d;

namespace {

constexpr int kWidth = 960;
constexpr int kHeight = 540;
constexpr float kGravity = 120.0f;
constexpr float kDt = 1.0f / 60.0f;

HDC g_dc = nullptr;
HGLRC g_glrc = nullptr;
Terrain g_terrain;
Projectile g_projectile{};
Trail g_trail{};
bool g_space_down = false;

void init_terrain(Terrain& terrain) {
    terrain.heights.clear();
    for (int i = 0; i < 100; ++i) {
        const float x = static_cast<float>(i);
        terrain.heights.push_back(80.0f + 35.0f * std::sin(x * 0.08f) + 20.0f * std::cos(x * 0.03f));
    }
}

void reset_shot() {
    g_trail = Trail{};
    const float start_x = 40.0f;
    fire(g_projectile, 52.0f, 220.0f);
    g_projectile.pos = {start_x, g_terrain.sample(start_x) + 8.0f};
}

void simulate() {
    if (!g_projectile.alive) {
        return;
    }
    integrate(g_projectile, kDt, kGravity);
    trail_push(g_trail, g_projectile.pos);
    if (terrain_hit(g_projectile, g_terrain)) {
        crater(g_terrain, g_projectile.pos.x, 28.0f, 12.0f);
        g_projectile.alive = false;
    }
}

void render_scene() {
    glClearColor(0.07f, 0.09f, 0.16f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0.0, static_cast<double>(kWidth), 0.0, static_cast<double>(kHeight), -1.0, 1.0);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glColor3f(0.19f, 0.55f, 0.24f);
    glBegin(GL_LINE_STRIP);
    for (std::size_t i = 0; i < g_terrain.heights.size(); ++i) {
        const float x = static_cast<float>(i) * 10.0f;
        glVertex2f(x, g_terrain.heights[i]);
    }
    glEnd();

    glColor3f(0.94f, 0.82f, 0.25f);
    glPointSize(4.0f);
    glBegin(GL_POINTS);
    for (std::size_t i = 0; i < g_trail.count; ++i) {
        glVertex2f(g_trail.points[i].pos.x, g_trail.points[i].pos.y);
    }
    glEnd();

    if (g_projectile.alive) {
        glColor3f(0.96f, 0.96f, 0.96f);
        const float r = 5.0f;
        const int segments = 16;
        glBegin(GL_TRIANGLE_FAN);
        glVertex2f(g_projectile.pos.x, g_projectile.pos.y);
        for (int i = 0; i <= segments; ++i) {
            const float a = static_cast<float>(i) / static_cast<float>(segments) * 6.2831853f;
            glVertex2f(g_projectile.pos.x + std::cos(a) * r, g_projectile.pos.y + std::sin(a) * r);
        }
        glEnd();
    }
}

bool init_gl(HWND window) {
    g_dc = GetDC(window);
    if (!g_dc) {
        return false;
    }
    PIXELFORMATDESCRIPTOR pfd{};
    pfd.nSize = sizeof(pfd);
    pfd.nVersion = 1;
    pfd.dwFlags = PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL | PFD_DOUBLEBUFFER;
    pfd.iPixelType = PFD_TYPE_RGBA;
    pfd.cColorBits = 32;
    const int pf = ChoosePixelFormat(g_dc, &pfd);
    if (!pf || !SetPixelFormat(g_dc, pf, &pfd)) {
        return false;
    }
    g_glrc = wglCreateContext(g_dc);
    return g_glrc && wglMakeCurrent(g_dc, g_glrc);
}

LRESULT CALLBACK window_proc(HWND window, UINT message, WPARAM wparam, LPARAM lparam) {
    switch (message) {
    case WM_KEYDOWN:
        if (wparam == VK_ESCAPE) {
            DestroyWindow(window);
            return 0;
        }
        if (wparam == VK_SPACE && !g_space_down) {
            g_space_down = true;
            reset_shot();
        }
        return 0;
    case WM_KEYUP:
        if (wparam == VK_SPACE) {
            g_space_down = false;
        }
        return 0;
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    default:
        break;
    }
    return DefWindowProcW(window, message, wparam, lparam);
}

}  // namespace

int WINAPI wWinMain(HINSTANCE instance, HINSTANCE, PWSTR, int) {
    WNDCLASSW wc{};
    wc.lpfnWndProc = window_proc;
    wc.hInstance = instance;
    wc.lpszClassName = L"ArtilleryGl";
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
    wc.style = CS_OWNDC;
    RegisterClassW(&wc);

    HWND window = CreateWindowExW(
        0, wc.lpszClassName, L"Artillery OpenGL — Space fire, Esc quit",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE, CW_USEDEFAULT, CW_USEDEFAULT,
        kWidth, kHeight, nullptr, nullptr, instance, nullptr);
    if (!window) {
        return 1;
    }
    if (!init_gl(window)) {
        MessageBoxW(window, L"WGL init failed.", L"artillery_gl", MB_ICONERROR);
        return 2;
    }

    init_terrain(g_terrain);
    reset_shot();

    auto prev = std::chrono::steady_clock::now();
    MSG msg{};
    bool running = true;
    while (running) {
        while (PeekMessageW(&msg, nullptr, 0, 0, PM_REMOVE)) {
            if (msg.message == WM_QUIT) {
                running = false;
            }
            TranslateMessage(&msg);
            DispatchMessageW(&msg);
        }
        const auto now = std::chrono::steady_clock::now();
        (void)std::chrono::duration<float>(now - prev).count();
        prev = now;
        simulate();
        render_scene();
        SwapBuffers(g_dc);
        Sleep(1);
    }
    wglMakeCurrent(nullptr, nullptr);
    wglDeleteContext(g_glrc);
    ReleaseDC(window, g_dc);
    return 0;
}
