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

#include "pso.hpp"

using namespace pso;

namespace {

constexpr int kWidth = 800;
constexpr int kHeight = 600;
constexpr float kCycleSec = 2.0f;

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
PipelineState g_active{};
int g_preset = 0;
float g_cycle_timer = 0.0f;
float g_time = 0.0f;

std::uint32_t rgb(std::uint8_t r, std::uint8_t g, std::uint8_t b) {
    return (static_cast<std::uint32_t>(r) << 16) |
           (static_cast<std::uint32_t>(g) << 8) |
           static_cast<std::uint32_t>(b);
}

void draw_line(int x0, int y0, int x1, int y1, std::uint32_t color) {
    const int dx = std::abs(x1 - x0);
    const int dy = std::abs(y1 - y0);
    const int sx = x0 < x1 ? 1 : -1;
    const int sy = y0 < y1 ? 1 : -1;
    int err = dx - dy;
    int x = x0;
    int y = y0;
    while (true) {
        g_fb.set_pixel(x, y, color);
        if (x == x1 && y == y1) {
            break;
        }
        const int e2 = 2 * err;
        if (e2 > -dy) {
            err -= dy;
            x += sx;
        }
        if (e2 < dx) {
            err += dx;
            y += sy;
        }
    }
}

void fill_triangle(int x0, int y0, int x1, int y1, int x2, int y2, std::uint32_t color) {
    const int min_x = std::max(0, std::min({x0, x1, x2}));
    const int max_x = std::min(g_fb.width - 1, std::max({x0, x1, x2}));
    const int min_y = std::max(0, std::min({y0, y1, y2}));
    const int max_y = std::min(g_fb.height - 1, std::max({y0, y1, y2}));
    auto edge = [](int ax, int ay, int bx, int by, int cx, int cy) {
        return (cx - ax) * (by - ay) - (cy - ay) * (bx - ax);
    };
    const int area = edge(x0, y0, x1, y1, x2, y2);
    if (area == 0) {
        return;
    }
    for (int y = min_y; y <= max_y; ++y) {
        for (int x = min_x; x <= max_x; ++x) {
            const int w0 = edge(x1, y1, x2, y2, x, y);
            const int w1 = edge(x2, y2, x0, y0, x, y);
            const int w2 = edge(x0, y0, x1, y1, x, y);
            if ((w0 >= 0 && w1 >= 0 && w2 >= 0) || (w0 <= 0 && w1 <= 0 && w2 <= 0)) {
                g_fb.set_pixel(x, y, color);
            }
        }
    }
}

void render_scene() {
    g_fb.clear(rgb(18, 22, 34));
    const float cx = static_cast<float>(g_fb.width) * 0.5f;
    const float cy = static_cast<float>(g_fb.height) * 0.5f + std::sin(g_time * 1.2f) * 18.0f;
    const float ang = g_time * 0.6f;
    const float s = 140.0f;
    auto rot = [&](float lx, float ly) {
        const float c = std::cos(ang);
        const float sn = std::sin(ang);
        return std::pair<int, int>{
            static_cast<int>(cx + c * lx - sn * ly),
            static_cast<int>(cy + sn * lx + c * ly)};
    };
    const auto p0 = rot(0.0f, -s);
    const auto p1 = rot(-s, s * 0.7f);
    const auto p2 = rot(s, s * 0.7f);
    const auto color = rgb(
        static_cast<std::uint8_t>(g_active.r * 255.0f),
        static_cast<std::uint8_t>(g_active.g * 255.0f),
        static_cast<std::uint8_t>(g_active.b * 255.0f));
    if (g_active.fill_mode == kFillSolid) {
        fill_triangle(p0.first, p0.second, p1.first, p1.second, p2.first, p2.second, color);
    } else {
        draw_line(p0.first, p0.second, p1.first, p1.second, color);
        draw_line(p1.first, p1.second, p2.first, p2.second, color);
        draw_line(p2.first, p2.second, p0.first, p0.second, color);
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
    wc.lpszClassName = L"PsoSw";
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
    RegisterClassW(&wc);

    HWND window = CreateWindowExW(
        0, wc.lpszClassName, L"PSO CPU — auto-cycle fill/wire/color",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE, CW_USEDEFAULT, CW_USEDEFAULT,
        kWidth, kHeight, nullptr, nullptr, instance, nullptr);
    if (!window) {
        return 1;
    }

    g_fb.resize(kWidth, kHeight);
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
        present(window);
        Sleep(1);
    }
    return 0;
}
