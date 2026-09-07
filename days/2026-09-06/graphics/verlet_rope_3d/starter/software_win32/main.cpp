#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
// PEDAGOGY-TEST: GFX-PORTAL-SW-07
// TODO [GFX-PORTAL-SW-07]: wireframe CPU — mesma cena que portal_demo GL (sem stencil)
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"Implement wireframe software renderer", L"portal_sw", MB_OK);
    return 0;
}
