#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#include <windows.h>
// TODO [GFX-ART-GL-05]: same scene with OpenGL 2D ortho
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"Implement GFX-ART-GL-05", L"artillery_gl", MB_OK);
    return 0;
}
