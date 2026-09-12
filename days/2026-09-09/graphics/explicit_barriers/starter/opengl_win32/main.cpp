#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include <GL/gl.h>
#include "barriers.hpp"
// Starter stub: open solutions/opengl_win32 after core TODOs pass ctest.
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"Implement OpenGL visual backend (see solutions)", L"barriers_gl", MB_OK);
    return 0;
}
