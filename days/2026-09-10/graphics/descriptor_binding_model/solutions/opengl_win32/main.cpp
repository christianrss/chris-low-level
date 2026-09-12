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

#include "descriptor.hpp"

using namespace desc;

namespace {

constexpr int kWidth = 900;
constexpr int kHeight = 480;
constexpr float kCycleSec = 1.5f;

HDC g_dc = nullptr;
HGLRC g_glrc = nullptr;
DescriptorSet g_set{};
float g_time = 0.0f;
float g_cycle = 0.0f;
int g_phase = 0;

void rebind_phase() {
    const Vec3 palette[3] = {
        {1.0f, 0.25f, 0.20f},
        {0.20f, 0.90f, 0.35f},
        {0.25f, 0.45f, 1.0f},
    };
    for (int i = 0; i < 3; ++i) {
        bind(g_set, i, palette[(g_phase + i) % 3]);
    }
}

void render_scene() {
    glClearColor(0.07f, 0.09f, 0.13f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0.0, static_cast<double>(kWidth), 0.0, static_cast<double>(kHeight), -1.0, 1.0);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    const float panel_w = kWidth / 3.0f;
    const float pad = 24.0f;
    const float bob = std::sin(g_time * 2.0f) * 12.0f;
    for (int i = 0; i < 3; ++i) {
        const Vec3 tint = sample(g_set, i);
        const float x0 = i * panel_w + pad;
        const float x1 = (i + 1) * panel_w - pad;
        const float y0 = 80.0f + bob;
        const float y1 = kHeight - 80.0f;
        glColor3f(tint.x, tint.y, tint.z);
        glBegin(GL_QUADS);
        glVertex2f(x0, y0);
        glVertex2f(x1, y0);
        glVertex2f(x1, y1);
        glVertex2f(x0, y1);
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
    wc.lpszClassName = L"DescGl";
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
    wc.style = CS_OWNDC;
    RegisterClassW(&wc);

    HWND window = CreateWindowExW(
        0, wc.lpszClassName, L"Descriptors OpenGL — 3 tinted panels",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE, CW_USEDEFAULT, CW_USEDEFAULT,
        kWidth, kHeight, nullptr, nullptr, instance, nullptr);
    if (!window) {
        return 1;
    }
    if (!init_gl(window)) {
        MessageBoxW(window, L"WGL init failed.", L"desc_gl", MB_ICONERROR);
        return 2;
    }

    const DescriptorLayout layout = make_layout(3);
    g_set.slot_count = layout.slot_count;
    rebind_phase();

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
        g_cycle += dt;
        if (g_cycle >= kCycleSec) {
            g_cycle = 0.0f;
            g_phase = (g_phase + 1) % 3;
            rebind_phase();
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
