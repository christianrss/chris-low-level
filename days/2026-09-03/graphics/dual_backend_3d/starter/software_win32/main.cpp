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

#include "../common/engine.hpp"

using namespace lab3d;

namespace {

struct Framebuffer {
    int width = 0;
    int height = 0;
    std::vector<std::uint32_t> pixels;
    std::vector<float> depth;

    void resize(int new_width, int new_height) {
        // windows.h historically defines min/max macros. NOMINMAX above keeps
        // std::min/std::max usable with MSVC.
        width = std::max(1, new_width);
        height = std::max(1, new_height);

        pixels.assign(static_cast<std::size_t>(width) * height, 0u);
        depth.assign(static_cast<std::size_t>(width) * height, 1.0f);
    }

    void clear(std::uint32_t color) {
        std::fill(pixels.begin(), pixels.end(), color);
        std::fill(depth.begin(), depth.end(), 1.0f);
    }
};

struct ScreenVertex {
    float x = 0.0f;
    float y = 0.0f;
    float z = 0.0f;
    float inverse_w = 0.0f;
    Vec3 world{};
};

constexpr Vec3 kCubeVertices[8] = {
    {-1.0f, -1.0f, -1.0f},
    { 1.0f, -1.0f, -1.0f},
    { 1.0f,  1.0f, -1.0f},
    {-1.0f,  1.0f, -1.0f},
    {-1.0f, -1.0f,  1.0f},
    { 1.0f, -1.0f,  1.0f},
    { 1.0f,  1.0f,  1.0f},
    {-1.0f,  1.0f,  1.0f},
};

constexpr int kCubeIndices[36] = {
    0, 2, 1, 0, 3, 2,
    4, 5, 6, 4, 6, 7,
    0, 1, 5, 0, 5, 4,
    3, 7, 6, 3, 6, 2,
    1, 2, 6, 1, 6, 5,
    0, 4, 7, 0, 7, 3,
};

Framebuffer g_framebuffer;
SceneState g_scene;
CameraState g_camera;
POINT g_last_mouse{};
bool g_have_last_mouse = false;

std::uint32_t rgb(Vec3 color, float light) {
    const auto to_channel = [light](float value) {
        const float lit = std::clamp(value * light, 0.0f, 1.0f);
        return static_cast<std::uint32_t>(lit * 255.0f + 0.5f);
    };

    const std::uint32_t red = to_channel(color.x);
    const std::uint32_t green = to_channel(color.y);
    const std::uint32_t blue = to_channel(color.z);

    // BI_RGB with a 32-bit top-down DIB expects B, G, R, X bytes in memory.
    // On little-endian x86/x64, 0x00RRGGBB produces exactly that byte order.
    return (red << 16u) | (green << 8u) | blue;
}

bool project_vertex(
    const Vec3& position,
    const Mat4& model,
    const Mat4& view_projection,
    int width,
    int height,
    ScreenVertex& output) {

    const Vec4 world = model * Vec4{position.x, position.y, position.z, 1.0f};
    const Vec4 clip = view_projection * world;

    // A complete renderer would clip triangles against the near plane. For
    // this first exercise we reject vertices behind the camera instead.
    if (clip.w <= 0.001f) {
        return false;
    }

    const float inverse_w = 1.0f / clip.w;
    const float ndc_x = clip.x * inverse_w;
    const float ndc_y = clip.y * inverse_w;
    const float ndc_z = clip.z * inverse_w;

    output.x = (ndc_x * 0.5f + 0.5f) * static_cast<float>(width - 1);
    output.y = (1.0f - (ndc_y * 0.5f + 0.5f)) * static_cast<float>(height - 1);
    output.z = ndc_z * 0.5f + 0.5f;
    output.inverse_w = inverse_w;
    output.world = {world.x, world.y, world.z};

    return true;
}

float edge(float ax, float ay, float bx, float by, float px, float py) {
    return (px - ax) * (by - ay) - (py - ay) * (bx - ax);
}

void rasterize_triangle(
    Framebuffer& framebuffer,
    const ScreenVertex& a,
    const ScreenVertex& b,
    const ScreenVertex& c,
    Vec3 base_color) {
    
    // Área orientada e degeneração
    const float area = edge(a.x, a.y, b.x, b.y, c.x, c.y);
    if (std::fabs(area) < 1.0e-6f) {
        return;
    }

    // Bouding box
    const float min_x_f = std::min({a.x, b.x, c.x});
    const float max_x_f = std::max({a.x, b.x, c.x});
    const float min_y_f = std::min({a.y, b.y, c.y});
    const float max_y_f = std::max({a.y, b.y, c.y});

    const int min_x = std::max(0, static_cast<int>(std::floor(min_x_f)));
    const int max_x = std::min(
        framebuffer.width - 1,
        static_cast<int>(std::ceil(max_x_f)));
    const int min_y = std::max(0, static_cast<int>(std::floor(min_y_f)));
    const int max_y = std::min(
        framebuffer.height - 1,
        static_cast<int>(std::ceil(max_y_f)));

    // Normal e Lambert por face
    const Vec3 normal = normalize(cross(b.world - a.world, c.world - a.world));
    const Vec3 light_direction = normalize(Vec3{-0.4f, 0.8f, 0.6f});
    const float diffuse = std::max(0.0f, dot(normal, light_direction));
    const float light = 0.20f + 0.80f * diffuse;
    const std::uint32_t packed_color = rgb(base_color, light);

    // Varredura de pixels
    for (int y = min_y; y <= max_y; ++y) {
        for (int x = min_x; x <= max_x; ++x) {
            const float sample_x = static_cast<float>(x) + 0.5f;
            const float sample_y = static_cast<float>(y) + 0.5f;
            // Barycentrics
            const float w0 = edge(b.x, b.y, c.x, c.y, sample_x, sample_y) / area;
            const float w1 = edge(c.x, c.y, a.x, a.y, sample_x, sample_y) / area;
            const float w2 = 1.0f - w0 - w1;

            if (w0 < 0.0f || w1 < 0.0f || w2 < 0.0f) {
                continue;
            }

            // Profundidade e depth test
            const float depth = w0 * a.z + w1 * b.z + w2 * c.z;
            if (depth < 0.0f || depth > 1.0f) {
                continue;
            }

            const std::size_t index =
                static_cast<std::size_t>(y) * framebuffer.width + x;

            if (depth < framebuffer.depth[index]) {
                framebuffer.depth[index] = depth;
                framebuffer.pixels[index] = packed_color;
            }
        }
    }
}

void draw_cube(Framebuffer& framebuffer, const DrawItem& item, const Mat4& view_projection) {
    ScreenVertex vertices[8]{};
    bool visible[8]{};

    for (int i = 0; i < 8; ++i) {
        visible[i] = project_vertex(
            kCubeVertices[i] * 0.5f,
            item.model,
            view_projection,
            framebuffer.width,
            framebuffer.height,
            vertices[i]);
    }

    for (int i = 0; i < 36; i += 3) {
        const int i0 = kCubeIndices[i + 0];
        const int i1 = kCubeIndices[i + 1];
        const int i2 = kCubeIndices[i + 2];

        if (visible[i0] && visible[i1] && visible[i2]) {
            // TODO [GFX-CULL-02]: compute signed area and skip back-facing triangles.
            rasterize_triangle(
                framebuffer,
                vertices[i0],
                vertices[i1],
                vertices[i2],
                item.color);
        }
    }
}

void update_camera_keyboard(float frame_dt) {
    // TODO [GFX-CAMERA-04]: W/S move along forward; A/D along right.
    (void)frame_dt;
}

void present(HWND window) {
    if (g_framebuffer.width <= 0 || g_framebuffer.height <= 0) {
        return;
    }

    HDC device_context = GetDC(window);
    if (device_context == nullptr) {
        return;
    }

    BITMAPINFO bitmap_info{};
    bitmap_info.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    bitmap_info.bmiHeader.biWidth = g_framebuffer.width;
    bitmap_info.bmiHeader.biHeight = -g_framebuffer.height; // Negative = top-down DIB.
    bitmap_info.bmiHeader.biPlanes = 1;
    bitmap_info.bmiHeader.biBitCount = 32;
    bitmap_info.bmiHeader.biCompression = BI_RGB;

    StretchDIBits(
        device_context,
        0,
        0,
        g_framebuffer.width,
        g_framebuffer.height,
        0,
        0,
        g_framebuffer.width,
        g_framebuffer.height,
        g_framebuffer.pixels.data(),
        &bitmap_info,
        DIB_RGB_COLORS,
        SRCCOPY);

    ReleaseDC(window, device_context);
}

LRESULT CALLBACK window_proc(HWND window, UINT message, WPARAM wparam, LPARAM lparam) {
    switch (message) {
        case WM_SIZE:
            g_framebuffer.resize(
                static_cast<int>(LOWORD(lparam)),
                static_cast<int>(HIWORD(lparam)));
            return 0;

        case WM_KEYDOWN:
            if (wparam == VK_ESCAPE) {
                DestroyWindow(window);
                return 0;
            }

            if (wparam == 'R') {
                reset_scene(g_scene);
                g_camera = CameraState{};
                g_have_last_mouse = false;
                return 0;
            }

            if (wparam == 'P') {
                g_scene.paused = !g_scene.paused;
                return 0;
            }
            break;

        case WM_MOUSEMOVE:
            // TODO [GFX-CAMERA-05]: convert mouse delta to yaw/pitch and clamp pitch.
            return 0;

        case WM_DESTROY:
            PostQuitMessage(0);
            return 0;

        default:
            break;
    }

    return DefWindowProcA(window, message, wparam, lparam);
}

} // namespace

int WINAPI WinMain(HINSTANCE instance, HINSTANCE, LPSTR, int) {
    WNDCLASSA window_class{};
    window_class.lpfnWndProc = window_proc;
    window_class.hInstance = instance;
    window_class.lpszClassName = "LowLevelSoftware3D";
    window_class.hCursor = LoadCursorA(nullptr, IDC_ARROW);

    if (RegisterClassA(&window_class) == 0) {
        MessageBoxA(nullptr, "RegisterClassA failed.", "Error", MB_ICONERROR);
        return 1;
    }

    HWND window = CreateWindowExA(
        0,
        window_class.lpszClassName,
        "Low-Level 3D - Software CPU Rasterizer",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE,
        CW_USEDEFAULT,
        CW_USEDEFAULT,
        1100,
        720,
        nullptr,
        nullptr,
        instance,
        nullptr);

    if (window == nullptr) {
        MessageBoxA(nullptr, "CreateWindowExA failed.", "Error", MB_ICONERROR);
        return 2;
    }

    g_framebuffer.resize(1100, 720);
    reset_scene(g_scene);
    g_camera = CameraState{};

    auto previous_time = std::chrono::steady_clock::now();
    double accumulator = 0.0;
    constexpr double kFixedTimeStep = 1.0 / 120.0;

    MSG message{};
    bool running = true;

    while (running) {
        while (PeekMessageA(&message, nullptr, 0, 0, PM_REMOVE)) {
            if (message.message == WM_QUIT) {
                running = false;
                break;
            }

            TranslateMessage(&message);
            DispatchMessageA(&message);
        }

        const auto current_time = std::chrono::steady_clock::now();
        double delta_time =
            std::chrono::duration<double>(current_time - previous_time).count();
        previous_time = current_time;

        // Prevent a debugger pause/window drag from producing a giant physics step.
        delta_time = std::min(delta_time, 0.05);
        update_camera_keyboard(static_cast<float>(delta_time));
        accumulator += delta_time;

        while (accumulator >= kFixedTimeStep) {
            physics_step(g_scene, static_cast<float>(kFixedTimeStep));
            accumulator -= kFixedTimeStep;
        }

        g_framebuffer.clear(0x00101820u);

        const float aspect =
            static_cast<float>(g_framebuffer.width) /
            static_cast<float>(std::max(1, g_framebuffer.height));
        const Mat4 view_projection = projection_matrix(aspect) * view_matrix(g_camera);

        for (const DrawItem& item : build_draw_list(g_scene)) {
            draw_cube(g_framebuffer, item, view_projection);
        }

        present(window);
        Sleep(1);
    }

    return 0;
}
