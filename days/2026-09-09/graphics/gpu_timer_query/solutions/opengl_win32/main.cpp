#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif

#include <windows.h>
#include <GL/gl.h>

#include <algorithm>
#include <chrono>
#include <cmath>

#include "gpu_timer.hpp"

using namespace gputq;

namespace {

constexpr int kWidth = 800;
constexpr int kHeight = 480;

HDC g_dc = nullptr;
HGLRC g_glrc = nullptr;
GpuTimer g_timer;
float g_t = 0.0f;

void render_scene() {
    glClearColor(0.06f, 0.08f, 0.12f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0.0, static_cast<double>(kWidth), 0.0, static_cast<double>(kHeight), -1.0, 1.0);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    const double ms = g_timer.last_ms();
    const float max_h = static_cast<float>(kHeight - 40);
    const float bar_h = std::clamp(static_cast<float>(ms * 40.0), 4.0f, max_h);
    glColor3f(0.31f, 0.78f, 0.47f);
    glBegin(GL_QUADS);
    glVertex2f(30.0f, 20.0f);
    glVertex2f(70.0f, 20.0f);
    glVertex2f(70.0f, 20.0f + bar_h);
    glVertex2f(30.0f, 20.0f + bar_h);
    glEnd();

    const float bounce = std::fabs(std::sin(g_t * 2.0f));
    const float cx = kWidth * 0.55f;
    const float cy = kHeight * 0.35f + bounce * 120.0f;
    const float half = 48.0f;
    const float ang = g_t * 1.5f;
    const float c = std::cos(ang);
    const float s = std::sin(ang);
    glColor3f(0.94f, 0.71f, 0.24f);
    glBegin(GL_QUADS);
    for (int i = 0; i < 4; ++i) {
        const float lx = (i == 0 || i == 3) ? -half : half;
        const float ly = (i < 2) ? -half : half;
        glVertex2f(cx + lx * c - ly * s, cy + lx * s + ly * c);
    }
    glEnd();
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
    wc.lpszClassName = L"GpuTimerGl";
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
    wc.style = CS_OWNDC;
    RegisterClassW(&wc);

    HWND window = CreateWindowExW(
        0, wc.lpszClassName, L"GPU Timer OpenGL — bar = last_ms",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE, CW_USEDEFAULT, CW_USEDEFAULT,
        kWidth, kHeight, nullptr, nullptr, instance, nullptr);
    if (!window) {
        return 1;
    }
    if (!init_gl(window)) {
        MessageBoxW(window, L"WGL init failed.", L"gpu_timer_gl", MB_ICONERROR);
        return 2;
    }

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
        g_t += dt;
        g_timer.begin();
        render_scene();
        SwapBuffers(g_dc);
        g_timer.end();
        Sleep(1);
    }
    wglMakeCurrent(nullptr, nullptr);
    wglDeleteContext(g_glrc);
    ReleaseDC(window, g_dc);
    return 0;
}
