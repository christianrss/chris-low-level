#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include "blend.hpp"
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"Implement software_win32 alpha blend after core TODOs", L"blend_sw", MB_OK);
    return 0;
}
