#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include <GL/gl.h>
#include <chrono>
#include "blend.hpp"

HDC g_dc = nullptr;
HGLRC g_gl = nullptr;
bool init_gl(HWND hwnd) {
    g_dc = GetDC(hwnd);
    PIXELFORMATDESCRIPTOR pfd{};
    pfd.nSize = sizeof(pfd);
    pfd.nVersion = 1;
    pfd.dwFlags = PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL | PFD_DOUBLEBUFFER;
    pfd.iPixelType = PFD_TYPE_RGBA;
    pfd.cColorBits = 32;
    int pf = ChoosePixelFormat(g_dc, &pfd);
    SetPixelFormat(g_dc, pf, &pfd);
    g_gl = wglCreateContext(g_dc);
    return wglMakeCurrent(g_dc, g_gl) == TRUE;
}
void shutdown_gl(HWND hwnd) {
    wglMakeCurrent(nullptr, nullptr);
    if (g_gl) wglDeleteContext(g_gl);
    if (g_dc) ReleaseDC(hwnd, g_dc);
}

using blendlab::Sprite;
Sprite g_a{80,80, 140,90, 90,70, {255,40,40,140}};
Sprite g_b{400,200, -110,120, 110,80, {40,80,255,160}};
LRESULT CALLBACK wndproc(HWND w, UINT m, WPARAM wp, LPARAM lp) {
    if (m==WM_DESTROY || (m==WM_KEYDOWN && wp==VK_ESCAPE)) { PostQuitMessage(0); return 0; }
    return DefWindowProcW(w,m,wp,lp);
}
void draw_sprite(const Sprite& s) {
    float a=s.color.a/255.f;
    glColor4f(s.color.r/255.f, s.color.g/255.f, s.color.b/255.f, a);
    glBegin(GL_QUADS);
    glVertex2f(s.x, s.y); glVertex2f(s.x+s.w, s.y);
    glVertex2f(s.x+s.w, s.y+s.h); glVertex2f(s.x, s.y+s.h);
    glEnd();
}
int WINAPI wWinMain(HINSTANCE inst, HINSTANCE, PWSTR, int) {
    WNDCLASSW wc{}; wc.lpfnWndProc=wndproc; wc.hInstance=inst; wc.lpszClassName=L"BlendGl";
    wc.hCursor=LoadCursor(nullptr,IDC_ARROW); RegisterClassW(&wc);
    HWND hwnd=CreateWindowExW(0,wc.lpszClassName,L"alpha_blend_scanline OpenGL — Esc quit",
        WS_OVERLAPPEDWINDOW|WS_VISIBLE,CW_USEDEFAULT,CW_USEDEFAULT,960,540,nullptr,nullptr,inst,nullptr);
    if(!hwnd || !init_gl(hwnd)) return 1;
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    auto prev=std::chrono::steady_clock::now();
    MSG msg{}; bool run=true;
    while(run){
        while(PeekMessageW(&msg,nullptr,0,0,PM_REMOVE)){
            if(msg.message==WM_QUIT) run=false;
            TranslateMessage(&msg); DispatchMessageW(&msg);
        }
        auto now=std::chrono::steady_clock::now();
        float dt=std::chrono::duration<float>(now-prev).count(); prev=now;
        blendlab::update_sprite(g_a, dt, 0,0, 960,540);
        blendlab::update_sprite(g_b, dt, 0,0, 960,540);
        glClearColor(0.12f,0.12f,0.14f,1); glClear(GL_COLOR_BUFFER_BIT);
        glMatrixMode(GL_PROJECTION); glLoadIdentity(); glOrtho(0,960,540,0,-1,1);
        glMatrixMode(GL_MODELVIEW); glLoadIdentity();
        for (int y=0;y<540;y+=32) for (int x=0;x<960;x+=32) {
            bool c=((x/32)+(y/32))&1;
            glColor3f(c?0.2f:0.12f, c?0.2f:0.12f, c?0.22f:0.14f);
            glBegin(GL_QUADS); glVertex2f(x,y); glVertex2f(x+32,y); glVertex2f(x+32,y+32); glVertex2f(x,y+32); glEnd();
        }
        draw_sprite(g_a); draw_sprite(g_b);
        SwapBuffers(g_dc); Sleep(1);
    }
    shutdown_gl(hwnd); return 0;
}
