// PEDAGOGY-TEST: GFX-PORTAL-06: OpenGL demo (manual GPU — Caso 6)
// TODO [GFX-PORTAL-06]: Win32 loop + portal_gl_render_frame
#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif

#include "render_gl.hpp"
#include <windows.h>

int WINAPI WinMain(HINSTANCE, HINSTANCE, LPSTR, int) {
    MessageBoxA(
        nullptr,
        "Implement GFX-PORTAL-06 in starter/src/render_gl.cpp and main_opengl.cpp.\n"
        "Compare with solutions/ and run portal_demo.exe.",
        "portal_demo starter",
        MB_OK);
    return 0;
}
