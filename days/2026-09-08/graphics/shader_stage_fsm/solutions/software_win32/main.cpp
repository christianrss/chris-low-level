#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif

#include <windows.h>

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <vector>

#include "shader_fsm.hpp"

// PEDAGOGY-SOLUTION: GFX-SH-ADVANCE (visual driver uses core)

using namespace shfsm;

namespace {

constexpr int kWidth = 800;
constexpr int kHeight = 480;

struct Framebuffer {
    int width = 0;
    int height = 0;
    std::vector<std::uint32_t> pixels;

    void resize(int w, int h) {
        width = std::max(1, w);
        height = std::max(1, h);
        pixels.assign(static_cast<std::size_t>(width) * height, 0u);
    }

    void clear(std::uint32_t color) {
        std::fill(pixels.begin(), pixels.end(), color);
    }

    void set_pixel(int x, int y, std::uint32_t color) {
        if (x < 0 || y < 0 || x >= width || y >= height) {
            return;
        }
        pixels[static_cast<std::size_t>(y) * width + x] = color;
    }
};

Framebuffer g_fb;
ShaderFsm g_fsm;
float g_angle = 0.0f;
float g_stage_timer = 0.0f;

std::uint32_t rgb8(float r, float g, float b) {
    const auto R = static_cast<std::uint32_t>(std::clamp(r, 0.0f, 1.0f) * 255.0f);
    const auto G = static_cast<std::uint32_t>(std::clamp(g, 0.0f, 1.0f) * 255.0f);
    const auto B = static_cast<std::uint32_t>(std::clamp(b, 0.0f, 1.0f) * 255.0f);
    return (R << 16) | (G << 8) | B;
}

void fill_tri(int x0, int y0, int x1, int y1, int x2, int y2, std::uint32_t color) {
    const int minx = std::max(0, std::min({x0, x1, x2}));
    const int maxx = std::min(g_fb.width - 1, std::max({x0, x1, x2}));
    const int miny = std::max(0, std::min({y0, y1, y2}));
    const int maxy = std::min(g_fb.height - 1, std::max({y0, y1, y2}));
    const auto edge = [](int ax, int ay, int bx, int by, int cx, int cy) {
        return (cx - ax) * (by - ay) - (cy - ay) * (bx - ax);
    };
    const int area = edge(x0, y0, x1, y1, x2, y2);
    if (area == 0) {
        return;
    }
    for (int y = miny; y <= maxy; ++y) {
        for (int x = minx; x <= maxx; ++x) {
            const int w0 = edge(x1, y1, x2, y2, x, y);
            const int w1 = edge(x2, y2, x0, y0, x, y);
            const int w2 = edge(x0, y0, x1, y1, x, y);
            if ((w0 >= 0 && w1 >= 0 && w2 >= 0) || (w0 <= 0 && w1 <= 0 && w2 <= 0)) {
                g_fb.set_pixel(x, y, color);
            }
        }
    }
}

void fill_rect(int x, int y, int w, int h, std::uint32_t color) {
    for (int yy = y; yy < y + h; ++yy) {
        for (int xx = x; xx < x + w; ++xx) {
            g_fb.set_pixel(xx, yy, color);
        }
    }
}

void render_scene() {
    g_fb.clear(rgb8(0.08f, 0.09f, 0.14f));
    const Rgb c = g_fsm.stage_color();
    const float cx = g_fb.width * 0.55f;
    const float cy = g_fb.height * 0.50f;
    const float rad = 110.0f;
    const float a0 = g_angle;
    const float a1 = g_angle + 2.094395f;
    const float a2 = g_angle + 4.188790f;
    const int x0 = static_cast<int>(cx + std::cos(a0) * rad);
    const int y0 = static_cast<int>(cy + std::sin(a0) * rad);
    const int x1 = static_cast<int>(cx + std::cos(a1) * rad);
    const int y1 = static_cast<int>(cy + std::sin(a1) * rad);
    const int x2 = static_cast<int>(cx + std::cos(a2) * rad);
    const int y2 = static_cast<int>(cy + std::sin(a2) * rad);
    fill_tri(x0, y0, x1, y1, x2, y2, rgb8(c.r, c.g, c.b));

    const int bar_h = 28;
    const int gap = 8;
    const int base_y = 24;
    const Stage stages[] = {Stage::Edit, Stage::Compile, Stage::Link, Stage::Ready};
    for (int i = 0; i < 4; ++i) {
        ShaderFsm tmp;
        while (tmp.stage() != stages[i]) {
            tmp.advance();
        }
        const Rgb sc = tmp.stage_color();
        const bool active = g_fsm.stage() == stages[i];
        const int w = active ? 160 : 90;
        fill_rect(24, base_y + i * (bar_h + gap), w, bar_h, rgb8(sc.r, sc.g, sc.b));
    }
}

void present(HWND window) {
    HDC dc = GetDC(window);
    if (!dc) {
        return;
    }
    BITMAPINFO bmi{};
    bmi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    bmi.bmiHeader.biWidth = g_fb.width;
    bmi.bmiHeader.biHeight = -g_fb.height;
    bmi.bmiHeader.biPlanes = 1;
    bmi.bmiHeader.biBitCount = 32;
    bmi.bmiHeader.biCompression = BI_RGB;
    StretchDIBits(
        dc, 0, 0, g_fb.width, g_fb.height, 0, 0, g_fb.width, g_fb.height,
        g_fb.pixels.data(), &bmi, DIB_RGB_COLORS, SRCCOPY);
    ReleaseDC(window, dc);
}

LRESULT CALLBACK window_proc(HWND window, UINT message, WPARAM wparam, LPARAM lparam) {
    switch (message) {
    case WM_SIZE:
        g_fb.resize(LOWORD(lparam), HIWORD(lparam));
        return 0;
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
    wc.lpszClassName = L"ShaderFsmSw";
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
    RegisterClassW(&wc);

    HWND window = CreateWindowExW(
        0, wc.lpszClassName, L"Shader FSM CPU — rotating triangle by stage",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE, CW_USEDEFAULT, CW_USEDEFAULT,
        kWidth, kHeight, nullptr, nullptr, instance, nullptr);
    if (!window) {
        return 1;
    }

    g_fb.resize(kWidth, kHeight);
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
        present(window);
        Sleep(1);
    }
    return 0;
}
