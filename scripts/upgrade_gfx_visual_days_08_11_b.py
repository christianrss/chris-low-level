#!/usr/bin/env python3
"""Finish visual GFX upgrades for gpu_timer, barriers, alpha_blend (+ ensure day10 clean)."""
from __future__ import annotations

import importlib.util
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("u", ROOT / "scripts" / "upgrade_gfx_visual_days_08_11.py")
u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u)

SW_HELPER = u.SW_HELPER
GL_INIT = u.GL_INIT
write_pair = u.write_pair
pedagogy = u.pedagogy


def mod_gpu_timer() -> None:
    mod = ROOT / "days/2026-09-09/graphics/gpu_timer_query"
    name = "gpu_timer"
    hpp = """#pragma once
namespace gputimer {
struct GpuTimer {
    bool running = false;
    double t0 = 0.0;
    double last = 0.0;
    void begin(double now_seconds);
    void end(double now_seconds);
    double last_ms() const;
};
}
"""
    cpp_s = """#include "gpu_timer.hpp"
namespace gputimer {
void GpuTimer::begin(double now_seconds) {
    // TODO [GFX-TQ-BEGIN]
    (void)now_seconds;
}
void GpuTimer::end(double now_seconds) {
    // TODO [GFX-TQ-END]
    (void)now_seconds;
}
double GpuTimer::last_ms() const {
    // TODO [GFX-TQ-READ]
    return 0.0;
}
}
"""
    cpp_sol = """#include "gpu_timer.hpp"
namespace gputimer {
void GpuTimer::begin(double now_seconds) {
    // PEDAGOGY-SOLUTION: GFX-TQ-BEGIN
    running = true;
    t0 = now_seconds;
}
void GpuTimer::end(double now_seconds) {
    // PEDAGOGY-SOLUTION: GFX-TQ-END
    if (!running) return;
    last = (now_seconds - t0) * 1000.0;
    running = false;
}
double GpuTimer::last_ms() const {
    // PEDAGOGY-SOLUTION: GFX-TQ-READ
    return last;
}
}
"""
    test = """#include "gpu_timer.hpp"
#include <cassert>
#include <cmath>
int main() {
    using namespace gputimer;
    GpuTimer t;
    // PEDAGOGY-TEST: GFX-TQ-BEGIN
    t.begin(1.0);
    assert(t.running);
    // PEDAGOGY-TEST: GFX-TQ-END
    t.end(1.016);
    assert(!t.running);
    // PEDAGOGY-TEST: GFX-TQ-READ
    assert(std::abs(t.last_ms() - 16.0) < 0.001);
    return 0;
}
"""
    sw_sol = f'''#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <vector>
#include "gpu_timer.hpp"
{SW_HELPER}
Framebuffer g_fb;
gputimer::GpuTimer g_timer;
float g_t = 0;
void render(double now) {{
    g_timer.begin(now);
    g_fb.clear(rgb(10, 12, 22));
    int cx = 480 + int(120*std::sin(g_t));
    int cy = 270 + int(80*std::cos(g_t*0.9f));
    fill_rect(g_fb, cx-50, cy-50, cx+50, cy+50, rgb(80, 180, 255));
    // busy work to make timer non-zero
    volatile int sink = 0;
    for (int i=0;i<200000; ++i) sink += i;
    g_timer.end(now + 0.001); // wall clock below
}}
LRESULT CALLBACK wndproc(HWND w, UINT m, WPARAM wp, LPARAM lp) {{
    if (m==WM_DESTROY || (m==WM_KEYDOWN && wp==VK_ESCAPE)) {{ PostQuitMessage(0); return 0; }}
    return DefWindowProcW(w,m,wp,lp);
}}
int WINAPI wWinMain(HINSTANCE inst, HINSTANCE, PWSTR, int) {{
    WNDCLASSW wc{{}}; wc.lpfnWndProc=wndproc; wc.hInstance=inst; wc.lpszClassName=L"GpuTimerSw";
    wc.hCursor=LoadCursor(nullptr,IDC_ARROW); RegisterClassW(&wc);
    HWND hwnd=CreateWindowExW(0,wc.lpszClassName,L"gpu_timer_query CPU — Esc quit",
        WS_OVERLAPPEDWINDOW|WS_VISIBLE,CW_USEDEFAULT,CW_USEDEFAULT,960,540,nullptr,nullptr,inst,nullptr);
    if(!hwnd) return 1;
    g_fb.resize(960,540);
    auto t0 = std::chrono::steady_clock::now();
    auto prev = t0;
    MSG msg{{}}; bool run=true;
    while(run){{
        while(PeekMessageW(&msg,nullptr,0,0,PM_REMOVE)){{
            if(msg.message==WM_QUIT) run=false;
            TranslateMessage(&msg); DispatchMessageW(&msg);
        }}
        auto nowc = std::chrono::steady_clock::now();
        float dt = std::chrono::duration<float>(nowc-prev).count(); prev=nowc;
        g_t += dt;
        double now = std::chrono::duration<double>(nowc-t0).count();
        g_timer.begin(now);
        g_fb.clear(rgb(10,12,22));
        int cx = 480 + int(120*std::sin(g_t));
        int cy = 270 + int(80*std::cos(g_t*0.9f));
        fill_rect(g_fb, cx-50, cy-50, cx+50, cy+50, rgb(80,180,255));
        volatile int sink=0; for(int i=0;i<250000;++i) sink+=i;
        double now2 = std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count();
        g_timer.end(now2);
        int bar = int(std::min(400.0, g_timer.last_ms() * 8.0));
        fill_rect(g_fb, 30, 500-bar, 70, 500, rgb(255,200,40));
        present(hwnd, g_fb); Sleep(1);
    }}
    return 0;
}}
'''
    gl_sol = f'''#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include <GL/gl.h>
#include <chrono>
#include <cmath>
#include "gpu_timer.hpp"
{GL_INIT}
gputimer::GpuTimer g_timer;
float g_t=0;
LRESULT CALLBACK wndproc(HWND w, UINT m, WPARAM wp, LPARAM lp) {{
    if (m==WM_DESTROY || (m==WM_KEYDOWN && wp==VK_ESCAPE)) {{ PostQuitMessage(0); return 0; }}
    return DefWindowProcW(w,m,wp,lp);
}}
int WINAPI wWinMain(HINSTANCE inst, HINSTANCE, PWSTR, int) {{
    WNDCLASSW wc{{}}; wc.lpfnWndProc=wndproc; wc.hInstance=inst; wc.lpszClassName=L"GpuTimerGl";
    wc.hCursor=LoadCursor(nullptr,IDC_ARROW); RegisterClassW(&wc);
    HWND hwnd=CreateWindowExW(0,wc.lpszClassName,L"gpu_timer_query OpenGL — Esc quit",
        WS_OVERLAPPEDWINDOW|WS_VISIBLE,CW_USEDEFAULT,CW_USEDEFAULT,960,540,nullptr,nullptr,inst,nullptr);
    if(!hwnd || !init_gl(hwnd)) return 1;
    auto t0=std::chrono::steady_clock::now(); auto prev=t0;
    MSG msg{{}}; bool run=true;
    while(run){{
        while(PeekMessageW(&msg,nullptr,0,0,PM_REMOVE)){{
            if(msg.message==WM_QUIT) run=false;
            TranslateMessage(&msg); DispatchMessageW(&msg);
        }}
        auto nowc=std::chrono::steady_clock::now();
        float dt=std::chrono::duration<float>(nowc-prev).count(); prev=nowc; g_t+=dt;
        double now=std::chrono::duration<double>(nowc-t0).count();
        g_timer.begin(now);
        glClearColor(0.04f,0.05f,0.1f,1); glClear(GL_COLOR_BUFFER_BIT);
        glMatrixMode(GL_PROJECTION); glLoadIdentity(); glOrtho(0,960,0,540,-1,1);
        glMatrixMode(GL_MODELVIEW); glLoadIdentity();
        float cx=480+120*std::sin(g_t); float cy=270+80*std::cos(g_t*0.9f);
        glColor3f(0.3f,0.7f,1); glBegin(GL_QUADS);
        glVertex2f(cx-50,cy-50); glVertex2f(cx+50,cy-50); glVertex2f(cx+50,cy+50); glVertex2f(cx-50,cy+50); glEnd();
        volatile int sink=0; for(int i=0;i<250000;++i) sink+=i;
        double now2=std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count();
        g_timer.end(now2);
        float bar=float(std::min(400.0, g_timer.last_ms()*8.0));
        glColor3f(1,0.8f,0.15f); glBegin(GL_QUADS);
        glVertex2f(30,20); glVertex2f(70,20); glVertex2f(70,20+bar); glVertex2f(30,20+bar); glEnd();
        SwapBuffers(g_dc); Sleep(1);
    }}
    shutdown_gl(hwnd); return 0;
}}
'''
    stub = '''#include <windows.h>
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"TODO: implement core then use solutions backends", L"gpu_timer_query", MB_OK);
    return 0;
}
'''
    write_pair(mod, name, hpp, cpp_s, cpp_sol, test, stub, sw_sol, stub, gl_sol)
    pedagogy(
        mod, "gpu_timer_query",
        "Timer begin/end/read (proxy de GPU timer query) com barra visual do ultimo frame e quad animado.",
        ["GFX-TQ-BEGIN", "GFX-TQ-END", "GFX-TQ-READ"],
        "cd days/2026-09-09/graphics/gpu_timer_query/starter\ncmake -S . -B build_ci -G Ninja\ncmake --build build_ci\nctest --test-dir build_ci --output-on-failure",
        {
            "GFX-TQ-BEGIN": ("starter/core/gpu_timer.cpp", "GpuTimer::begin"),
            "GFX-TQ-END": ("starter/core/gpu_timer.cpp", "GpuTimer::end"),
            "GFX-TQ-READ": ("starter/core/gpu_timer.cpp", "GpuTimer::last_ms"),
        },
        {
            "GFX-TQ-BEGIN": "running = true;\nt0 = now_seconds;\n(void)0;",
            "GFX-TQ-END": "if (!running) return;\nlast = (now_seconds - t0) * 1000.0;\nrunning = false;",
            "GFX-TQ-READ": "return last;\n(void)0;\n(void)0;",
        },
        "Abra `gpu_timer_sw.exe` / `gpu_timer_gl.exe`: quad bounceia e uma barra amarela cresce com last_ms do timer.",
    )
    print("ok gpu_timer")


def mod_barriers() -> None:
    mod = ROOT / "days/2026-09-09/graphics/explicit_barriers"
    name = "barriers"
    hpp = """#pragma once
namespace barriers {
enum class ResourceState { Undefined=0, CopyDst, ShaderRead, RenderTarget, Present, Count };
struct Resource { ResourceState state = ResourceState::Undefined; };
bool can_transition(ResourceState from, ResourceState to);
bool apply_barrier(Resource& r, ResourceState to);
ResourceState next_state(ResourceState s);
}
"""
    cpp_s = """#include "barriers.hpp"
namespace barriers {
bool can_transition(ResourceState from, ResourceState to) {
    // TODO [GFX-BAR-VALID]
    (void)from; (void)to; return false;
}
bool apply_barrier(Resource& r, ResourceState to) {
    // TODO [GFX-BAR-APPLY]
    (void)r; (void)to; return false;
}
ResourceState next_state(ResourceState s) {
    // TODO [GFX-BAR-TICK]
    (void)s; return ResourceState::Undefined;
}
}
"""
    cpp_sol = """#include "barriers.hpp"
namespace barriers {
bool can_transition(ResourceState from, ResourceState to) {
    // PEDAGOGY-SOLUTION: GFX-BAR-VALID
    if (from == to) return true;
    if (from == ResourceState::Undefined && to == ResourceState::CopyDst) return true;
    if (from == ResourceState::CopyDst && to == ResourceState::ShaderRead) return true;
    if (from == ResourceState::ShaderRead && to == ResourceState::RenderTarget) return true;
    if (from == ResourceState::RenderTarget && to == ResourceState::Present) return true;
    if (from == ResourceState::Present && to == ResourceState::CopyDst) return true;
    return false;
}
bool apply_barrier(Resource& r, ResourceState to) {
    // PEDAGOGY-SOLUTION: GFX-BAR-APPLY
    if (!can_transition(r.state, to)) return false;
    r.state = to;
    return true;
}
ResourceState next_state(ResourceState s) {
    // PEDAGOGY-SOLUTION: GFX-BAR-TICK
    switch (s) {
    case ResourceState::Undefined: return ResourceState::CopyDst;
    case ResourceState::CopyDst: return ResourceState::ShaderRead;
    case ResourceState::ShaderRead: return ResourceState::RenderTarget;
    case ResourceState::RenderTarget: return ResourceState::Present;
    default: return ResourceState::CopyDst;
    }
}
}
"""
    test = """#include "barriers.hpp"
#include <cassert>
int main() {
    using namespace barriers;
    // PEDAGOGY-TEST: GFX-BAR-VALID
    assert(can_transition(ResourceState::Undefined, ResourceState::CopyDst));
    assert(!can_transition(ResourceState::Undefined, ResourceState::Present));
    Resource r;
    // PEDAGOGY-TEST: GFX-BAR-APPLY
    assert(apply_barrier(r, ResourceState::CopyDst));
    assert(r.state == ResourceState::CopyDst);
    assert(!apply_barrier(r, ResourceState::Present));
    // PEDAGOGY-TEST: GFX-BAR-TICK
    assert(next_state(ResourceState::CopyDst) == ResourceState::ShaderRead);
    return 0;
}
"""
    # color by state
    sw_sol = f'''#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <vector>
#include "barriers.hpp"
{SW_HELPER}
Framebuffer g_fb;
barriers::Resource g_res;
float g_t=0, g_acc=0;
std::uint32_t state_color(barriers::ResourceState s) {{
    using barriers::ResourceState;
    switch(s){{
    case ResourceState::Undefined: return rgb(20,20,20);
    case ResourceState::CopyDst: return rgb(40,40,120);
    case ResourceState::ShaderRead: return rgb(40,120,60);
    case ResourceState::RenderTarget: return rgb(160,80,40);
    case ResourceState::Present: return rgb(200,200,60);
    default: return rgb(0,0,0);
    }}
}}
LRESULT CALLBACK wndproc(HWND w, UINT m, WPARAM wp, LPARAM lp) {{
    if (m==WM_DESTROY || (m==WM_KEYDOWN && wp==VK_ESCAPE)) {{ PostQuitMessage(0); return 0; }}
    return DefWindowProcW(w,m,wp,lp);
}}
int WINAPI wWinMain(HINSTANCE inst, HINSTANCE, PWSTR, int) {{
    WNDCLASSW wc{{}}; wc.lpfnWndProc=wndproc; wc.hInstance=inst; wc.lpszClassName=L"BarriersSw";
    wc.hCursor=LoadCursor(nullptr,IDC_ARROW); RegisterClassW(&wc);
    HWND hwnd=CreateWindowExW(0,wc.lpszClassName,L"explicit_barriers CPU — Esc quit",
        WS_OVERLAPPEDWINDOW|WS_VISIBLE,CW_USEDEFAULT,CW_USEDEFAULT,960,540,nullptr,nullptr,inst,nullptr);
    if(!hwnd) return 1;
    g_fb.resize(960,540);
    auto prev=std::chrono::steady_clock::now();
    MSG msg{{}}; bool run=true;
    while(run){{
        while(PeekMessageW(&msg,nullptr,0,0,PM_REMOVE)){{
            if(msg.message==WM_QUIT) run=false;
            TranslateMessage(&msg); DispatchMessageW(&msg);
        }}
        auto now=std::chrono::steady_clock::now();
        float dt=std::chrono::duration<float>(now-prev).count(); prev=now;
        g_t+=dt; g_acc+=dt;
        if(g_acc>1.0f){{
            auto nxt = barriers::next_state(g_res.state);
            barriers::apply_barrier(g_res, nxt);
            g_acc=0;
        }}
        g_fb.clear(state_color(g_res.state));
        int x = 100 + int(60*std::sin(g_t*2));
        fill_rect(g_fb, x, 200, x+120, 320, rgb(255,255,255));
        present(hwnd, g_fb); Sleep(1);
    }}
    return 0;
}}
'''
    gl_sol = f'''#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include <GL/gl.h>
#include <chrono>
#include <cmath>
#include "barriers.hpp"
{GL_INIT}
barriers::Resource g_res;
float g_t=0, g_acc=0;
void clear_for_state(barriers::ResourceState s) {{
    using barriers::ResourceState;
    switch(s){{
    case ResourceState::Undefined: glClearColor(0.08f,0.08f,0.08f,1); break;
    case ResourceState::CopyDst: glClearColor(0.15f,0.15f,0.45f,1); break;
    case ResourceState::ShaderRead: glClearColor(0.15f,0.45f,0.22f,1); break;
    case ResourceState::RenderTarget: glClearColor(0.55f,0.3f,0.15f,1); break;
    case ResourceState::Present: glClearColor(0.7f,0.7f,0.2f,1); break;
    default: glClearColor(0,0,0,1); break;
    }}
}}
LRESULT CALLBACK wndproc(HWND w, UINT m, WPARAM wp, LPARAM lp) {{
    if (m==WM_DESTROY || (m==WM_KEYDOWN && wp==VK_ESCAPE)) {{ PostQuitMessage(0); return 0; }}
    return DefWindowProcW(w,m,wp,lp);
}}
int WINAPI wWinMain(HINSTANCE inst, HINSTANCE, PWSTR, int) {{
    WNDCLASSW wc{{}}; wc.lpfnWndProc=wndproc; wc.hInstance=inst; wc.lpszClassName=L"BarriersGl";
    wc.hCursor=LoadCursor(nullptr,IDC_ARROW); RegisterClassW(&wc);
    HWND hwnd=CreateWindowExW(0,wc.lpszClassName,L"explicit_barriers OpenGL — Esc quit",
        WS_OVERLAPPEDWINDOW|WS_VISIBLE,CW_USEDEFAULT,CW_USEDEFAULT,960,540,nullptr,nullptr,inst,nullptr);
    if(!hwnd || !init_gl(hwnd)) return 1;
    auto prev=std::chrono::steady_clock::now();
    MSG msg{{}}; bool run=true;
    while(run){{
        while(PeekMessageW(&msg,nullptr,0,0,PM_REMOVE)){{
            if(msg.message==WM_QUIT) run=false;
            TranslateMessage(&msg); DispatchMessageW(&msg);
        }}
        auto now=std::chrono::steady_clock::now();
        float dt=std::chrono::duration<float>(now-prev).count(); prev=now;
        g_t+=dt; g_acc+=dt;
        if(g_acc>1.0f){{
            auto nxt=barriers::next_state(g_res.state);
            barriers::apply_barrier(g_res, nxt);
            g_acc=0;
        }}
        clear_for_state(g_res.state); glClear(GL_COLOR_BUFFER_BIT);
        glMatrixMode(GL_PROJECTION); glLoadIdentity(); glOrtho(0,960,0,540,-1,1);
        glMatrixMode(GL_MODELVIEW); glLoadIdentity();
        float x=100+60*std::sin(g_t*2);
        glColor3f(1,1,1); glBegin(GL_QUADS);
        glVertex2f(x,200); glVertex2f(x+120,200); glVertex2f(x+120,320); glVertex2f(x,320); glEnd();
        SwapBuffers(g_dc); Sleep(1);
    }}
    shutdown_gl(hwnd); return 0;
}}
'''
    stub = '''#include <windows.h>
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"TODO: implement core then use solutions backends", L"explicit_barriers", MB_OK);
    return 0;
}
'''
    write_pair(mod, name, hpp, cpp_s, cpp_sol, test, stub, sw_sol, stub, gl_sol)
    pedagogy(
        mod, "explicit_barriers",
        "Transicoes explicitas de ResourceState com validacao; cor de fundo muda a cada barreira aplicada.",
        ["GFX-BAR-VALID", "GFX-BAR-APPLY", "GFX-BAR-TICK"],
        "cd days/2026-09-09/graphics/explicit_barriers/starter\ncmake -S . -B build_ci -G Ninja\ncmake --build build_ci\nctest --test-dir build_ci --output-on-failure",
        {
            "GFX-BAR-VALID": ("starter/core/barriers.cpp", "can_transition"),
            "GFX-BAR-APPLY": ("starter/core/barriers.cpp", "apply_barrier"),
            "GFX-BAR-TICK": ("starter/core/barriers.cpp", "next_state"),
        },
        {
            "GFX-BAR-VALID": "if (from == ResourceState::Undefined && to == ResourceState::CopyDst) return true;\nif (from == ResourceState::CopyDst && to == ResourceState::ShaderRead) return true;\nreturn from == to;",
            "GFX-BAR-APPLY": "if (!can_transition(r.state, to)) return false;\nr.state = to;\nreturn true;",
            "GFX-BAR-TICK": "if (s == ResourceState::Undefined) return ResourceState::CopyDst;\nif (s == ResourceState::CopyDst) return ResourceState::ShaderRead;\nreturn ResourceState::Present;",
        },
        "Abra `barriers_sw.exe` / `barriers_gl.exe`: fundo muda de cor a cada ~1s (ciclo de estados) e um sprite branco se move.",
    )
    print("ok barriers")


def mod_alpha() -> None:
    mod = ROOT / "days/2026-09-11/graphics/alpha_blend_scanline"
    name = "blend"
    hpp = """#pragma once
#include <cstdint>
namespace blendlab {
struct Pixel { std::uint8_t r,g,b,a; };
struct Sprite { float x,y,vx,vy; int w,h; Pixel color; };
void blend_pixel(Pixel& dst, Pixel src);
void blend_scanline(Pixel* dst, const Pixel* src, int n);
void update_sprite(Sprite& s, float dt, float minx, float miny, float maxx, float maxy);
}
"""
    cpp_s = """#include "blend.hpp"
namespace blendlab {
void blend_pixel(Pixel& dst, Pixel src) {
    // TODO [GFX-BLEND-PIXEL]
    (void)dst; (void)src;
}
void blend_scanline(Pixel* dst, const Pixel* src, int n) {
    // TODO [GFX-BLEND-SCAN]
    (void)dst; (void)src; (void)n;
}
void update_sprite(Sprite& s, float dt, float minx, float miny, float maxx, float maxy) {
    // TODO [GFX-BLEND-SPRITE]
    (void)s; (void)dt; (void)minx; (void)miny; (void)maxx; (void)maxy;
}
}
"""
    cpp_sol = """#include "blend.hpp"
namespace blendlab {
void blend_pixel(Pixel& dst, Pixel src) {
    // PEDAGOGY-SOLUTION: GFX-BLEND-PIXEL
    const float sa = src.a / 255.0f;
    const float da = 1.0f - sa;
    dst.r = static_cast<std::uint8_t>(src.r * sa + dst.r * da);
    dst.g = static_cast<std::uint8_t>(src.g * sa + dst.g * da);
    dst.b = static_cast<std::uint8_t>(src.b * sa + dst.b * da);
    dst.a = 255;
}
void blend_scanline(Pixel* dst, const Pixel* src, int n) {
    // PEDAGOGY-SOLUTION: GFX-BLEND-SCAN
    for (int i = 0; i < n; ++i) blend_pixel(dst[i], src[i]);
}
void update_sprite(Sprite& s, float dt, float minx, float miny, float maxx, float maxy) {
    // PEDAGOGY-SOLUTION: GFX-BLEND-SPRITE
    s.x += s.vx * dt;
    s.y += s.vy * dt;
    if (s.x < minx || s.x + s.w > maxx) { s.vx = -s.vx; s.x += s.vx * dt; }
    if (s.y < miny || s.y + s.h > maxy) { s.vy = -s.vy; s.y += s.vy * dt; }
}
}
"""
    test = """#include "blend.hpp"
#include <cassert>
int main() {
    using namespace blendlab;
    Pixel dst{0,0,0,255};
    Pixel src{255,0,0,128};
    // PEDAGOGY-TEST: GFX-BLEND-PIXEL
    blend_pixel(dst, src);
    assert(dst.r > 100);
    Pixel line_d[2]={{0,0,0,255},{0,0,0,255}};
    Pixel line_s[2]={{0,255,0,255},{0,0,255,255}};
    // PEDAGOGY-TEST: GFX-BLEND-SCAN
    blend_scanline(line_d, line_s, 2);
    assert(line_d[0].g == 255);
    Sprite s{10,10, 50,-40, 20,20, {255,255,255,128}};
    // PEDAGOGY-TEST: GFX-BLEND-SPRITE
    update_sprite(s, 0.1f, 0, 0, 100, 100);
    assert(s.x > 10);
    return 0;
}
"""
    sw_sol = f'''#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <vector>
#include "blend.hpp"
{SW_HELPER}
using blendlab::Pixel; using blendlab::Sprite;
Framebuffer g_fb;
std::vector<Pixel> g_pix;
Sprite g_a{{80,80, 140,90, 90,70, {{255,40,40,140}}}};
Sprite g_b{{400,200, -110,120, 110,80, {{40,80,255,160}}}};
void blit_sprite(const Sprite& s) {{
    for (int y=0; y<s.h; ++y) {{
        int py = int(s.y)+y;
        if (py<0||py>=g_fb.height) continue;
        for (int x=0; x<s.w; ++x) {{
            int px = int(s.x)+x;
            if (px<0||px>=g_fb.width) continue;
            Pixel& d = g_pix[py*g_fb.width+px];
            blendlab::blend_pixel(d, s.color);
        }}
    }}
}}
void to_fb() {{
    for (int i=0;i<g_fb.width*g_fb.height;++i) {{
        auto& p=g_pix[i];
        g_fb.pixels[i]=rgb(p.r,p.g,p.b);
    }}
}}
LRESULT CALLBACK wndproc(HWND w, UINT m, WPARAM wp, LPARAM lp) {{
    if (m==WM_DESTROY || (m==WM_KEYDOWN && wp==VK_ESCAPE)) {{ PostQuitMessage(0); return 0; }}
    return DefWindowProcW(w,m,wp,lp);
}}
int WINAPI wWinMain(HINSTANCE inst, HINSTANCE, PWSTR, int) {{
    WNDCLASSW wc{{}}; wc.lpfnWndProc=wndproc; wc.hInstance=inst; wc.lpszClassName=L"BlendSw";
    wc.hCursor=LoadCursor(nullptr,IDC_ARROW); RegisterClassW(&wc);
    HWND hwnd=CreateWindowExW(0,wc.lpszClassName,L"alpha_blend_scanline CPU — Esc quit",
        WS_OVERLAPPEDWINDOW|WS_VISIBLE,CW_USEDEFAULT,CW_USEDEFAULT,960,540,nullptr,nullptr,inst,nullptr);
    if(!hwnd) return 1;
    g_fb.resize(960,540);
    g_pix.resize(960*540);
    auto prev=std::chrono::steady_clock::now();
    MSG msg{{}}; bool run=true;
    while(run){{
        while(PeekMessageW(&msg,nullptr,0,0,PM_REMOVE)){{
            if(msg.message==WM_QUIT) run=false;
            TranslateMessage(&msg); DispatchMessageW(&msg);
        }}
        auto now=std::chrono::steady_clock::now();
        float dt=std::chrono::duration<float>(now-prev).count(); prev=now;
        blendlab::update_sprite(g_a, dt, 0,0, 960,540);
        blendlab::update_sprite(g_b, dt, 0,0, 960,540);
        for (int y=0;y<540;++y) for (int x=0;x<960;++x) {{
            bool c=((x/32)+(y/32))&1;
            g_pix[y*960+x]= c? Pixel{{50,50,55,255}}:Pixel{{30,30,35,255}};
        }}
        blit_sprite(g_a); blit_sprite(g_b);
        to_fb(); present(hwnd, g_fb); Sleep(1);
    }}
    return 0;
}}
'''
    gl_sol = f'''#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include <GL/gl.h>
#include <chrono>
#include "blend.hpp"
{GL_INIT}
using blendlab::Sprite;
Sprite g_a{{80,80, 140,90, 90,70, {{255,40,40,140}}}};
Sprite g_b{{400,200, -110,120, 110,80, {{40,80,255,160}}}};
LRESULT CALLBACK wndproc(HWND w, UINT m, WPARAM wp, LPARAM lp) {{
    if (m==WM_DESTROY || (m==WM_KEYDOWN && wp==VK_ESCAPE)) {{ PostQuitMessage(0); return 0; }}
    return DefWindowProcW(w,m,wp,lp);
}}
void draw_sprite(const Sprite& s) {{
    float a=s.color.a/255.f;
    glColor4f(s.color.r/255.f, s.color.g/255.f, s.color.b/255.f, a);
    glBegin(GL_QUADS);
    glVertex2f(s.x, s.y); glVertex2f(s.x+s.w, s.y);
    glVertex2f(s.x+s.w, s.y+s.h); glVertex2f(s.x, s.y+s.h);
    glEnd();
}}
int WINAPI wWinMain(HINSTANCE inst, HINSTANCE, PWSTR, int) {{
    WNDCLASSW wc{{}}; wc.lpfnWndProc=wndproc; wc.hInstance=inst; wc.lpszClassName=L"BlendGl";
    wc.hCursor=LoadCursor(nullptr,IDC_ARROW); RegisterClassW(&wc);
    HWND hwnd=CreateWindowExW(0,wc.lpszClassName,L"alpha_blend_scanline OpenGL — Esc quit",
        WS_OVERLAPPEDWINDOW|WS_VISIBLE,CW_USEDEFAULT,CW_USEDEFAULT,960,540,nullptr,nullptr,inst,nullptr);
    if(!hwnd || !init_gl(hwnd)) return 1;
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    auto prev=std::chrono::steady_clock::now();
    MSG msg{{}}; bool run=true;
    while(run){{
        while(PeekMessageW(&msg,nullptr,0,0,PM_REMOVE)){{
            if(msg.message==WM_QUIT) run=false;
            TranslateMessage(&msg); DispatchMessageW(&msg);
        }}
        auto now=std::chrono::steady_clock::now();
        float dt=std::chrono::duration<float>(now-prev).count(); prev=now;
        blendlab::update_sprite(g_a, dt, 0,0, 960,540);
        blendlab::update_sprite(g_b, dt, 0,0, 960,540);
        glClearColor(0.12f,0.12f,0.14f,1); glClear(GL_COLOR_BUFFER_BIT);
        glMatrixMode(GL_PROJECTION); glLoadIdentity(); glOrtho(0,960,540,0,-1,1);
        glMatrixMode(GL_MODELVIEW); glLoadIdentity();
        for (int y=0;y<540;y+=32) for (int x=0;x<960;x+=32) {{
            bool c=((x/32)+(y/32))&1;
            glColor3f(c?0.2f:0.12f, c?0.2f:0.12f, c?0.22f:0.14f);
            glBegin(GL_QUADS); glVertex2f(x,y); glVertex2f(x+32,y); glVertex2f(x+32,y+32); glVertex2f(x,y+32); glEnd();
        }}
        draw_sprite(g_a); draw_sprite(g_b);
        SwapBuffers(g_dc); Sleep(1);
    }}
    shutdown_gl(hwnd); return 0;
}}
'''
    stub = '''#include <windows.h>
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"TODO: implement core then use solutions backends", L"alpha_blend", MB_OK);
    return 0;
}
'''
    write_pair(mod, name, hpp, cpp_s, cpp_sol, test, stub, sw_sol, stub, gl_sol)
    # remove leftover flat blend files if any
    for p in list(mod.glob("**/blend.hpp")) + list(mod.glob("**/blend.cpp")) + list(mod.glob("**/test_blend.cpp")):
        if "core" not in p.parts and "tests" not in p.parts:
            p.unlink(missing_ok=True)
    pedagogy(
        mod, "alpha_blend_scanline",
        "Porter-Duff src-over em CPU (pixel/scanline) + sprites bouncing; OpenGL usa GL_BLEND na mesma cena.",
        ["GFX-BLEND-PIXEL", "GFX-BLEND-SCAN", "GFX-BLEND-SPRITE"],
        "cd days/2026-09-11/graphics/alpha_blend_scanline/starter\ncmake -S . -B build_ci -G Ninja\ncmake --build build_ci\nctest --test-dir build_ci --output-on-failure",
        {
            "GFX-BLEND-PIXEL": ("starter/core/blend.cpp", "blend_pixel"),
            "GFX-BLEND-SCAN": ("starter/core/blend.cpp", "blend_scanline"),
            "GFX-BLEND-SPRITE": ("starter/core/blend.cpp", "update_sprite"),
        },
        {
            "GFX-BLEND-PIXEL": "float sa = src.a / 255.0f;\nfloat da = 1.0f - sa;\ndst.r = (uint8_t)(src.r * sa + dst.r * da);",
            "GFX-BLEND-SCAN": "for (int i = 0; i < n; ++i) {\n  blend_pixel(dst[i], src[i]);\n}",
            "GFX-BLEND-SPRITE": "s.x += s.vx * dt;\ns.y += s.vy * dt;\nif (s.x < minx || s.x + s.w > maxx) s.vx = -s.vx;",
        },
        "Abra `blend_sw.exe` / `blend_gl.exe`: checkerboard + dois sprites translucidos quicando e se misturando.",
    )
    print("ok alpha")


if __name__ == "__main__":
    mod_gpu_timer()
    mod_barriers()
    mod_alpha()
    print("done b")
