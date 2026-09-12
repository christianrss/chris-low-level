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

#include "shader_fsm.hpp"

using namespace shfsm;

namespace {

constexpr int kWidth = 800;
constexpr int kHeight = 480;

HDC g_dc = nullptr;
HGLRC g_glrc = nullptr;
ShaderFsm g_fsm;
float g_angle = 0.0f;
float g_stage_timer = 0.0f;

void render_scene() {
    glClearColor(0.08f, 0.09f, 0.14f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0.0, static_cast<double>(kWidth), 0.0, static_cast<double>(kHeight), -1.0, 1.0);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    const Rgb c = g_fsm.stage_color();
    const float cx = kWidth * 0.55f;
    const float cy = kHeight * 0.50f;
    const float rad = 110.0f;
    glColor3f(c.r, c.g, c.b);
    glBegin(GL_TRIANGLES);
    glVertex2f(cx + std::cos(g_angle) * rad, cy + std::sin(g_angle) * rad);
    glVertex2f(cx + std::cos(g_angle + 2.094395f) * rad, cy + std::sin(g_angle + 2.094395f) * rad);
    glVertex2f(cx + std::cos(g_angle + 4.188790f) * rad, cy + std::sin(g_angle + 4.188790f) * rad);
    glEnd();

    const Stage stages[] = {Stage::Edit, Stage::Compile, Stage::Link, Stage::Ready};
    for (int i = 0; i < 4; ++i) {
        ShaderFsm tmp;
        while (tmp.stage() != stages[i]) {
            tmp.advance();
        }
        const Rgb sc = tmp.stage_color();
        const bool active = g_fsm.stage() == stages[i];
        const float w = active ? 160.0f : 90.0f;
        const float y = static_cast<float>(kHeight - 52 - i * 36);
        glColor3f(sc.r, sc.g, sc.b);
        glBegin(GL_QUADS);
        glVertex2f(24.0f, y);
        glVertex2f(24.0f + w, y);
        glVertex2f(24.0f + w, y + 28.0f);
        glVertex2f(24.0f, y + 28.0f);
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
        if (wparam == 'R') {
            g_fsm.reset();
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
    wc.lpszClassName = L"ShaderFsmGl";
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
    wc.style = CS_OWNDC;
    RegisterClassW(&wc);

    HWND window = CreateWindowExW(
        0, wc.lpszClassName, L"Shader FSM OpenGL — rotating triangle by stage",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE, CW_USEDEFAULT, CW_USEDEFAULT,
        kWidth, kHeight, nullptr, nullptr, instance, nullptr);
    if (!window) {
        return 1;
    }
    if (!init_gl(window)) {
        MessageBoxW(window, L"WGL init failed.", L"shader_fsm_gl", MB_ICONERROR);
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
        g_angle += dt * 1.2f;
        g_stage_timer += dt;
        if (g_stage_timer >= 1.5f) {
            g_stage_timer = 0.0f;
            g_fsm.advance();
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
