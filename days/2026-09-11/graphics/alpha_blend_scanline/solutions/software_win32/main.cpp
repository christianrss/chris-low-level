#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <vector>
#include "blend.hpp"

using blendlab::Pixel;
using blendlab::Sprite;

namespace {

struct Framebuffer {
    int width = 0;
    int height = 0;
    std::vector<std::uint32_t> pixels;
    void resize(int w, int h) {
        width = std::max(1, w);
        height = std::max(1, h);
        pixels.assign(static_cast<std::size_t>(width) * height, 0u);
    }
};

std::uint32_t rgb(int r, int g, int b) {
    return (std::uint32_t(r) << 16) | (std::uint32_t(g) << 8) | std::uint32_t(b);
}

Framebuffer g_fb;
std::vector<Pixel> g_pix;
Sprite g_a{80, 80, 140, 90, 90, 70, {255, 40, 40, 140}};
Sprite g_b{400, 200, -110, 120, 110, 80, {40, 80, 255, 160}};

void blit_sprite(const Sprite& s) {
    std::vector<Pixel> row(static_cast<std::size_t>(s.w), s.color);
    for (int y = 0; y < s.h; ++y) {
        const int py = static_cast<int>(s.y) + y;
        if (py < 0 || py >= g_fb.height) {
            continue;
        }
        int start = 0;
        int count = s.w;
        int dst_x = static_cast<int>(s.x);
        if (dst_x < 0) {
            start = -dst_x;
            count -= start;
            dst_x = 0;
        }
        if (dst_x + count > g_fb.width) {
            count = g_fb.width - dst_x;
        }
        if (count <= 0) {
            continue;
        }
        blendlab::blend_scanline(
            &g_pix[static_cast<std::size_t>(py) * g_fb.width + dst_x],
            row.data() + start,
            count);
    }
}

void present(HWND window) {
    for (std::size_t i = 0; i < g_pix.size(); ++i) {
        const Pixel& p = g_pix[i];
        g_fb.pixels[i] = rgb(p.r, p.g, p.b);
    }
    BITMAPINFO bmi{};
    bmi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    bmi.bmiHeader.biWidth = g_fb.width;
    bmi.bmiHeader.biHeight = -g_fb.height;
    bmi.bmiHeader.biPlanes = 1;
    bmi.bmiHeader.biBitCount = 32;
    bmi.bmiHeader.biCompression = BI_RGB;
    HDC dc = GetDC(window);
    StretchDIBits(
        dc, 0, 0, g_fb.width, g_fb.height, 0, 0, g_fb.width, g_fb.height,
        g_fb.pixels.data(), &bmi, DIB_RGB_COLORS, SRCCOPY);
    ReleaseDC(window, dc);
}

LRESULT CALLBACK wndproc(HWND w, UINT m, WPARAM wp, LPARAM) {
    if (m == WM_DESTROY || (m == WM_KEYDOWN && wp == VK_ESCAPE)) {
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProcW(w, m, wp, 0);
}

}  // namespace

int WINAPI wWinMain(HINSTANCE inst, HINSTANCE, PWSTR, int) {
    WNDCLASSW wc{};
    wc.lpfnWndProc = wndproc;
    wc.hInstance = inst;
    wc.lpszClassName = L"BlendSw";
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
    RegisterClassW(&wc);
    HWND hwnd = CreateWindowExW(
        0, wc.lpszClassName, L"alpha_blend_scanline CPU — Esc quit",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE, CW_USEDEFAULT, CW_USEDEFAULT,
        960, 540, nullptr, nullptr, inst, nullptr);
    if (!hwnd) {
        return 1;
    }
    g_fb.resize(960, 540);
    g_pix.resize(static_cast<std::size_t>(960) * 540);
    auto prev = std::chrono::steady_clock::now();
    MSG msg{};
    bool run = true;
    while (run) {
        while (PeekMessageW(&msg, nullptr, 0, 0, PM_REMOVE)) {
            if (msg.message == WM_QUIT) {
                run = false;
            }
            TranslateMessage(&msg);
            DispatchMessageW(&msg);
        }
        const auto now = std::chrono::steady_clock::now();
        const float dt = std::chrono::duration<float>(now - prev).count();
        prev = now;
        blendlab::update_sprite(g_a, dt, 0, 0, 960, 540);
        blendlab::update_sprite(g_b, dt, 0, 0, 960, 540);
        for (int y = 0; y < 540; ++y) {
            for (int x = 0; x < 960; ++x) {
                const bool c = ((x / 32) + (y / 32)) & 1;
                g_pix[static_cast<std::size_t>(y) * 960 + x] =
                    c ? Pixel{50, 50, 55, 255} : Pixel{30, 30, 35, 255};
            }
        }
        blit_sprite(g_a);
        blit_sprite(g_b);
        present(hwnd);
        Sleep(1);
    }
    return 0;
}
