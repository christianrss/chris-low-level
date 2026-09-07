#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include <d3d11.h>
#include "../common/engine.hpp"
// Extension optional — não bloqueia gate CPU+GL original.
// PEDAGOGY-TEST: GFX-D3D11-CTX-01
// PEDAGOGY-TEST: GFX-D3D11-DRAW-02
// TODO [GFX-D3D11-CTX-01]: device, swapchain, render target view
// TODO [GFX-D3D11-DRAW-02]: upload mesh + HLSL Lambert draw call
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"Implement D3D11 extension (see RESOLUCAO_APENDICE)", L"d3d11_renderer", MB_OK);
    return 0;
}
