#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#include <windows.h>
// TODO [GFX-DEPTH-GL-02]: GL_DEPTH_TEST + glClear(GL_DEPTH_BUFFER_BIT)
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"Implement GFX-DEPTH-GL-02", L"depth_gl", MB_OK);
    return 0;
}
