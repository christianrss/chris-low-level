// PEDAGOGY-SOLUTION: GFX-D3D11-CTX-01
// PEDAGOGY-SOLUTION: GFX-D3D11-DRAW-02

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif

#include <windows.h>
#include <d3d11.h>
#include <d3dcompiler.h>
#include <dxgi.h>

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstring>
#include <vector>

#include "../common/engine.hpp"

#pragma comment(lib, "d3dcompiler.lib")

using namespace lab3d;

namespace {

struct Vertex {
    float px, py, pz;
    float nx, ny, nz;
};

constexpr Vertex kCube[] = {
    {-0.5f, -0.5f, -0.5f, 0, 0, -1}, {0.5f, 0.5f, -0.5f, 0, 0, -1}, {0.5f, -0.5f, -0.5f, 0, 0, -1},
    {-0.5f, -0.5f, -0.5f, 0, 0, -1}, {-0.5f, 0.5f, -0.5f, 0, 0, -1}, {0.5f, 0.5f, -0.5f, 0, 0, -1},
    {-0.5f, -0.5f, 0.5f, 0, 0, 1}, {0.5f, -0.5f, 0.5f, 0, 0, 1}, {0.5f, 0.5f, 0.5f, 0, 0, 1},
    {-0.5f, -0.5f, 0.5f, 0, 0, 1}, {0.5f, 0.5f, 0.5f, 0, 0, 1}, {-0.5f, 0.5f, 0.5f, 0, 0, 1},
    {-0.5f, -0.5f, -0.5f, 0, -1, 0}, {0.5f, -0.5f, -0.5f, 0, -1, 0}, {0.5f, -0.5f, 0.5f, 0, -1, 0},
    {-0.5f, -0.5f, -0.5f, 0, -1, 0}, {0.5f, -0.5f, 0.5f, 0, -1, 0}, {-0.5f, -0.5f, 0.5f, 0, -1, 0},
    {-0.5f, 0.5f, -0.5f, 0, 1, 0}, {0.5f, 0.5f, 0.5f, 0, 1, 0}, {0.5f, 0.5f, -0.5f, 0, 1, 0},
    {-0.5f, 0.5f, -0.5f, 0, 1, 0}, {-0.5f, 0.5f, 0.5f, 0, 1, 0}, {0.5f, 0.5f, 0.5f, 0, 1, 0},
    {0.5f, -0.5f, -0.5f, 1, 0, 0}, {0.5f, 0.5f, -0.5f, 1, 0, 0}, {0.5f, 0.5f, 0.5f, 1, 0, 0},
    {0.5f, -0.5f, -0.5f, 1, 0, 0}, {0.5f, 0.5f, 0.5f, 1, 0, 0}, {0.5f, -0.5f, 0.5f, 1, 0, 0},
    {-0.5f, -0.5f, -0.5f, -1, 0, 0}, {-0.5f, 0.5f, 0.5f, -1, 0, 0}, {-0.5f, 0.5f, -0.5f, -1, 0, 0},
    {-0.5f, -0.5f, -0.5f, -1, 0, 0}, {-0.5f, -0.5f, 0.5f, -1, 0, 0}, {-0.5f, 0.5f, 0.5f, -1, 0, 0},
};

struct ConstantBuffer {
    float mvp[16];
    float model[16];
    float color[4];
};

ID3D11Device* g_device = nullptr;
ID3D11DeviceContext* g_context = nullptr;
IDXGISwapChain* g_swap = nullptr;
ID3D11RenderTargetView* g_rtv = nullptr;
ID3D11DepthStencilView* g_dsv = nullptr;
ID3D11VertexShader* g_vs = nullptr;
ID3D11PixelShader* g_ps = nullptr;
ID3D11InputLayout* g_layout = nullptr;
ID3D11Buffer* g_vb = nullptr;
ID3D11Buffer* g_cb = nullptr;

SceneState g_scene;
CameraState g_camera;
POINT g_last_mouse{};
bool g_have_last_mouse = false;
int g_width = 1100;
int g_height = 720;

const char* kShader = R"(
cbuffer Constants : register(b0) {
    float4x4 mvp;
    float4x4 model;
    float4 color;
};
struct VSIn { float3 pos : POSITION; float3 normal : NORMAL; };
struct VSOut { float4 pos : SV_POSITION; float3 world_normal : NORMAL; };
VSOut vs_main(VSIn input) {
    VSOut o;
    o.pos = mul(mvp, float4(input.pos, 1.0));
    o.world_normal = mul(model, float4(input.normal, 0.0)).xyz;
    return o;
}
float4 ps_main(VSOut input) : SV_TARGET {
    float3 n = normalize(input.world_normal);
    float light = saturate(dot(n, normalize(float3(0.3, 0.8, 0.4))));
    return float4(color.rgb * (0.25 + 0.75 * light), 1.0);
}
)";

bool compile_blob(const char* entry, const char* target, ID3DBlob** out) {
    ID3DBlob* errors = nullptr;
    const HRESULT hr = D3DCompile(
        kShader, std::strlen(kShader), nullptr, nullptr, nullptr, entry, target,
        D3DCOMPILE_ENABLE_STRICTNESS, 0, out, &errors);
    if (errors) {
        errors->Release();
    }
    return SUCCEEDED(hr);
}

bool create_render_targets(HWND window) {
    DXGI_SWAP_CHAIN_DESC sd{};
    sd.BufferCount = 2;
    sd.BufferDesc.Width = g_width;
    sd.BufferDesc.Height = g_height;
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
    sd.OutputWindow = window;
    sd.SampleDesc.Count = 1;
    sd.Windowed = TRUE;
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;

    D3D_FEATURE_LEVEL level{};
    if (FAILED(D3D11CreateDeviceAndSwapChain(
            nullptr, D3D_DRIVER_TYPE_HARDWARE, nullptr, 0, nullptr, 0, D3D11_SDK_VERSION,
            &sd, &g_swap, &g_device, &level, &g_context))) {
        return false;
    }

    ID3D11Texture2D* back = nullptr;
    g_swap->GetBuffer(0, __uuidof(ID3D11Texture2D), reinterpret_cast<void**>(&back));
    g_device->CreateRenderTargetView(back, nullptr, &g_rtv);
    back->Release();

    D3D11_TEXTURE2D_DESC depth_desc{};
    depth_desc.Width = g_width;
    depth_desc.Height = g_height;
    depth_desc.MipLevels = 1;
    depth_desc.ArraySize = 1;
    depth_desc.Format = DXGI_FORMAT_D24_UNORM_S8_UINT;
    depth_desc.SampleDesc.Count = 1;
    depth_desc.BindFlags = D3D11_BIND_DEPTH_STENCIL;
    ID3D11Texture2D* depth_tex = nullptr;
    g_device->CreateTexture2D(&depth_desc, nullptr, &depth_tex);
    g_device->CreateDepthStencilView(depth_tex, nullptr, &g_dsv);
    depth_tex->Release();

    ID3DBlob* vs_blob = nullptr;
    ID3DBlob* ps_blob = nullptr;
    if (!compile_blob("vs_main", "vs_4_0", &vs_blob) || !compile_blob("ps_main", "ps_4_0", &ps_blob)) {
        return false;
    }
    g_device->CreateVertexShader(vs_blob->GetBufferPointer(), vs_blob->GetBufferSize(), nullptr, &g_vs);
    g_device->CreatePixelShader(ps_blob->GetBufferPointer(), ps_blob->GetBufferSize(), nullptr, &g_ps);

    const D3D11_INPUT_ELEMENT_DESC layout[] = {
        {"POSITION", 0, DXGI_FORMAT_R32G32B32_FLOAT, 0, 0, D3D11_INPUT_PER_VERTEX_DATA, 0},
        {"NORMAL", 0, DXGI_FORMAT_R32G32B32_FLOAT, 0, 12, D3D11_INPUT_PER_VERTEX_DATA, 0}};
    g_device->CreateInputLayout(layout, 2, vs_blob->GetBufferPointer(), vs_blob->GetBufferSize(), &g_layout);
    vs_blob->Release();
    ps_blob->Release();

    D3D11_BUFFER_DESC vbd{};
    vbd.ByteWidth = sizeof(kCube);
    vbd.Usage = D3D11_USAGE_IMMUTABLE;
    vbd.BindFlags = D3D11_BIND_VERTEX_BUFFER;
    D3D11_SUBRESOURCE_DATA vinit{};
    vinit.pSysMem = kCube;
    g_device->CreateBuffer(&vbd, &vinit, &g_vb);

    D3D11_BUFFER_DESC cbd{};
    cbd.ByteWidth = sizeof(ConstantBuffer);
    cbd.Usage = D3D11_USAGE_DYNAMIC;
    cbd.BindFlags = D3D11_BIND_CONSTANT_BUFFER;
    cbd.CPUAccessFlags = D3D11_CPU_ACCESS_WRITE;
    g_device->CreateBuffer(&cbd, nullptr, &g_cb);
    return true;
}

void resize(int w, int h) {
    g_width = std::max(1, w);
    g_height = std::max(1, h);
    if (!g_swap) {
        return;
    }
    if (g_dsv) {
        g_dsv->Release();
        g_dsv = nullptr;
    }
    if (g_rtv) {
        g_rtv->Release();
        g_rtv = nullptr;
    }
    g_context->OMSetRenderTargets(0, nullptr, nullptr);
    g_swap->ResizeBuffers(0, g_width, g_height, DXGI_FORMAT_UNKNOWN, 0);
    ID3D11Texture2D* back = nullptr;
    g_swap->GetBuffer(0, __uuidof(ID3D11Texture2D), reinterpret_cast<void**>(&back));
    g_device->CreateRenderTargetView(back, nullptr, &g_rtv);
    back->Release();

    D3D11_TEXTURE2D_DESC depth_desc{};
    depth_desc.Width = g_width;
    depth_desc.Height = g_height;
    depth_desc.MipLevels = 1;
    depth_desc.ArraySize = 1;
    depth_desc.Format = DXGI_FORMAT_D24_UNORM_S8_UINT;
    depth_desc.SampleDesc.Count = 1;
    depth_desc.BindFlags = D3D11_BIND_DEPTH_STENCIL;
    ID3D11Texture2D* depth_tex = nullptr;
    g_device->CreateTexture2D(&depth_desc, nullptr, &depth_tex);
    g_device->CreateDepthStencilView(depth_tex, nullptr, &g_dsv);
    depth_tex->Release();
}

void update_camera_keyboard(float dt) {
    constexpr float speed = 3.0f;
    const Vec3 forward = camera_forward(g_camera);
    const Vec3 right = camera_right(g_camera);
    if ((GetAsyncKeyState('W') & 0x8000) != 0) {
        g_camera.position = g_camera.position + forward * (speed * dt);
    }
    if ((GetAsyncKeyState('S') & 0x8000) != 0) {
        g_camera.position = g_camera.position - forward * (speed * dt);
    }
    if ((GetAsyncKeyState('D') & 0x8000) != 0) {
        g_camera.position = g_camera.position + right * (speed * dt);
    }
    if ((GetAsyncKeyState('A') & 0x8000) != 0) {
        g_camera.position = g_camera.position - right * (speed * dt);
    }
}

void render_scene() {
    const float aspect = static_cast<float>(g_width) / static_cast<float>(std::max(1, g_height));
    const Mat4 view_projection = projection_matrix(aspect) * view_matrix(g_camera);

    const float clear[4] = {0.08f, 0.1f, 0.14f, 1.0f};
    g_context->OMSetRenderTargets(1, &g_rtv, g_dsv);
    g_context->ClearRenderTargetView(g_rtv, clear);
    g_context->ClearDepthStencilView(g_dsv, D3D11_CLEAR_DEPTH | D3D11_CLEAR_STENCIL, 1.0f, 0);

    const UINT stride = sizeof(Vertex);
    const UINT offset = 0;
    g_context->IASetInputLayout(g_layout);
    g_context->IASetVertexBuffers(0, 1, &g_vb, &stride, &offset);
    g_context->IASetPrimitiveTopology(D3D11_PRIMITIVE_TOPOLOGY_TRIANGLELIST);
    g_context->VSSetShader(g_vs, nullptr, 0);
    g_context->PSSetShader(g_ps, nullptr, 0);
    g_context->VSSetConstantBuffers(0, 1, &g_cb);
    g_context->PSSetConstantBuffers(0, 1, &g_cb);

    for (const DrawItem& item : build_draw_list(g_scene)) {
        ConstantBuffer cb{};
        const Mat4 mvp = view_projection * item.model;
        std::memcpy(cb.mvp, mvp.m.data(), sizeof(cb.mvp));
        std::memcpy(cb.model, item.model.m.data(), sizeof(cb.model));
        cb.color[0] = item.color.x;
        cb.color[1] = item.color.y;
        cb.color[2] = item.color.z;
        cb.color[3] = 1.0f;

        D3D11_MAPPED_SUBRESOURCE mapped{};
        if (SUCCEEDED(g_context->Map(g_cb, 0, D3D11_MAP_WRITE_DISCARD, 0, &mapped))) {
            std::memcpy(mapped.pData, &cb, sizeof(cb));
            g_context->Unmap(g_cb, 0);
        }
        g_context->Draw(36, 0);
    }
    g_swap->Present(1, 0);
}

LRESULT CALLBACK window_proc(HWND window, UINT message, WPARAM wparam, LPARAM lparam) {
    switch (message) {
    case WM_SIZE:
        resize(LOWORD(lparam), HIWORD(lparam));
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
    case WM_MOUSEMOVE: {
        const POINT cur{static_cast<short>(LOWORD(lparam)), static_cast<short>(HIWORD(lparam))};
        if (g_have_last_mouse) {
            constexpr float sens = 0.004f;
            g_camera.yaw += static_cast<float>(cur.x - g_last_mouse.x) * sens;
            g_camera.pitch = std::clamp(
                g_camera.pitch - static_cast<float>(cur.y - g_last_mouse.y) * sens, -1.45f, 1.45f);
        }
        g_last_mouse = cur;
        g_have_last_mouse = true;
        return 0;
    }
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    default:
        break;
    }
    return DefWindowProcA(window, message, wparam, lparam);
}

}  // namespace

int WINAPI WinMain(HINSTANCE instance, HINSTANCE, LPSTR, int) {
    WNDCLASSA wc{};
    wc.lpfnWndProc = window_proc;
    wc.hInstance = instance;
    wc.lpszClassName = "LowLevelD3D113D";
    wc.hCursor = LoadCursorA(nullptr, IDC_ARROW);
    RegisterClassA(&wc);

    HWND window = CreateWindowExA(
        0, wc.lpszClassName, "D3D11 dual backend — WASD move, mouse look, R reset, P pause",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE, CW_USEDEFAULT, CW_USEDEFAULT, g_width, g_height,
        nullptr, nullptr, instance, nullptr);
    if (!window) {
        return 1;
    }
    if (!create_render_targets(window)) {
        MessageBoxA(window, "D3D11 init failed.", "d3d11_renderer", MB_ICONERROR);
        return 2;
    }

    auto prev = std::chrono::steady_clock::now();
    MSG msg{};
    bool running = true;
    while (running) {
        while (PeekMessageA(&msg, nullptr, 0, 0, PM_REMOVE)) {
            if (msg.message == WM_QUIT) {
                running = false;
            }
            TranslateMessage(&msg);
            DispatchMessageA(&msg);
        }
        const auto now = std::chrono::steady_clock::now();
        const float dt = std::chrono::duration<float>(now - prev).count();
        prev = now;
        update_camera_keyboard(dt);
        if (!g_scene.paused) {
            physics_step(g_scene, dt);
        }
        render_scene();
        Sleep(1);
    }

    if (g_cb) g_cb->Release();
    if (g_vb) g_vb->Release();
    if (g_layout) g_layout->Release();
    if (g_ps) g_ps->Release();
    if (g_vs) g_vs->Release();
    if (g_dsv) g_dsv->Release();
    if (g_rtv) g_rtv->Release();
    if (g_swap) g_swap->Release();
    if (g_context) g_context->Release();
    if (g_device) g_device->Release();
    return 0;
}
