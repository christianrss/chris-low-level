#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include "pso.hpp"
// After GFX-PSO-* core TODOs: wire OpenGL triangle demo (see solutions/)
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"Implement opengl_win32 PSO demo", L"pso_gl", MB_OK);
    return 0;
}
