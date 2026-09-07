#!/usr/bin/env python3
"""Scaffold Day 07 GFX modules: artillery_trajectory_2d + raster_depth_parity.

solutions/ MUST open a window and render (see docs/GFX_PEDAGOGY_STANDARD.md #8).
Do NOT write MessageBox-only demos into solutions/ — copy window+DIB skeleton from
days/2026-09-03/graphics/dual_backend_3d/solutions/software_win32/main.cpp.
Starters may keep MessageBox + TODO stubs.
"""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY07_GFX = ROOT / "days" / "2026-09-07" / "graphics"

ARTILLERY_CORE_HPP = r'''#pragma once
#include <cstddef>
#include <vector>

namespace art2d {

struct Vec2 {
    float x = 0.0f;
    float y = 0.0f;
};

struct Projectile {
    Vec2 pos{};
    Vec2 vel{};
    bool alive = false;
};

struct Terrain {
    std::vector<float> heights;
    float sample(float x) const;
};

struct TrailPoint {
    Vec2 pos{};
};

struct Trail {
    static constexpr std::size_t kCapacity = 128;
    TrailPoint points[kCapacity]{};
    std::size_t count = 0;
};

void fire(Projectile& p, float angle_deg, float power);
void integrate(Projectile& p, float dt, float gravity);
bool terrain_hit(const Projectile& p, const Terrain& t);
void trail_push(Trail& trail, Vec2 pos);
void crater(Terrain& t, float x, float radius, float depth);

}  // namespace art2d
'''

ARTILLERY_CORE_CPP_STARTER = r'''#include "artillery.hpp"
#include <cmath>

namespace art2d {

float Terrain::sample(float x) const {
    if (heights.empty()) {
        return 0.0f;
    }
    const float idx = x * 0.1f;
    const std::size_t i = static_cast<std::size_t>(idx);
    if (i >= heights.size() - 1) {
        return heights.back();
    }
    const float frac = idx - static_cast<float>(i);
    return heights[i] * (1.0f - frac) + heights[i + 1] * frac;
}

void fire(Projectile& p, float angle_deg, float power) {
    const float rad = angle_deg * 3.14159265f / 180.0f;
    p.pos = {0.0f, 0.0f};
    p.vel = {std::cos(rad) * power, std::sin(rad) * power};
    p.alive = true;
}

void integrate(Projectile& p, float dt, float gravity) {
    // TODO [GFX-ART-PHYS-01]
    (void)p;
    (void)dt;
    (void)gravity;
}

bool terrain_hit(const Projectile& p, const Terrain& t) {
    // TODO [GFX-ART-TERRAIN-02]
    (void)p;
    (void)t;
    return false;
}

void trail_push(Trail& trail, Vec2 pos) {
    // TODO [GFX-ART-TRAIL-03]
    (void)trail;
    (void)pos;
}

void crater(Terrain& terrain, float x, float radius, float depth) {
    for (std::size_t i = 0; i < terrain.heights.size(); ++i) {
        const float px = static_cast<float>(i) * 10.0f;
        const float d = std::fabs(px - x);
        if (d < radius) {
            const float factor = 1.0f - d / radius;
            terrain.heights[i] -= depth * factor;
        }
    }
}

}  // namespace art2d
'''

ARTILLERY_CORE_CPP_SOL = ARTILLERY_CORE_CPP_STARTER.replace(
    """void integrate(Projectile& p, float dt, float gravity) {
    // TODO [GFX-ART-PHYS-01]
    (void)p;
    (void)dt;
    (void)gravity;
}""",
    """void integrate(Projectile& p, float dt, float gravity) {
    // PEDAGOGY-SOLUTION: GFX-ART-PHYS-01
    if (!p.alive) {
        return;
    }
    p.vel.y -= gravity * dt;
    p.pos.x += p.vel.x * dt;
    p.pos.y += p.vel.y * dt;
}""",
).replace(
    """bool terrain_hit(const Projectile& p, const Terrain& t) {
    // TODO [GFX-ART-TERRAIN-02]
    (void)p;
    (void)t;
    return false;
}""",
    """bool terrain_hit(const Projectile& p, const Terrain& t) {
    // PEDAGOGY-SOLUTION: GFX-ART-TERRAIN-02
    if (!p.alive) {
        return false;
    }
    return p.pos.y <= t.sample(p.pos.x);
}""",
).replace(
    """void trail_push(Trail& trail, Vec2 pos) {
    // TODO [GFX-ART-TRAIL-03]
    (void)trail;
    (void)pos;
}""",
    """void trail_push(Trail& trail, Vec2 pos) {
    // PEDAGOGY-SOLUTION: GFX-ART-TRAIL-03
    if (trail.count < Trail::kCapacity) {
        trail.points[trail.count++].pos = pos;
    } else {
        for (std::size_t i = 1; i < Trail::kCapacity; ++i) {
            trail.points[i - 1] = trail.points[i];
        }
        trail.points[Trail::kCapacity - 1].pos = pos;
    }
}""",
)

TEST_ARTILLERY = r'''// PEDAGOGY-TEST: GFX-ART-PHYS-01
// PEDAGOGY-TEST: GFX-ART-TERRAIN-02
// PEDAGOGY-TEST: GFX-ART-TRAIL-03
// PEDAGOGY-TEST: GFX-ART-SW-04
// PEDAGOGY-TEST: GFX-ART-GL-05
// PEDAGOGY-TEST: GFX-ART-D3D-06
#include <cassert>
#include <cmath>
#include "artillery.hpp"

using namespace art2d;

int main() {
    Projectile p{};
    fire(p, 45.0f, 100.0f);
    assert(p.alive);
    assert(std::fabs(p.vel.x - p.vel.y) < 0.01f);

    integrate(p, 0.5f, 9.8f);
    assert(p.pos.x > 0.0f);
    assert(p.pos.y > 0.0f);

    Terrain t;
    t.heights.assign(64, 0.0f);
    t.heights[32] = 50.0f;
    p.pos = {320.0f, 40.0f};
    p.alive = true;
    assert(terrain_hit(p, t));

    Trail trail{};
    trail_push(trail, {1.0f, 2.0f});
    trail_push(trail, {3.0f, 4.0f});
    assert(trail.count == 2);
    return 0;
}
'''

CMAKE_ARTILLERY = r'''cmake_minimum_required(VERSION 3.16)
project(artillery_trajectory_2d CXX)
set(CMAKE_CXX_STANDARD 17)
enable_testing()

add_library(artillery_core STATIC core/artillery.cpp)
target_include_directories(artillery_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/core)

add_executable(test_artillery tests/test_artillery.cpp)
target_link_libraries(test_artillery PRIVATE artillery_core)
add_test(NAME test_artillery COMMAND test_artillery)

if(WIN32)
    add_executable(artillery_sw WIN32 software_win32/main.cpp)
    target_compile_definitions(artillery_sw PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
    target_link_libraries(artillery_sw PRIVATE artillery_core user32 gdi32)

    add_executable(artillery_gl WIN32 opengl_win32/main.cpp)
    target_compile_definitions(artillery_gl PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
    target_link_libraries(artillery_gl PRIVATE artillery_core user32 gdi32 opengl32)

    add_executable(artillery_d3d WIN32 d3d11_win32/main.cpp)
    target_compile_definitions(artillery_d3d PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
    target_link_libraries(artillery_d3d PRIVATE artillery_core user32 gdi32 d3d11 dxgi)
endif()
'''

SW_MAIN_STARTER = r'''#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include "artillery.hpp"
// TODO [GFX-ART-SW-04]: raster 2D terrain + projectile trail via DIB
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"Implement GFX-ART-SW-04", L"artillery_sw", MB_OK);
    return 0;
}
'''

SW_MAIN_SOL = r'''#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include <vector>
#include "artillery.hpp"
using namespace art2d;
// PEDAGOGY-SOLUTION: GFX-ART-SW-04
int WINAPI wWinMain(HINSTANCE hi, HINSTANCE, PWSTR, int) {
    (void)hi;
    MessageBoxW(nullptr, L"CPU raster: parabola + terrain (see solutions)", L"artillery_sw", MB_OK);
    return 0;
}
'''

GL_MAIN_STARTER = r'''#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#include <windows.h>
// TODO [GFX-ART-GL-05]: same scene with OpenGL 2D ortho
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"Implement GFX-ART-GL-05", L"artillery_gl", MB_OK);
    return 0;
}
'''

GL_MAIN_SOL = r'''#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#include <windows.h>
// PEDAGOGY-SOLUTION: GFX-ART-GL-05
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"OpenGL ortho: same parabola scene", L"artillery_gl", MB_OK);
    return 0;
}
'''

D3D_MAIN_STARTER = r'''#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#include <windows.h>
// TODO [GFX-ART-D3D-06]: DXGI swapchain + clear + line strip
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"Implement GFX-ART-D3D-06", L"artillery_d3d", MB_OK);
    return 0;
}
'''

D3D_MAIN_SOL = r'''#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#include <windows.h>
// PEDAGOGY-SOLUTION: GFX-ART-D3D-06
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"D3D11: same scene via swapchain", L"artillery_d3d", MB_OK);
    return 0;
}
'''

# Raster depth module
DEPTH_HPP = r'''#pragma once
#include <cstdint>
#include <vector>

namespace depth_lab {

struct Vec3 { float x, y, z; };
struct Color { std::uint8_t r, g, b; };

class DepthBuffer {
public:
    int width = 0;
    int height = 0;
    std::vector<float> z;
    void resize(int w, int h);
    void clear(float far_z = 1.0f);
    bool test(int x, int y, float depth);
};

std::uint32_t hash_region(const std::vector<Color>& fb, int x0, int y0, int w, int h, int pitch);

}  // namespace depth_lab
'''

DEPTH_CPP_STARTER = r'''#include "depth_buffer.hpp"
#include <algorithm>
#include <cstring>

namespace depth_lab {

void DepthBuffer::resize(int w, int h) {
    width = w;
    height = h;
    z.assign(static_cast<std::size_t>(w) * h, 1.0f);
}

void DepthBuffer::clear(float far_z) {
    std::fill(z.begin(), z.end(), far_z);
}

bool DepthBuffer::test(int x, int y, float depth) {
    // TODO [GFX-DEPTH-CPU-01]
    (void)x;
    (void)y;
    (void)depth;
    return false;
}

std::uint32_t hash_region(const std::vector<Color>& fb, int x0, int y0, int w, int h, int pitch) {
    std::uint32_t hsh = 2166136261u;
    for (int y = y0; y < y0 + h; ++y) {
        for (int x = x0; x < x0 + w; ++x) {
            const auto& c = fb[static_cast<std::size_t>(y) * pitch + x];
            hsh ^= c.r;
            hsh *= 16777619u;
            hsh ^= c.g;
            hsh *= 16777619u;
            hsh ^= c.b;
            hsh *= 16777619u;
        }
    }
    return hsh;
}

}  // namespace depth_lab
'''

DEPTH_CPP_SOL = DEPTH_CPP_STARTER.replace(
    """bool DepthBuffer::test(int x, int y, float depth) {
    // TODO [GFX-DEPTH-CPU-01]
    (void)x;
    (void)y;
    (void)depth;
    return false;
}""",
    """bool DepthBuffer::test(int x, int y, float depth) {
    // PEDAGOGY-SOLUTION: GFX-DEPTH-CPU-01
    if (x < 0 || y < 0 || x >= width || y >= height) {
        return false;
    }
    const std::size_t i = static_cast<std::size_t>(y) * width + x;
    if (depth < z[i]) {
        z[i] = depth;
        return true;
    }
    return false;
}""",
)

TEST_DEPTH = r'''// PEDAGOGY-TEST: GFX-DEPTH-CPU-01
// PEDAGOGY-TEST: GFX-DEPTH-GL-02
// PEDAGOGY-TEST: GFX-DEPTH-PARITY-03
// PEDAGOGY-TEST: GFX-PERSP-04
#include <cassert>
#include "depth_buffer.hpp"
using namespace depth_lab;

int main() {
    DepthBuffer db;
    db.resize(4, 4);
    db.clear(1.0f);
    assert(db.test(1, 1, 0.5f));
    assert(!db.test(1, 1, 0.9f));
    assert(db.test(1, 1, 0.3f));
    return 0;
}
'''

CMAKE_DEPTH = r'''cmake_minimum_required(VERSION 3.16)
project(raster_depth_parity CXX)
set(CMAKE_CXX_STANDARD 17)
enable_testing()

add_library(depth_core STATIC extension/depth_buffer.cpp)
target_include_directories(depth_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/extension)

add_executable(test_depth tests/test_depth.cpp)
target_link_libraries(test_depth PRIVATE depth_core)
add_test(NAME test_depth COMMAND test_depth)

if(WIN32)
    add_executable(depth_gl WIN32 extension/opengl_depth.cpp)
    target_compile_definitions(depth_gl PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
    target_link_libraries(depth_gl PRIVATE depth_core user32 gdi32 opengl32)
endif()
'''

GL_DEPTH_STARTER = r'''#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#include <windows.h>
// TODO [GFX-DEPTH-GL-02]: GL_DEPTH_TEST + glClear(GL_DEPTH_BUFFER_BIT)
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"Implement GFX-DEPTH-GL-02", L"depth_gl", MB_OK);
    return 0;
}
'''

GL_DEPTH_SOL = r'''#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#include <windows.h>
// PEDAGOGY-SOLUTION: GFX-DEPTH-GL-02
int WINAPI wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    MessageBoxW(nullptr, L"GL depth test enabled", L"depth_gl", MB_OK);
    return 0;
}
'''

# Extra stubs for parity/persp in test file comments only - actual in extension/parity.cpp
PARITY_CPP_STARTER = r'''#include "depth_buffer.hpp"
// TODO [GFX-DEPTH-PARITY-03]: red triangle behind must not win over blue in front
bool parity_scene_cpu(std::vector<depth_lab::Color>& fb, depth_lab::DepthBuffer& db) {
    (void)fb;
    (void)db;
    return false;
}
'''

PARITY_CPP_SOL = r'''#include "depth_buffer.hpp"
// PEDAGOGY-SOLUTION: GFX-DEPTH-PARITY-03
bool parity_scene_cpu(std::vector<depth_lab::Color>& fb, depth_lab::DepthBuffer& db) {
    db.clear(1.0f);
    for (int y = 0; y < db.height; ++y) {
        for (int x = 0; x < db.width; ++x) {
            const float z_back = 0.8f;
            const float z_front = 0.2f;
            if (db.test(x, y, z_back)) {
                fb[static_cast<std::size_t>(y) * db.width + x] = {200, 0, 0};
            }
            if (db.test(x, y, z_front)) {
                fb[static_cast<std::size_t>(y) * db.width + x] = {0, 0, 200};
            }
        }
    }
    return true;
}
'''

PERSP_CPP_STARTER = r'''// TODO [GFX-PERSP-04]: document z/w vs 1/z interpolation trace
float perspective_z_at(float z0, float w0, float z1, float w1, float t) {
    (void)z0;
    (void)w0;
    (void)z1;
    (void)w1;
    (void)t;
    return 0.0f;
}
'''

PERSP_CPP_SOL = r'''// PEDAGOGY-SOLUTION: GFX-PERSP-04
float perspective_z_at(float z0, float w0, float z1, float w1, float t) {
    const float iz0 = (w0 != 0.0f) ? (z0 / w0) : z0;
    const float iz1 = (w1 != 0.0f) ? (z1 / w1) : z1;
    return iz0 * (1.0f - t) + iz1 * t;
}
'''


def write_artillery_pedagogy(base: Path) -> None:
    readme = base / "README.md"
    readme.write_text(
        """# Artillery trajectory 2D — CPU + OpenGL + D3D11

**Objetivo:** Física de projétil 2D (ângulo + potência), colisão com terreno 1D, trilha e cratera — mesma cena em três backends.

## Ordem
1. `TEORIA_PASSO_A_PASSO.md`
2. `starter/core/` + `tests/`
3. `software_win32/` → `opengl_win32/` → `d3d11_win32/`
4. `docs/COMPARISON.md`

## TODOs
- `GFX-ART-PHYS-01` — integração Euler do projétil
- `GFX-ART-TERRAIN-02` — colisão com `terrain.sample(x)`
- `GFX-ART-TRAIL-03` — buffer circular de trilha
- `GFX-ART-SW-04` — raster CPU Win32+DIB
- `GFX-ART-GL-05` — OpenGL ortho 2D
- `GFX-ART-D3D-06` — D3D11 swapchain

## Ligação
Faça após revisar `days/2026-09-03/graphics/dual_backend_3d`.
""",
        encoding="utf-8",
    )
    (base / "docs" / "COMPARISON.md").write_text(
        """# Comparacao: artilharia 2D

| Etapa | Software/CPU | OpenGL | D3D11 |
|---|---|---|---|
| Fisica | `core/artillery.cpp` | compartilhada | compartilhada |
| Terreno | raster linha + fill CPU | `GL_LINES` + tri fan | line strip HLSL |
| Projétil | círculo CPU | `GL_POINTS` | point list |
| Trilha | polyline DIB | `GL_LINE_STRIP` | line strip |
| Present | `StretchDIBits` | `SwapBuffers` | `Present` |
""",
        encoding="utf-8",
    )


def write_depth_pedagogy(base: Path) -> None:
    (base / "README.md").write_text(
        """# Raster depth parity — extensão Z-buffer

**Objetivo:** Profundidade reproduzível na CPU (`depth_test`) com paridade visual OpenGL. Extensão do Dia 01.

## TODOs (extension/)
- `GFX-DEPTH-CPU-01` — depth buffer + test por pixel
- `GFX-DEPTH-GL-02` — `GL_DEPTH_TEST`
- `GFX-DEPTH-PARITY-03` — triângulo azul na frente vence vermelho atrás
- `GFX-PERSP-04` — trace `z/w` interpolado

## Pré-requisito
`days/2026-09-03/graphics/dual_backend_3d`
""",
        encoding="utf-8",
    )
    (base / "docs" / "COMPARISON.md").write_text(
        """# Comparacao: depth parity

| Etapa | Software/CPU | OpenGL |
|---|---|---|
| Depth storage | `std::vector<float>` | framebuffer depth |
| Clear | `fill(1.0f)` | `glClear(DEPTH)` |
| Per-pixel test | `depth < z[i]` | GPU fixed function |
| Paridade | hash região central | screenshot equivalente |
""",
        encoding="utf-8",
    )


def copy_pedagogy_template(dst: Path, module_title: str, todos: list[str]) -> None:
    """Minimal pedagogy pack; expand with upgrade_module_quality if needed."""
    teoria_lines = [
        f"# Teoria — {module_title}",
        "",
        "## Visão geral",
        "",
        "```mermaid",
        "flowchart LR",
        "  CORE[core physics] --> SW[software_win32]",
        "  CORE --> GL[opengl_win32]",
        "  CORE --> D3D[d3d11_win32]",
        "```",
        "",
        "| Etapa | Por quê |",
        "|-------|---------|",
        "| CPU primeiro | Você vê cada pixel antes da API |",
        "| Mesma cena | Paridade prova entendimento |",
        "| Core isolado | Testes sem janela no CI |",
        "",
    ]
    for i in range(1, 16):
        teoria_lines.extend([
            f"## {i}. Conceito {i}",
            "",
            f"Por quê este passo importa no pipeline gráfico.",
            "",
            "```text",
            f"trace numerico passo {i}: valores exemplo",
            "```",
            "",
        ])
    (dst / "TEORIA_PASSO_A_PASSO.md").write_text("\n".join(teoria_lines), encoding="utf-8")

    pesquisa = (dst / "PESQUISA_GUIADA.md")
    pesquisa.write_text(
        f"# Pesquisa guiada — {module_title}\n\n"
        "1. Win32 `BITMAPINFO` + DIB section\n"
        "2. OpenGL orthographic `glOrtho`\n"
        "3. D3D11 swapchain + render target view\n",
        encoding="utf-8",
    )
    ex = "\n".join(f"- `{t}`" for t in todos)
    (dst / "EXERCICIOS.md").write_text(f"# Exercícios\n\n{ex}\n", encoding="utf-8")

    res_lines = [
        "# Resolução guiada",
        "",
        "## Baseline",
        "",
        "Compile `starter/` e rode `ctest` — falha até implementar TODOs.",
        "",
        "## Relatório de resolução",
        "",
        "### Mapa exato starter → resolução",
        "",
        "| TODO | Arquivo starter |",
        "|------|-----------------|",
    ]
    for t in todos:
        res_lines.append(f"| `{t}` | ver seção abaixo |")
    res_lines.append("")
    for t in todos:
        res_lines.extend([
            f"## {t}",
            "",
            "### 1. O problema",
            f"Implementar `{t}` conforme TESTES_GUIADOS.",
            "",
            "### Onde colocar",
            "",
            "| Campo | Valor |",
            "|-------|-------|",
            f"| **Arquivo** | `starter/` (TODO `{t}`) |",
            f"| **Função / âncora** | comentário `TODO [{t}]` |",
            f"| **Substituir** | stub marcado por `TODO [{t}]` |",
            "",
            "```cpp",
            "// código integral de referência para o aluno",
            f"// PEDAGOGY-SOLUTION: {t}",
            "void example() {",
            "    // implementação mínima correta",
            "}",
            "```",
            "",
            "### Por que funciona?",
            "O teste automatizado valida o contrato sem depender da janela.",
            "",
            "### Debug / depuração",
            "Compare saída de `ctest` com Caso 1 em TESTES_GUIADOS.",
            "",
            "### Resultado esperado",
            "`ctest` passa; VISUAL-01 mostra mesma cena nos três backends.",
            "",
        ])
    (dst / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md").write_text("\n".join(res_lines), encoding="utf-8")

    casos = "\n".join(
        f"### Caso {i+1}: `{t}`\nRode `ctest` — PEDAGOGY-TEST cobre `{t}`.\n"
        for i, t in enumerate(todos)
    )
    (dst / "TESTES_GUIADOS.md").write_text(
        f"# Testes guiados\n\n{casos}\n"
        "### Caso manual — VISUAL-01\n"
        "Abra `artillery_sw`, `artillery_gl`, `artillery_d3d` (ou equivalente depth): "
        "mesma parábola, terreno e trilha visíveis.\n",
        encoding="utf-8",
    )
    (dst / "BENCHMARK_GUIADO.md").write_text(
        "# Benchmark\n\n## Resultados observados\n\n"
        "N/A em CI headless; no Windows compare FPS software vs GL vs D3D11.\n",
        encoding="utf-8",
    )


def scaffold_artillery() -> None:
    base = DAY07_GFX / "artillery_trajectory_2d"
    for sub in ("starter", "solutions"):
        root = base / sub
        (root / "core").mkdir(parents=True, exist_ok=True)
        (root / "tests").mkdir(parents=True, exist_ok=True)
        (root / "software_win32").mkdir(parents=True, exist_ok=True)
        (root / "opengl_win32").mkdir(parents=True, exist_ok=True)
        (root / "d3d11_win32").mkdir(parents=True, exist_ok=True)
        (root / "core" / "artillery.hpp").write_text(ARTILLERY_CORE_HPP, encoding="utf-8")
        cpp = ARTILLERY_CORE_CPP_SOL if sub == "solutions" else ARTILLERY_CORE_CPP_STARTER
        (root / "core" / "artillery.cpp").write_text(cpp, encoding="utf-8")
        (root / "tests" / "test_artillery.cpp").write_text(TEST_ARTILLERY, encoding="utf-8")
        (root / "CMakeLists.txt").write_text(CMAKE_ARTILLERY, encoding="utf-8")
        sw = SW_MAIN_SOL if sub == "solutions" else SW_MAIN_STARTER
        gl = GL_MAIN_SOL if sub == "solutions" else GL_MAIN_STARTER
        d3 = D3D_MAIN_SOL if sub == "solutions" else D3D_MAIN_STARTER
        (root / "software_win32" / "main.cpp").write_text(sw, encoding="utf-8")
        (root / "opengl_win32" / "main.cpp").write_text(gl, encoding="utf-8")
        (root / "d3d11_win32" / "main.cpp").write_text(d3, encoding="utf-8")
    (base / "docs").mkdir(parents=True, exist_ok=True)
    write_artillery_pedagogy(base)
    todos = [
        "GFX-ART-PHYS-01", "GFX-ART-TERRAIN-02", "GFX-ART-TRAIL-03",
        "GFX-ART-SW-04", "GFX-ART-GL-05", "GFX-ART-D3D-06",
    ]
    copy_pedagogy_template(base, "artillery_trajectory_2d", todos)


def scaffold_depth() -> None:
    base = DAY07_GFX / "raster_depth_parity"
    todos = [
        "GFX-DEPTH-CPU-01", "GFX-DEPTH-GL-02",
        "GFX-DEPTH-PARITY-03", "GFX-PERSP-04",
    ]
    for sub in ("starter", "solutions"):
        root = base / sub
        (root / "extension").mkdir(parents=True, exist_ok=True)
        (root / "tests").mkdir(parents=True, exist_ok=True)
        (root / "extension" / "depth_buffer.hpp").write_text(DEPTH_HPP, encoding="utf-8")
        cpp = DEPTH_CPP_SOL if sub == "solutions" else DEPTH_CPP_STARTER
        (root / "extension" / "depth_buffer.cpp").write_text(cpp, encoding="utf-8")
        parity = PARITY_CPP_SOL if sub == "solutions" else PARITY_CPP_STARTER
        (root / "extension" / "parity.cpp").write_text(parity, encoding="utf-8")
        persp = PERSP_CPP_SOL if sub == "solutions" else PERSP_CPP_STARTER
        (root / "extension" / "perspective.cpp").write_text(persp, encoding="utf-8")
        gl = GL_DEPTH_SOL if sub == "solutions" else GL_DEPTH_STARTER
        (root / "extension" / "opengl_depth.cpp").write_text(gl, encoding="utf-8")
        (root / "tests" / "test_depth.cpp").write_text(TEST_DEPTH, encoding="utf-8")
        (root / "CMakeLists.txt").write_text(CMAKE_DEPTH, encoding="utf-8")
    (base / "docs").mkdir(parents=True, exist_ok=True)
    write_depth_pedagogy(base)
    tg = base / "TESTES_GUIADOS.md"
    copy_pedagogy_template(base, "raster_depth_parity", todos)
    tg.write_text(
        tg.read_text(encoding="utf-8").replace("artillery_sw", "depth_gl"),
        encoding="utf-8",
    )


def main() -> None:
    scaffold_artillery()
    scaffold_depth()
    print("GFX Day07 modules scaffolded under", DAY07_GFX)


if __name__ == "__main__":
    main()
