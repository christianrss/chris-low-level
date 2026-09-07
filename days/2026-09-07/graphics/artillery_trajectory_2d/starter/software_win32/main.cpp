#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include "artillery.hpp"
// TODO [GFX-ART-SW-04]: raster 2D terrain + projectile trail via DIB
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"Implement GFX-ART-SW-04", L"artillery_sw", MB_OK);
    return 0;
}
