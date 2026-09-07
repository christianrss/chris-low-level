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

#include "artillery.hpp"

// PEDAGOGY-SOLUTION: GFX-ART-SW-04

using namespace art2d;

namespace {

constexpr int kWidth = 960;
constexpr int kHeight = 540;
constexpr float kGravity = 120.0f;
constexpr float kDt = 1.0f / 60.0f;

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
Terrain g_terrain;
Projectile g_projectile{};
Trail g_trail{};
bool g_space_down = false;

std::uint32_t rgb(std::uint8_t r, std::uint8_t g, std::uint8_t b) {
    return (static_cast<std::uint32_t>(r) << 16) |
           (static_cast<std::uint32_t>(g) << 8) |
           static_cast<std::uint32_t>(b);
}

void init_terrain(Terrain& terrain) {
    terrain.heights.clear();
    for (int i = 0; i < 100; ++i) {
        const float x = static_cast<float>(i);
        const float h = 80.0f + 35.0f * std::sin(x * 0.08f) + 20.0f * std::cos(x * 0.03f);
        terrain.heights.push_back(h);
    }
}

int world_to_screen_y(float world_y) {
    return g_fb.height - 1 - static_cast<int>(world_y);
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

void draw_circle(int cx, int cy, int radius, std::uint32_t color) {
    for (int y = -radius; y <= radius; ++y) {
        for (int x = -radius; x <= radius; ++x) {
            if (x * x + y * y <= radius * radius) {
                g_fb.set_pixel(cx + x, cy + y, color);
            }
        }
    }
}

void reset_shot() {
    g_trail = Trail{};
    const float start_x = 40.0f;
    const float start_y = g_terrain.sample(start_x) + 8.0f;
    fire(g_projectile, 52.0f, 220.0f);
    g_projectile.pos = {start_x, start_y};
    g_projectile.vel.y += kGravity * 0.02f;
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
    g_fb.clear(rgb(18, 24, 42));

    const std::uint32_t terrain_color = rgb(48, 140, 62);
    for (std::size_t i = 1; i < g_terrain.heights.size(); ++i) {
        const int x0 = static_cast<int>(static_cast<float>(i - 1) * 10.0f);
        const int x1 = static_cast<int>(static_cast<float>(i) * 10.0f);
        const int y0 = world_to_screen_y(g_terrain.heights[i - 1]);
        const int y1 = world_to_screen_y(g_terrain.heights[i]);
        draw_line(x0, y0, x1, y1, terrain_color);
        for (int x = x0; x <= x1; ++x) {
            const float t = static_cast<float>(x - x0) / static_cast<float>(std::max(1, x1 - x0));
            const float h = g_terrain.heights[i - 1] * (1.0f - t) + g_terrain.heights[i] * t;
            for (int y = world_to_screen_y(h); y < g_fb.height; ++y) {
                g_fb.set_pixel(x, y, terrain_color);
            }
        }
    }

    const std::uint32_t trail_color = rgb(240, 210, 64);
    for (std::size_t i = 0; i < g_trail.count; ++i) {
        const Vec2 p = g_trail.points[i].pos;
        draw_circle(static_cast<int>(p.x), world_to_screen_y(p.y), 2, trail_color);
    }

    if (g_projectile.alive) {
        draw_circle(
            static_cast<int>(g_projectile.pos.x),
            world_to_screen_y(g_projectile.pos.y),
            5,
            rgb(245, 245, 245));
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
    wc.lpszClassName = L"ArtillerySw";
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
    RegisterClassW(&wc);

    HWND window = CreateWindowExW(
        0, wc.lpszClassName, L"Artillery CPU — Space fire, Esc quit",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE, CW_USEDEFAULT, CW_USEDEFAULT,
        kWidth, kHeight, nullptr, nullptr, instance, nullptr);
    if (!window) {
        return 1;
    }

    g_fb.resize(kWidth, kHeight);
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
        const float frame_dt = std::chrono::duration<float>(now - prev).count();
        prev = now;
        if (frame_dt > 0.0f) {
            simulate();
        }
        render_scene();
        present(window);
        Sleep(1);
    }
    return 0;
}
