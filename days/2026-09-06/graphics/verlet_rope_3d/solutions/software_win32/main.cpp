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

#include "math.hpp"
#include "verlet.hpp"

// PEDAGOGY-SOLUTION: GFX-PORTAL-SW-07

namespace {

constexpr int kWidth = 960;
constexpr int kHeight = 540;

struct Framebuffer {
    int width = 0;
    int height = 0;
    std::vector<std::uint32_t> pixels;
    std::vector<float> depth;

    void resize(int w, int h) {
        width = std::max(1, w);
        height = std::max(1, h);
        pixels.assign(static_cast<std::size_t>(width) * height, 0u);
        depth.assign(static_cast<std::size_t>(width) * height, 1.0f);
    }

    void clear(std::uint32_t color) {
        std::fill(pixels.begin(), pixels.end(), color);
        std::fill(depth.begin(), depth.end(), 1.0f);
    }
};

Framebuffer g_fb;
VerletRope g_rope;
float g_yaw = 0.6f;
float g_pitch = 0.35f;
float g_orbit_radius = 10.0f;
bool g_space_down = false;
POINT g_last_mouse{};
bool g_have_mouse = false;

std::uint32_t rgb(std::uint8_t r, std::uint8_t g, std::uint8_t b) {
    return (static_cast<std::uint32_t>(r) << 16) |
           (static_cast<std::uint32_t>(g) << 8) |
           static_cast<std::uint32_t>(b);
}

Vec3 orbit_eye() {
    const float cy = std::cos(g_yaw);
    const float sy = std::sin(g_yaw);
    const float cp = std::cos(g_pitch);
    const float sp = std::sin(g_pitch);
    return {g_orbit_radius * sy * cp, g_orbit_radius * sp + 2.0f, g_orbit_radius * cy * cp};
}

bool project_point(Vec3 world, int& sx, int& sy, float& sz) {
    const Vec3 eye = orbit_eye();
    const Mat4 view = mat4_look_at(eye, {0.0f, 2.0f, 0.0f}, {0.0f, 1.0f, 0.0f});
    const Mat4 proj = mat4_perspective(
        0.9f,
        static_cast<float>(g_fb.width) / static_cast<float>(std::max(1, g_fb.height)),
        0.1f,
        40.0f);
    const Mat4 vp = mat4_multiply(proj, view);
    const float cx = vp.m[0] * world.x + vp.m[4] * world.y + vp.m[8] * world.z + vp.m[12];
    const float cy = vp.m[1] * world.x + vp.m[5] * world.y + vp.m[9] * world.z + vp.m[13];
    const float cz = vp.m[2] * world.x + vp.m[6] * world.y + vp.m[10] * world.z + vp.m[14];
    const float cw = vp.m[3] * world.x + vp.m[7] * world.y + vp.m[11] * world.z + vp.m[15];
    if (cw <= 0.001f) {
        return false;
    }
    const float iw = 1.0f / cw;
    const float ndc_x = cx * iw;
    const float ndc_y = cy * iw;
    const float ndc_z = cz * iw;
    sx = static_cast<int>((ndc_x * 0.5f + 0.5f) * static_cast<float>(g_fb.width));
    sy = static_cast<int>((1.0f - (ndc_y * 0.5f + 0.5f)) * static_cast<float>(g_fb.height));
    sz = ndc_z * 0.5f + 0.5f;
    return sx >= 0 && sy >= 0 && sx < g_fb.width && sy < g_fb.height;
}

void plot_depth(int x, int y, float z, std::uint32_t color) {
    if (x < 0 || y < 0 || x >= g_fb.width || y >= g_fb.height) {
        return;
    }
    const std::size_t i = static_cast<std::size_t>(y) * g_fb.width + x;
    if (z < g_fb.depth[i]) {
        g_fb.depth[i] = z;
        g_fb.pixels[i] = color;
    }
}

void draw_line_3d(Vec3 a, Vec3 b, std::uint32_t color) {
    int x0, y0, x1, y1;
    float z0, z1;
    if (!project_point(a, x0, y0, z0) || !project_point(b, x1, y1, z1)) {
        return;
    }
    const int dx = std::abs(x1 - x0);
    const int dy = std::abs(y1 - y0);
    const int sx = x0 < x1 ? 1 : -1;
    const int sy = y0 < y1 ? 1 : -1;
    int err = dx - dy;
    int steps = std::max(dx, dy) + 1;
    for (int i = 0; i <= steps; ++i) {
        const float t = static_cast<float>(i) / static_cast<float>(steps);
        plot_depth(x0, y0, z0 * (1.0f - t) + z1 * t, color);
        if (x0 == x1 && y0 == y1) {
            break;
        }
        const int e2 = 2 * err;
        if (e2 > -dy) {
            err -= dy;
            x0 += sx;
        }
        if (e2 < dx) {
            err += dx;
            y0 += sy;
        }
    }
}

void draw_room() {
    const std::uint32_t wall = rgb(70, 90, 120);
    const float s = 6.0f;
    const float h = 4.0f;
    const Vec3 corners[] = {
        {-s, 0, -s}, {s, 0, -s}, {s, 0, s}, {-s, 0, s},
        {-s, h, -s}, {s, h, -s}, {s, h, s}, {-s, h, s}};
    const int edges[][2] = {
        {0, 1}, {1, 2}, {2, 3}, {3, 0},
        {4, 5}, {5, 6}, {6, 7}, {7, 4},
        {0, 4}, {1, 5}, {2, 6}, {3, 7}};
    for (const auto& e : edges) {
        draw_line_3d(corners[e[0]], corners[e[1]], wall);
    }
}

void draw_rope() {
    const std::uint32_t rope_color = rgb(230, 210, 90);
    for (std::size_t i = 1; i < g_rope.points.size(); ++i) {
        draw_line_3d(g_rope.points[i - 1], g_rope.points[i], rope_color);
    }
    if (!g_rope.points.empty()) {
        const Vec3& w = g_rope.points.back();
        draw_line_3d(w, {w.x + 0.35f, w.y - 0.35f, w.z}, rgb(220, 120, 80));
        draw_line_3d(w, {w.x - 0.35f, w.y - 0.35f, w.z}, rgb(220, 120, 80));
        draw_line_3d(w, {w.x, w.y - 0.35f, w.z + 0.35f}, rgb(220, 120, 80));
        draw_line_3d(w, {w.x, w.y - 0.35f, w.z - 0.35f}, rgb(220, 120, 80));
    }
}

void impulse_weight() {
    if (g_rope.points.size() < 2) {
        return;
    }
    Vec3& w = g_rope.points.back();
    w.x += 0.4f;
    g_rope.prev_points.back() = w;
}

void present(HWND window) {
    HDC dc = GetDC(window);
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
            impulse_weight();
        }
        return 0;
    case WM_KEYUP:
        if (wparam == VK_SPACE) {
            g_space_down = false;
        }
        return 0;
    case WM_MOUSEMOVE: {
        const POINT cur{static_cast<short>(LOWORD(lparam)), static_cast<short>(HIWORD(lparam))};
        if (g_have_mouse) {
            g_yaw += (cur.x - g_last_mouse.x) * 0.005f;
            g_pitch = std::clamp(g_pitch - (cur.y - g_last_mouse.y) * 0.005f, -1.2f, 1.2f);
        }
        g_last_mouse = cur;
        g_have_mouse = true;
        return 0;
    }
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
    wc.lpszClassName = L"PortalSw";
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
    RegisterClassW(&wc);

    HWND window = CreateWindowExW(
        0, wc.lpszClassName, L"Verlet rope CPU — drag orbit, Space impulse, Esc quit",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE, CW_USEDEFAULT, CW_USEDEFAULT,
        kWidth, kHeight, nullptr, nullptr, instance, nullptr);
    if (!window) {
        return 1;
    }

    g_fb.resize(kWidth, kHeight);
    verlet_init_rope(g_rope, {0.0f, 4.0f, 0.0f}, {0.0f, 1.5f, 0.0f}, 12);

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
        verlet_step(g_rope, {0.0f, -9.8f, 0.0f}, std::min(dt, 0.033f), 6);
        g_fb.clear(rgb(16, 20, 28));
        draw_room();
        draw_rope();
        present(window);
        Sleep(1);
    }
    return 0;
}
