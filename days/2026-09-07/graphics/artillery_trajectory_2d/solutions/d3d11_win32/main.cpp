#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif

#include <windows.h>
#include <d3d11.h>
#include <d3dcompiler.h>

#include <chrono>
#include <cmath>
#include <cstring>
#include <vector>

#include "artillery.hpp"

// PEDAGOGY-SOLUTION: GFX-ART-D3D-06

#pragma comment(lib, "d3dcompiler.lib")

using namespace art2d;

namespace {

constexpr int kWidth = 960;
constexpr int kHeight = 540;
constexpr float kGravity = 120.0f;
constexpr float kDt = 1.0f / 60.0f;

struct Vertex2d {
    float x;
    float y;
};

ID3D11Device* g_device = nullptr;
ID3D11DeviceContext* g_context = nullptr;
IDXGISwapChain* g_swap = nullptr;
ID3D11RenderTargetView* g_rtv = nullptr;
ID3D11VertexShader* g_vs = nullptr;
ID3D11PixelShader* g_ps = nullptr;
ID3D11InputLayout* g_layout = nullptr;
ID3D11Buffer* g_vb = nullptr;

Terrain g_terrain;
Projectile g_projectile{};
Trail g_trail{};
bool g_space_down = false;
std::vector<Vertex2d> g_vertices;

const char* kShader = R"(
struct VSIn { float2 pos : POSITION; };
struct VSOut { float4 pos : SV_POSITION; };
VSOut vs_main(VSIn input) {
    VSOut o;
    float2 ndc;
    ndc.x = (input.pos.x / 960.0) * 2.0 - 1.0;
    ndc.y = 1.0 - (input.pos.y / 540.0) * 2.0;
    o.pos = float4(ndc, 0.0, 1.0);
    return o;
}
float4 ps_main() : SV_TARGET { return float4(0.19, 0.55, 0.24, 1.0); }
)";

bool compile_shader(const char* source, const char* entry, const char* target, ID3DBlob** blob) {
    ID3DBlob* errors = nullptr;
    const HRESULT hr = D3DCompile(
        source, std::strlen(source), nullptr, nullptr, nullptr, entry, target,
        D3DCOMPILE_ENABLE_STRICTNESS, 0, blob, &errors);
    if (FAILED(hr)) {
        if (errors) {
            errors->Release();
        }
        return false;
    }
    return true;
}

void init_terrain(Terrain& terrain) {
    terrain.heights.clear();
    for (int i = 0; i < 100; ++i) {
        const float x = static_cast<float>(i);
        terrain.heights.push_back(80.0f + 35.0f * std::sin(x * 0.08f) + 20.0f * std::cos(x * 0.03f));
    }
}

void reset_shot() {
    g_trail = Trail{};
    const float start_x = 40.0f;
    fire(g_projectile, 52.0f, 220.0f);
    g_projectile.pos = {start_x, g_terrain.sample(start_x) + 8.0f};
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

void rebuild_vertices() {
    g_vertices.clear();
    for (std::size_t i = 0; i < g_terrain.heights.size(); ++i) {
        g_vertices.push_back({static_cast<float>(i) * 10.0f, g_terrain.heights[i]});
    }
    for (std::size_t i = 0; i < g_trail.count; ++i) {
        g_vertices.push_back({g_trail.points[i].pos.x, g_trail.points[i].pos.y});
    }
    if (g_projectile.alive) {
        const float r = 5.0f;
        for (int s = 0; s <= 12; ++s) {
            const float a = static_cast<float>(s) / 12.0f * 6.2831853f;
            g_vertices.push_back({
                g_projectile.pos.x + std::cos(a) * r,
                g_projectile.pos.y + std::sin(a) * r});
        }
    }
}

bool create_device(HWND window) {
    DXGI_SWAP_CHAIN_DESC scd{};
    scd.BufferCount = 2;
    scd.BufferDesc.Width = kWidth;
    scd.BufferDesc.Height = kHeight;
    scd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
    scd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
    scd.OutputWindow = window;
    scd.SampleDesc.Count = 1;
    scd.Windowed = TRUE;
    scd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;

    D3D_FEATURE_LEVEL level{};
    const HRESULT hr = D3D11CreateDeviceAndSwapChain(
        nullptr, D3D_DRIVER_TYPE_HARDWARE, nullptr, 0, nullptr, 0, D3D11_SDK_VERSION,
        &scd, &g_swap, &g_device, &level, &g_context);
    if (FAILED(hr)) {
        return false;
    }

    ID3D11Texture2D* back = nullptr;
    g_swap->GetBuffer(0, __uuidof(ID3D11Texture2D), reinterpret_cast<void**>(&back));
    g_device->CreateRenderTargetView(back, nullptr, &g_rtv);
    back->Release();

    ID3DBlob* vs_blob = nullptr;
    ID3DBlob* ps_blob = nullptr;
    if (!compile_shader(kShader, "vs_main", "vs_4_0", &vs_blob) ||
        !compile_shader(kShader, "ps_main", "ps_4_0", &ps_blob)) {
        return false;
    }
    g_device->CreateVertexShader(vs_blob->GetBufferPointer(), vs_blob->GetBufferSize(), nullptr, &g_vs);
    g_device->CreatePixelShader(ps_blob->GetBufferPointer(), ps_blob->GetBufferSize(), nullptr, &g_ps);

    const D3D11_INPUT_ELEMENT_DESC layout[] = {
        {"POSITION", 0, DXGI_FORMAT_R32G32_FLOAT, 0, 0, D3D11_INPUT_PER_VERTEX_DATA, 0}};
    g_device->CreateInputLayout(layout, 1, vs_blob->GetBufferPointer(), vs_blob->GetBufferSize(), &g_layout);
    vs_blob->Release();
    ps_blob->Release();

    D3D11_BUFFER_DESC bd{};
    bd.ByteWidth = sizeof(Vertex2d) * 4096;
    bd.Usage = D3D11_USAGE_DYNAMIC;
    bd.BindFlags = D3D11_BIND_VERTEX_BUFFER;
    bd.CPUAccessFlags = D3D11_CPU_ACCESS_WRITE;
    g_device->CreateBuffer(&bd, nullptr, &g_vb);
    return true;
}

void render_frame() {
    rebuild_vertices();
    const float clear[4] = {0.07f, 0.09f, 0.16f, 1.0f};
    g_context->OMSetRenderTargets(1, &g_rtv, nullptr);
    g_context->ClearRenderTargetView(g_rtv, clear);
    if (g_vertices.empty()) {
        g_swap->Present(1, 0);
        return;
    }

    D3D11_MAPPED_SUBRESOURCE mapped{};
    if (SUCCEEDED(g_context->Map(g_vb, 0, D3D11_MAP_WRITE_DISCARD, 0, &mapped))) {
        std::memcpy(mapped.pData, g_vertices.data(), g_vertices.size() * sizeof(Vertex2d));
        g_context->Unmap(g_vb, 0);
    }

    const UINT stride = sizeof(Vertex2d);
    const UINT offset = 0;
    g_context->IASetInputLayout(g_layout);
    g_context->IASetPrimitiveTopology(D3D11_PRIMITIVE_TOPOLOGY_LINESTRIP);
    g_context->IASetVertexBuffers(0, 1, &g_vb, &stride, &offset);
    g_context->VSSetShader(g_vs, nullptr, 0);
    g_context->PSSetShader(g_ps, nullptr, 0);
    g_context->Draw(static_cast<UINT>(g_vertices.size()), 0);
    g_swap->Present(1, 0);
}

LRESULT CALLBACK window_proc(HWND window, UINT message, WPARAM wparam, LPARAM lparam) {
    switch (message) {
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
    wc.lpszClassName = L"ArtilleryD3d";
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
    RegisterClassW(&wc);

    HWND window = CreateWindowExW(
        0, wc.lpszClassName, L"Artillery D3D11 — Space fire, Esc quit",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE, CW_USEDEFAULT, CW_USEDEFAULT,
        kWidth, kHeight, nullptr, nullptr, instance, nullptr);
    if (!window) {
        return 1;
    }
    if (!create_device(window)) {
        MessageBoxW(window, L"D3D11 init failed.", L"artillery_d3d", MB_ICONERROR);
        return 2;
    }

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
        prev = std::chrono::steady_clock::now();
        simulate();
        render_frame();
        Sleep(1);
    }
    if (g_vb) g_vb->Release();
    if (g_layout) g_layout->Release();
    if (g_ps) g_ps->Release();
    if (g_vs) g_vs->Release();
    if (g_rtv) g_rtv->Release();
    if (g_swap) g_swap->Release();
    if (g_context) g_context->Release();
    if (g_device) g_device->Release();
    return 0;
}
