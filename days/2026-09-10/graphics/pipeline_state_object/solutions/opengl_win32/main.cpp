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

#include "pso.hpp"

using namespace pso;

namespace {

constexpr int kWidth = 800;
constexpr int kHeight = 600;
constexpr float kCycleSec = 2.0f;

HDC g_dc = nullptr;
HGLRC g_glrc = nullptr;
PipelineState g_active{};
int g_preset = 0;
float g_cycle_timer = 0.0f;
float g_time = 0.0f;

void render_scene() {
    glClearColor(0.07f, 0.09f, 0.13f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0.0, static_cast<double>(kWidth), 0.0, static_cast<double>(kHeight), -1.0, 1.0);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    const float cx = kWidth * 0.5f;
    const float cy = kHeight * 0.5f + std::sin(g_time * 1.2f) * 18.0f;
    const float ang = g_time * 0.6f;
    const float s = 140.0f;
    auto rot = [&](float lx, float ly) {
        const float c = std::cos(ang);
        const float sn = std::sin(ang);
        return std::pair<float, float>{cx + c * lx - sn * ly, cy + sn * lx + c * ly};
    };
    const auto p0 = rot(0.0f, -s);
    const auto p1 = rot(-s, s * 0.7f);
    const auto p2 = rot(s, s * 0.7f);

    glColor3f(g_active.r, g_active.g, g_active.b);
    if (g_active.fill_mode == kFillSolid) {
        glBegin(GL_TRIANGLES);
        glVertex2f(p0.first, p0.second);
        glVertex2f(p1.first, p1.second);
        glVertex2f(p2.first, p2.second);
        glEnd();
    } else {
        glBegin(GL_LINE_LOOP);
        glVertex2f(p0.first, p0.second);
        glVertex2f(p1.first, p1.second);
        glVertex2f(p2.first, p2.second);
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
    wc.lpszClassName = L"PsoGl";
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
    wc.style = CS_OWNDC;
    RegisterClassW(&wc);

    HWND window = CreateWindowExW(
        0, wc.lpszClassName, L"PSO OpenGL — auto-cycle fill/wire/color",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE, CW_USEDEFAULT, CW_USEDEFAULT,
        kWidth, kHeight, nullptr, nullptr, instance, nullptr);
    if (!window) {
        return 1;
    }
    if (!init_gl(window)) {
        MessageBoxW(window, L"WGL init failed.", L"pso_gl", MB_ICONERROR);
        return 2;
    }

    bind(g_active, create_default_pso());
    g_preset = 0;

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
        const float dt = std::chrono::duration<float>(now - prev).count();
        prev = now;
        g_time += dt;
        g_cycle_timer += dt;
        if (g_cycle_timer >= kCycleSec) {
            g_cycle_timer = 0.0f;
            cycle_pso(g_active, g_preset);
        }
        render_scene();
        SwapBuffers(g_dc);
        Sleep(1);
    }
    wglMakeCurrent(nullptr, nullptr);
    wglDeleteContext(g_glrc);
    ReleaseDC(window, g_dc);
    return 0;
}
