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

#include "descriptor.hpp"

using namespace desc;

namespace {

constexpr int kWidth = 900;
constexpr int kHeight = 480;
constexpr float kCycleSec = 1.5f;

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
DescriptorSet g_set{};
float g_time = 0.0f;
float g_cycle = 0.0f;
int g_phase = 0;

std::uint32_t rgb_f(Vec3 c) {
    return (static_cast<std::uint32_t>(std::uint8_t(c.x * 255.0f)) << 16) |
           (static_cast<std::uint32_t>(std::uint8_t(c.y * 255.0f)) << 8) |
           static_cast<std::uint32_t>(std::uint8_t(c.z * 255.0f));
}

void fill_rect(int x0, int y0, int x1, int y1, std::uint32_t color) {
    for (int y = y0; y < y1; ++y) {
        for (int x = x0; x < x1; ++x) {
            g_fb.set_pixel(x, y, color);
        }
    }
}

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
    g_fb.clear(0x00121620);
    const int panel_w = g_fb.width / 3;
    const int pad = 24;
    const float bob = std::sin(g_time * 2.0f) * 12.0f;
    for (int i = 0; i < 3; ++i) {
        const Vec3 tint = sample(g_set, i);
        const int x0 = i * panel_w + pad;
        const int x1 = (i + 1) * panel_w - pad;
        const int y0 = static_cast<int>(80 + bob);
        const int y1 = g_fb.height - 80;
        fill_rect(x0, y0, x1, y1, rgb_f(tint));
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
    wc.lpszClassName = L"DescSw";
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
    RegisterClassW(&wc);

    HWND window = CreateWindowExW(
        0, wc.lpszClassName, L"Descriptors CPU — 3 tinted panels",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE, CW_USEDEFAULT, CW_USEDEFAULT,
        kWidth, kHeight, nullptr, nullptr, instance, nullptr);
    if (!window) {
        return 1;
    }

    g_fb.resize(kWidth, kHeight);
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
        present(window);
        Sleep(1);
    }
    return 0;
}
