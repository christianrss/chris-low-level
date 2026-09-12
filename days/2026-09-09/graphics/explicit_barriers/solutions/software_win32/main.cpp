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

#include "barriers.hpp"

using namespace barr;

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
Resource g_res{};
float g_t = 0.0f;
float g_phase = 0.0f;

std::uint32_t rgb(std::uint8_t r, std::uint8_t g, std::uint8_t b) {
    return (static_cast<std::uint32_t>(r) << 16) | (static_cast<std::uint32_t>(g) << 8) | b;
}

std::uint32_t clear_for_state(ResourceState s) {
    switch (s) {
    case ResourceState::Undefined:
        return rgb(30, 30, 36);
    case ResourceState::CopyDst:
        return rgb(40, 60, 110);
    case ResourceState::ShaderRead:
        return rgb(50, 90, 70);
    case ResourceState::RenderTarget:
        return rgb(110, 50, 50);
    case ResourceState::Present:
        return rgb(90, 70, 120);
    }
    return rgb(0, 0, 0);
}

void fill_circle(int cx, int cy, int radius, std::uint32_t color) {
    for (int y = -radius; y <= radius; ++y) {
        for (int x = -radius; x <= radius; ++x) {
            if (x * x + y * y <= radius * radius) {
                g_fb.set_pixel(cx + x, cy + y, color);
            }
        }
    }
}

void render_scene() {
    g_fb.clear(clear_for_state(g_res.state));
    const float x = 80.0f + std::fmod(g_t * 140.0f, static_cast<float>(g_fb.width - 160));
    const float y = g_fb.height * 0.5f + std::sin(g_t * 3.0f) * 80.0f;
    fill_circle(static_cast<int>(x), static_cast<int>(y), 28, rgb(240, 220, 80));
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
    wc.lpszClassName = L"BarriersSw";
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
    RegisterClassW(&wc);

    HWND window = CreateWindowExW(
        0, wc.lpszClassName, L"Explicit Barriers CPU — state clear + sprite",
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
        g_phase += dt;
        if (g_phase >= 1.0f) {
            g_phase = 0.0f;
            tick_barrier(g_res);
        }
        render_scene();
        present(window);
        Sleep(1);
    }
    return 0;
}
