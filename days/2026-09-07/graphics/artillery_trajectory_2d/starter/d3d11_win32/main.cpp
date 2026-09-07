#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#include <windows.h>
// TODO [GFX-ART-D3D-06]: DXGI swapchain + clear + line strip
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"Implement GFX-ART-D3D-06", L"artillery_d3d", MB_OK);
    return 0;
}
