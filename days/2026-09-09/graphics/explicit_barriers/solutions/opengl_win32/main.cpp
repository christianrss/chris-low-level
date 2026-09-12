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

#include "barriers.hpp"

using namespace barr;

namespace {

constexpr int kWidth = 800;
constexpr int kHeight = 480;

HDC g_dc = nullptr;
HGLRC g_glrc = nullptr;
Resource g_res{};
float g_t = 0.0f;
float g_phase = 0.0f;

void clear_color_for_state(ResourceState s) {
    switch (s) {
    case ResourceState::Undefined:
        glClearColor(0.12f, 0.12f, 0.14f, 1.0f);
        break;
    case ResourceState::CopyDst:
        glClearColor(0.16f, 0.24f, 0.43f, 1.0f);
        break;
    case ResourceState::ShaderRead:
        glClearColor(0.20f, 0.35f, 0.27f, 1.0f);
        break;
    case ResourceState::RenderTarget:
        glClearColor(0.43f, 0.20f, 0.20f, 1.0f);
        break;
    case ResourceState::Present:
        glClearColor(0.35f, 0.27f, 0.47f, 1.0f);
        break;
    }
}

void render_scene() {
    clear_color_for_state(g_res.state);
    glClear(GL_COLOR_BUFFER_BIT);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0.0, static_cast<double>(kWidth), 0.0, static_cast<double>(kHeight), -1.0, 1.0);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    const float x = 80.0f + std::fmod(g_t * 140.0f, static_cast<float>(kWidth - 160));
    const float y = kHeight * 0.5f + std::sin(g_t * 3.0f) * 80.0f;
    glColor3f(0.94f, 0.86f, 0.31f);
    const int seg = 24;
    glBegin(GL_TRIANGLE_FAN);
    glVertex2f(x, y);
    for (int i = 0; i <= seg; ++i) {
        const float a = static_cast<float>(i) / static_cast<float>(seg) * 6.2831853f;
        glVertex2f(x + std::cos(a) * 28.0f, y + std::sin(a) * 28.0f);
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
    wc.lpszClassName = L"BarriersGl";
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
    wc.style = CS_OWNDC;
    RegisterClassW(&wc);

    HWND window = CreateWindowExW(
        0, wc.lpszClassName, L"Explicit Barriers OpenGL — state clear + sprite",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE, CW_USEDEFAULT, CW_USEDEFAULT,
        kWidth, kHeight, nullptr, nullptr, instance, nullptr);
    if (!window) {
        return 1;
    }
    if (!init_gl(window)) {
        MessageBoxW(window, L"WGL init failed.", L"barriers_gl", MB_ICONERROR);
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
        g_phase += dt;
        if (g_phase >= 1.0f) {
            g_phase = 0.0f;
            tick_barrier(g_res);
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
