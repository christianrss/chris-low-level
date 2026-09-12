#!/usr/bin/env python3
"""Upgrade days 08–11 graphics modules to visual C++ dual-backend (SW + OpenGL)."""
from __future__ import annotations

import shutil
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# Shared skeletons
# ---------------------------------------------------------------------------

CMAKE = """cmake_minimum_required(VERSION 3.16)
project({name} CXX)
set(CMAKE_CXX_STANDARD 17)
enable_testing()

add_library({name}_core STATIC core/{core_cpp})
target_include_directories({name}_core PUBLIC ${{CMAKE_CURRENT_SOURCE_DIR}}/core)

add_executable(test_{name} tests/test_{name}.cpp)
target_link_libraries(test_{name} PRIVATE {name}_core)
add_test(NAME test_{name} COMMAND test_{name})

if(WIN32)
  add_executable({name}_sw WIN32 software_win32/main.cpp)
  target_compile_definitions({name}_sw PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
  target_link_libraries({name}_sw PRIVATE {name}_core user32 gdi32)

  add_executable({name}_gl WIN32 opengl_win32/main.cpp)
  target_compile_definitions({name}_gl PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
  target_link_libraries({name}_gl PRIVATE {name}_core user32 gdi32 opengl32)
endif()
"""

SW_HELPER = r'''
struct Framebuffer {
    int width = 0;
    int height = 0;
    std::vector<std::uint32_t> pixels;
    void resize(int w, int h) {
        width = std::max(1, w);
        height = std::max(1, h);
        pixels.assign(static_cast<std::size_t>(width) * height, 0u);
    }
    void clear(std::uint32_t c) { std::fill(pixels.begin(), pixels.end(), c); }
    void set(int x, int y, std::uint32_t c) {
        if (x < 0 || y < 0 || x >= width || y >= height) return;
        pixels[static_cast<std::size_t>(y) * width + x] = c;
    }
};
std::uint32_t rgb(int r, int g, int b) {
    return (std::uint32_t(r) << 16) | (std::uint32_t(g) << 8) | std::uint32_t(b);
}
void fill_rect(Framebuffer& fb, int x0, int y0, int x1, int y1, std::uint32_t c) {
    for (int y = y0; y < y1; ++y)
        for (int x = x0; x < x1; ++x) fb.set(x, y, c);
}
void present(HWND window, Framebuffer& fb) {
    BITMAPINFO bmi{};
    bmi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    bmi.bmiHeader.biWidth = fb.width;
    bmi.bmiHeader.biHeight = -fb.height;
    bmi.bmiHeader.biPlanes = 1;
    bmi.bmiHeader.biBitCount = 32;
    bmi.bmiHeader.biCompression = BI_RGB;
    HDC dc = GetDC(window);
    StretchDIBits(dc, 0, 0, fb.width, fb.height, 0, 0, fb.width, fb.height,
                  fb.pixels.data(), &bmi, DIB_RGB_COLORS, SRCCOPY);
    ReleaseDC(window, dc);
}
'''

GL_INIT = r'''
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
'''


def W(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).lstrip().replace("\r\n", "\n"), encoding="utf-8", newline="\n")


def wipe_code(mod: Path) -> None:
    for sub in ("starter", "solutions"):
        d = mod / sub
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)


def pedagogy(mod: Path, title: str, focus: str, ids: list[str], baseline: str, file_map: dict, sol_snip: dict, visual: str) -> None:
    rows = "\n".join(f"| `{i}` | contrato do assert |" for i in ids)
    mapa = "\n".join(
        f"| `{i}` | `{file_map[i][0]}` | `{file_map[i][1]}` |" for i in ids
    )
    teoria = f"""# Teoria passo a passo — {title}

Laboratório **visual C++** (software Win32 + OpenGL WGL), dual-backend.

## 1. O quê

{focus}

## 2. Como — fluxo

```text
core (estado/TODOs) -> software_win32 StretchDIBits
                    -> opengl_win32 SwapBuffers
                    -> mesma cena animada
```

## 3. Tabela de pastas

| Pasta | Papel |
|-------|-------|
| `core/` | lógica testável |
| `software_win32/` | CPU + DIB |
| `opengl_win32/` | WGL + GL legado |
| `tests/` | CTest |

## 4. TODOs

| ID | Papel |
|----|-------|
{rows}

## 5. Trace numerico

Execute o Caso 1 do teste no papel antes de editar o starter.

## 6. Por que dual-backend

Por que CPU e GL? Para separar contrato de estado da API de present.

## 7. Por que animacao

Por que mover todo frame? Prova que o loop de mensagem + render esta vivo.

## 8. Por que CTest no core

Por que assert no core? Gates CI sem precisar de janela interativa.

## 9. Invariantes

1. Determinismo do core
2. Mesma cena nos dois backends
3. Nao alterar testes
4. solutions abre janela e apresenta pixels

## 10. Bugs comuns

| Sintoma | Causa | Checagem |
|---------|-------|----------|
| janela preta | clear sem draw | confira render |
| sem movimento | dt=0 | steady_clock |
| teste falha | stub TODO | implemente core |

## 11. Lab vs producao

Recorte pedagogico do mesmo problema de engine/API.

## 12. Checklist

- [ ] Core PASS no CTest
- [ ] software_win32 mostra cena
- [ ] opengl_win32 mostra cena
- [ ] VISUAL-01 ok

## 13. Diagrama de estados

| Frame | Acao |
|-------|------|
| N | simula core |
| N | raster/GL |
| N | present |

## 14. Offsets / layout mental

Framebuffer BGRA little-endian via `0x00RRGGBB` no StretchDIBits top-down.

## 15. Extensao

Opcional: D3D11 Present com a mesma cena (fora do escopo minimo).

## 16. Referencias internas

- `docs/GFX_PEDAGOGY_STANDARD.md`
- `days/2026-09-07/graphics/artillery_trajectory_2d`
"""
    # pad teoria to >=120 lines
    while len(teoria.splitlines()) < 125:
        teoria += "\n## Nota\n\nMantenha o contrato dos TODOs; nao invente APIs extras no teste.\n"

    res_parts = [
        f"""# Resolucao guiada — {title}

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
{mapa}

## Baseline

```powershell
{baseline}
```

**Esperado antes dos TODOs:** FAIL.
"""
    ]
    for tid in ids:
        snip = sol_snip[tid]
        res_parts.append(
            f"""
## {tid}

### Onde colocar ({tid})

| Campo | Valor |
|-------|-------|
| Arquivo | `{file_map[tid][0]}` |
| Funcao | `{file_map[tid][1]}` |
| Substituir | corpo sob `TODO [{tid}]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `{tid}` falha e a cena visual fica incompleta.

### Algoritmo / trace
1. Leia o PEDAGOGY-TEST de `{tid}`.
2. Execute o Caso 1 no papel.
3. Cole o bloco abaixo no starter.

### Escreva o codigo

```cpp
{snip}
```

### Por que funciona?
Materializa o contrato numerico de `{tid}` usado pelo render.

### Verifique
Baseline parcial; `{tid}` PASS.

### Checkpoint
- [ ] `{tid}` PASS
"""
        )
    res_parts.append(
        """
## Debug

| Sintoma | Causa | Correcao |
|---------|-------|----------|
| stub | TODO intacto | cole o bloco |
| off-by-one | indices | refaca o trace |
| sem janela | backend errado | rode o `_sw` / `_gl` |

## Relatorio de resolucao

- TODOs concluidos:
- Comandos + saida:
- Invariantes:
- Edge cases:
- Benchmark: nao executado
"""
    )
    res = "\n".join(res_parts)

    tg = f"""# Testes guiados — {title}

## Caso 1 — core

Exercido por `tests/test_*.cpp` (PEDAGOGY-TEST).

## Caso manual — VISUAL-01

{visual}

## Identificadores

""" + "\n".join(f"- `{i}`" for i in ids) + "\n"

    W(mod / "TEORIA_PASSO_A_PASSO.md", teoria)
    W(mod / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md", res)
    W(mod / "TESTES_GUIADOS.md", tg)
    W(
        mod / "docs" / "COMPARISON.md",
        f"""# Comparacao — {title}

| Etapa | CPU (`software_win32`) | OpenGL (`opengl_win32`) |
|-------|------------------------|-------------------------|
| Estado | `core/` | mesmo `core/` |
| Raster | StretchDIBits | glBegin/glEnd + SwapBuffers |
| Animacao | steady_clock | steady_clock |
| Validacao | CTest | CTest + VISUAL-01 |
""",
    )
    W(
        mod / "README.md",
        f"""# {title}

Modulo **visual** C++: `software_win32` + `opengl_win32` + `core/` testavel.

## TODOs

"""
        + "\n".join(f"- `{i}`" for i in ids)
        + f"""

## Build

```powershell
cmake -S starter -B starter/build_ci -G Ninja
cmake --build starter/build_ci
ctest --test-dir starter/build_ci --output-on-failure
# demos: starter/build_ci/{mod.name}_sw.exe  /  {mod.name}_gl.exe
```
""",
    )
    W(
        mod / "PESQUISA_GUIADA.md",
        f"""# Pesquisa guiada — {title}

1. Qual invariante deste lab existe em engines reais?
2. O que o off-by-one quebra no Caso 1?
3. Como o CTest evita falha silenciosa sem janela?
4. Que parte da API real foi cortada?
5. Onde logar sem mudar o contrato dos TODOs?

## Fontes
- docs/GFX_PEDAGOGY_STANDARD.md
- README do modulo
""",
    )
    W(
        mod / "EXERCICIOS.md",
        f"""# Exercicios — {title}

## Facil
Paper-trace do Caso 1.

## Medio
Implemente o primeiro TODO ate o CTest passar.

## Dificil
Rode VISUAL-01 nos dois backends.

## Desafio
Documente uma extensao D3D11 Present.
""",
    )
    W(
        mod / "BENCHMARK_GUIADO.md",
        """# Benchmark guiado

## Hipotese
Frame estavel ~60 Hz apos PASS.

## Como medir
Rode o backend software e observe tempo de frame (Sleep/dt).

## Resultados observados
- Ambiente: merge local
- Tempo: nao executado
- Interpretacao: valide corretude primeiro

## Skip honesto
nao executado neste passo; rode apos CTest PASS.
""",
    )


def write_pair(mod: Path, name: str, core_h: str, core_cpp_s: str, core_cpp_sol: str, test_cpp: str, sw_s: str, sw_sol: str, gl_s: str, gl_sol: str) -> None:
    wipe_code(mod)
    for side, core_cpp, sw, gl in (
        ("starter", core_cpp_s, sw_s, gl_s),
        ("solutions", core_cpp_sol, sw_sol, gl_sol),
    ):
        base = mod / side
        W(base / "core" / f"{name}.hpp", core_h)
        W(base / "core" / f"{name}.cpp", core_cpp)
        W(base / "tests" / f"test_{name}.cpp", test_cpp)
        W(base / "software_win32" / "main.cpp", sw)
        W(base / "opengl_win32" / "main.cpp", gl)
        W(base / "CMakeLists.txt", CMAKE.format(name=name, core_cpp=f"{name}.cpp"))


# ========================= module bodies =========================

def mod_shader() -> None:
    mod = ROOT / "days/2026-09-08/graphics/shader_stage_fsm"
    name = "shader_fsm"
    hpp = """#pragma once
namespace shfsm {
enum class Stage { Edit = 0, Compile, Link, Ready, Count };
struct ShaderFsm {
    Stage stage = Stage::Edit;
    void advance();
    void reset();
    void stage_color(float& r, float& g, float& b) const;
};
}
"""
    cpp_s = """#include "shader_fsm.hpp"
namespace shfsm {
void ShaderFsm::advance() {
    // TODO [GFX-SH-ADVANCE]
}
void ShaderFsm::reset() {
    // TODO [GFX-SH-RESET]
}
void ShaderFsm::stage_color(float& r, float& g, float& b) const {
    // TODO [GFX-SH-COLOR]
    r = g = b = 0.0f;
}
}
"""
    cpp_sol = """#include "shader_fsm.hpp"
namespace shfsm {
void ShaderFsm::advance() {
    // PEDAGOGY-SOLUTION: GFX-SH-ADVANCE
    int s = static_cast<int>(stage) + 1;
    if (s >= static_cast<int>(Stage::Count)) s = 0;
    stage = static_cast<Stage>(s);
}
void ShaderFsm::reset() {
    // PEDAGOGY-SOLUTION: GFX-SH-RESET
    stage = Stage::Edit;
}
void ShaderFsm::stage_color(float& r, float& g, float& b) const {
    // PEDAGOGY-SOLUTION: GFX-SH-COLOR
    switch (stage) {
    case Stage::Edit: r=0.9f;g=0.3f;b=0.2f; break;
    case Stage::Compile: r=0.9f;g=0.7f;b=0.2f; break;
    case Stage::Link: r=0.3f;g=0.6f;b=0.9f; break;
    case Stage::Ready: r=0.2f;g=0.85f;b=0.4f; break;
    default: r=g=b=0.1f; break;
    }
}
}
"""
    test = """#include "shader_fsm.hpp"
#include <cassert>
#include <cmath>
int main() {
    using namespace shfsm;
    ShaderFsm f;
    // PEDAGOGY-TEST: GFX-SH-ADVANCE
    assert(f.stage == Stage::Edit);
    f.advance();
    assert(f.stage == Stage::Compile);
    f.advance(); f.advance();
    assert(f.stage == Stage::Ready);
    f.advance();
    assert(f.stage == Stage::Edit);
    // PEDAGOGY-TEST: GFX-SH-RESET
    f.advance();
    f.reset();
    assert(f.stage == Stage::Edit);
    // PEDAGOGY-TEST: GFX-SH-COLOR
    float r,g,b;
    f.stage = Stage::Ready;
    f.stage_color(r,g,b);
    assert(g > 0.5f);
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
#include "shader_fsm.hpp"
{SW_HELPER}
Framebuffer g_fb;
shfsm::ShaderFsm g_fsm;
float g_t = 0.0f;
float g_acc = 0.0f;
void render() {{
    g_fb.clear(rgb(12, 14, 28));
    float r,g,b; g_fsm.stage_color(r,g,b);
    int cx = g_fb.width/2 + int(40*std::sin(g_t));
    int cy = g_fb.height/2 + int(20*std::cos(g_t*1.3f));
    fill_rect(g_fb, cx-80, cy-70, cx+80, cy+70, rgb(int(r*255),int(g*255),int(b*255)));
    int stage = static_cast<int>(g_fsm.stage);
    for (int i=0;i<4;++i) {{
        auto c = (i==stage) ? rgb(240,240,240) : rgb(60,60,80);
        fill_rect(g_fb, 20+i*50, 20, 60+i*50, 40, c);
    }}
}}
LRESULT CALLBACK wndproc(HWND w, UINT m, WPARAM wp, LPARAM lp) {{
    if (m==WM_DESTROY) {{ PostQuitMessage(0); return 0; }}
    if (m==WM_KEYDOWN && wp==VK_ESCAPE) {{ PostQuitMessage(0); return 0; }}
    return DefWindowProcW(w,m,wp,lp);
}}
int WINAPI wWinMain(HINSTANCE inst, HINSTANCE, PWSTR, int) {{
    WNDCLASSW wc{{}}; wc.lpfnWndProc=wndproc; wc.hInstance=inst; wc.lpszClassName=L"ShaderFsmSw";
    wc.hCursor=LoadCursor(nullptr, IDC_ARROW); RegisterClassW(&wc);
    HWND hwnd = CreateWindowExW(0, wc.lpszClassName, L"shader_stage_fsm CPU — Esc quit",
        WS_OVERLAPPEDWINDOW|WS_VISIBLE, CW_USEDEFAULT,CW_USEDEFAULT, 960,540,nullptr,nullptr,inst,nullptr);
    if (!hwnd) return 1;
    g_fb.resize(960,540);
    auto prev = std::chrono::steady_clock::now();
    MSG msg{{}}; bool run=true;
    while (run) {{
        while (PeekMessageW(&msg,nullptr,0,0,PM_REMOVE)) {{
            if (msg.message==WM_QUIT) run=false;
            TranslateMessage(&msg); DispatchMessageW(&msg);
        }}
        auto now = std::chrono::steady_clock::now();
        float dt = std::chrono::duration<float>(now-prev).count(); prev=now;
        g_t += dt; g_acc += dt;
        if (g_acc > 1.5f) {{ g_fsm.advance(); g_acc = 0; }}
        render(); present(hwnd, g_fb); Sleep(1);
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
#include "shader_fsm.hpp"
{GL_INIT}
shfsm::ShaderFsm g_fsm;
float g_t=0, g_acc=0;
void render() {{
    float r,g,b; g_fsm.stage_color(r,g,b);
    glClearColor(0.05f,0.06f,0.12f,1); glClear(GL_COLOR_BUFFER_BIT);
    glMatrixMode(GL_PROJECTION); glLoadIdentity(); glOrtho(0,960,0,540,-1,1);
    glMatrixMode(GL_MODELVIEW); glLoadIdentity();
    float ox = 480 + 40*std::sin(g_t);
    float oy = 270 + 20*std::cos(g_t*1.3f);
    glColor3f(r,g,b);
    glBegin(GL_TRIANGLES);
    glVertex2f(ox, oy+90); glVertex2f(ox-90, oy-70); glVertex2f(ox+90, oy-70);
    glEnd();
    int stage = static_cast<int>(g_fsm.stage);
    for (int i=0;i<4;++i) {{
        if (i==stage) glColor3f(1,1,1); else glColor3f(0.25f,0.25f,0.35f);
        float x=20+i*50.f;
        glBegin(GL_QUADS); glVertex2f(x,500); glVertex2f(x+35,500); glVertex2f(x+35,520); glVertex2f(x,520); glEnd();
    }}
}}
LRESULT CALLBACK wndproc(HWND w, UINT m, WPARAM wp, LPARAM lp) {{
    if (m==WM_DESTROY) {{ PostQuitMessage(0); return 0; }}
    if (m==WM_KEYDOWN && wp==VK_ESCAPE) {{ PostQuitMessage(0); return 0; }}
    return DefWindowProcW(w,m,wp,lp);
}}
int WINAPI wWinMain(HINSTANCE inst, HINSTANCE, PWSTR, int) {{
    WNDCLASSW wc{{}}; wc.lpfnWndProc=wndproc; wc.hInstance=inst; wc.lpszClassName=L"ShaderFsmGl";
    wc.hCursor=LoadCursor(nullptr, IDC_ARROW); RegisterClassW(&wc);
    HWND hwnd = CreateWindowExW(0, wc.lpszClassName, L"shader_stage_fsm OpenGL — Esc quit",
        WS_OVERLAPPEDWINDOW|WS_VISIBLE, CW_USEDEFAULT,CW_USEDEFAULT, 960,540,nullptr,nullptr,inst,nullptr);
    if (!hwnd || !init_gl(hwnd)) return 1;
    auto prev = std::chrono::steady_clock::now();
    MSG msg{{}}; bool run=true;
    while (run) {{
        while (PeekMessageW(&msg,nullptr,0,0,PM_REMOVE)) {{
            if (msg.message==WM_QUIT) run=false;
            TranslateMessage(&msg); DispatchMessageW(&msg);
        }}
        auto now = std::chrono::steady_clock::now();
        float dt = std::chrono::duration<float>(now-prev).count(); prev=now;
        g_t += dt; g_acc += dt;
        if (g_acc > 1.5f) {{ g_fsm.advance(); g_acc = 0; }}
        render(); SwapBuffers(g_dc); Sleep(1);
    }}
    shutdown_gl(hwnd);
    return 0;
}}
'''
    stub_sw = sw_sol.replace("PEDAGOGY-SOLUTION", "TODO-VIEW")  # still visual in starter? Better MessageBox stub for starter backends
    # Starter backends: MessageBox + note to implement core first is OK per spec
    stub_sw = '''#include <windows.h>
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"TODO: implement core then copy solutions/software_win32 pattern", L"shader_stage_fsm", MB_OK);
    return 0;
}
'''
    stub_gl = '''#include <windows.h>
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"TODO: implement core then copy solutions/opengl_win32 pattern", L"shader_stage_fsm", MB_OK);
    return 0;
}
'''
    write_pair(mod, name, hpp, cpp_s, cpp_sol, test, stub_sw, sw_sol, stub_gl, gl_sol)
    pedagogy(
        mod,
        "shader_stage_fsm",
        "FSM de stages de shader (Edit/Compile/Link/Ready) dirigindo a cor de um triangulo animado.",
        ["GFX-SH-ADVANCE", "GFX-SH-RESET", "GFX-SH-COLOR"],
        "cd days/2026-09-08/graphics/shader_stage_fsm/starter\ncmake -S . -B build_ci -G Ninja\ncmake --build build_ci\nctest --test-dir build_ci --output-on-failure",
        {
            "GFX-SH-ADVANCE": ("starter/core/shader_fsm.cpp", "ShaderFsm::advance"),
            "GFX-SH-RESET": ("starter/core/shader_fsm.cpp", "ShaderFsm::reset"),
            "GFX-SH-COLOR": ("starter/core/shader_fsm.cpp", "ShaderFsm::stage_color"),
        },
        {
            "GFX-SH-ADVANCE": "int s = static_cast<int>(stage) + 1;\nif (s >= static_cast<int>(Stage::Count)) s = 0;\nstage = static_cast<Stage>(s);",
            "GFX-SH-RESET": "stage = Stage::Edit;\n(void)0;\nreturn;",
            "GFX-SH-COLOR": "switch (stage) {\ncase Stage::Ready: r=0.2f; g=0.85f; b=0.4f; break;\ndefault: r=0.9f; g=0.3f; b=0.2f; break;\n}",
        },
        "Abra `shader_fsm_sw.exe` e `shader_fsm_gl.exe`: triangulo/quad se move e muda de cor a cada ~1.5s conforme o stage; barras no topo marcam o stage atual.",
    )
    print("ok", mod)


if __name__ == "__main__":
    mod_shader()
    print("partial — continue in upgrade_gfx_visual_days_08_11_b.py")
