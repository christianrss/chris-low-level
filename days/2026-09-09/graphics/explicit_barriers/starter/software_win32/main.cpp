#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include "barriers.hpp"
// Starter stub: open solutions/software_win32 after core TODOs pass ctest.
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"Implement CPU visual backend (see solutions)", L"barriers_sw", MB_OK);
    return 0;
}
