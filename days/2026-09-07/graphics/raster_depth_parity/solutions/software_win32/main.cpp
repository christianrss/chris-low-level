#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif

#include <windows.h>

#include <cstdint>
#include <vector>

#include "depth_buffer.hpp"
#include "parity.hpp"

// PEDAGOGY-SOLUTION: GFX-DEPTH-SW-04

namespace {

constexpr int kWidth = 320;
constexpr int kHeight = 240;

std::vector<depth_lab::Color> g_fb;
depth_lab::DepthBuffer g_db;

void present(HWND window) {
    std::vector<std::uint32_t> pixels(static_cast<std::size_t>(kWidth) * kHeight);
    for (int y = 0; y < kHeight; ++y) {
        for (int x = 0; x < kWidth; ++x) {
            const auto& c = g_fb[static_cast<std::size_t>(y) * kWidth + x];
            pixels[static_cast<std::size_t>(y) * kWidth + x] =
                (static_cast<std::uint32_t>(c.r) << 16) |
                (static_cast<std::uint32_t>(c.g) << 8) |
                static_cast<std::uint32_t>(c.b);
        }
    }

    HDC dc = GetDC(window);
    BITMAPINFO bmi{};
    bmi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    bmi.bmiHeader.biWidth = kWidth;
    bmi.bmiHeader.biHeight = -kHeight;
    bmi.bmiHeader.biPlanes = 1;
    bmi.bmiHeader.biBitCount = 32;
    bmi.bmiHeader.biCompression = BI_RGB;
    StretchDIBits(dc, 0, 0, kWidth, kHeight, 0, 0, kWidth, kHeight, pixels.data(), &bmi, DIB_RGB_COLORS, SRCCOPY);
    ReleaseDC(window, dc);
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
    wc.lpszClassName = L"DepthSw";
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
    RegisterClassW(&wc);

    HWND window = CreateWindowExW(
        0, wc.lpszClassName, L"Depth CPU — blue square in front of red (Esc quit)",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE, CW_USEDEFAULT, CW_USEDEFAULT,
        kWidth + 16, kHeight + 39, nullptr, nullptr, instance, nullptr);
    if (!window) {
        return 1;
    }

    g_fb.assign(static_cast<std::size_t>(kWidth) * kHeight, depth_lab::Color{18, 18, 28});
    g_db.resize(kWidth, kHeight);
    parity_scene_cpu(g_fb, g_db);

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
        present(window);
        Sleep(16);
    }
    return 0;
}
