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

#include "gpu_timer.hpp"

using namespace gputq;

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
GpuTimer g_timer;
float g_t = 0.0f;

std::uint32_t rgb(std::uint8_t r, std::uint8_t g, std::uint8_t b) {
    return (static_cast<std::uint32_t>(r) << 16) | (static_cast<std::uint32_t>(g) << 8) | b;
}

void fill_rect(int x, int y, int w, int h, std::uint32_t color) {
    for (int yy = y; yy < y + h; ++yy) {
        for (int xx = x; xx < x + w; ++xx) {
            g_fb.set_pixel(xx, yy, color);
        }
    }
}

void fill_quad_rot(float cx, float cy, float half, float angle, std::uint32_t color) {
    const float c = std::cos(angle);
    const float s = std::sin(angle);
    const float pts[4][2] = {{-half, -half}, {half, -half}, {half, half}, {-half, half}};
    int xi[4], yi[4];
    for (int i = 0; i < 4; ++i) {
        const float x = pts[i][0] * c - pts[i][1] * s + cx;
        const float y = pts[i][0] * s + pts[i][1] * c + cy;
        xi[i] = static_cast<int>(x);
        yi[i] = static_cast<int>(y);
    }
    auto edge = [](int ax, int ay, int bx, int by, int px, int py) {
        return (px - ax) * (by - ay) - (py - ay) * (bx - ax);
    };
    auto fill_tri = [&](int i0, int i1, int i2) {
        const int minx = std::max(0, std::min({xi[i0], xi[i1], xi[i2]}));
        const int maxx = std::min(g_fb.width - 1, std::max({xi[i0], xi[i1], xi[i2]}));
        const int miny = std::max(0, std::min({yi[i0], yi[i1], yi[i2]}));
        const int maxy = std::min(g_fb.height - 1, std::max({yi[i0], yi[i1], yi[i2]}));
        for (int y = miny; y <= maxy; ++y) {
            for (int x = minx; x <= maxx; ++x) {
                const int w0 = edge(xi[i1], yi[i1], xi[i2], yi[i2], x, y);
                const int w1 = edge(xi[i2], yi[i2], xi[i0], yi[i0], x, y);
                const int w2 = edge(xi[i0], yi[i0], xi[i1], yi[i1], x, y);
                if ((w0 >= 0 && w1 >= 0 && w2 >= 0) || (w0 <= 0 && w1 <= 0 && w2 <= 0)) {
                    g_fb.set_pixel(x, y, color);
                }
            }
        }
    };
    fill_tri(0, 1, 2);
    fill_tri(0, 2, 3);
}

void render_scene() {
    g_fb.clear(rgb(16, 20, 32));
    const double ms = g_timer.last_ms();
    const int max_h = g_fb.height - 40;
    const int bar_h = std::clamp(static_cast<int>(ms * 40.0), 4, max_h);
    fill_rect(30, g_fb.height - 20 - bar_h, 40, bar_h, rgb(80, 200, 120));

    const float bounce = std::fabs(std::sin(g_t * 2.0f));
    const float cx = g_fb.width * 0.55f;
    const float cy = g_fb.height * 0.35f + bounce * 120.0f;
    fill_quad_rot(cx, cy, 48.0f, g_t * 1.5f, rgb(240, 180, 60));
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
    wc.lpszClassName = L"GpuTimerSw";
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
    RegisterClassW(&wc);

    HWND window = CreateWindowExW(
        0, wc.lpszClassName, L"GPU Timer CPU — bar = last_ms",
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
        g_t += dt;
        g_timer.begin();
        render_scene();
        present(window);
        g_timer.end();
        Sleep(1);
    }
    return 0;
}
