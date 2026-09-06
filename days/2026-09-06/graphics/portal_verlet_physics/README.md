# Ordem de estudo deste módulo

1. Leia `TEORIA_PASSO_A_PASSO.md` (traces Mat4 → portal → Verlet → stencil).
2. Abra `starter/src/` e localize `TODO [GFX-PORTAL-01..06]`.
3. Siga `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` (01–04) e `RESOLUCAO_APENDICE.md` (05–06).
4. Compile/teste após cada TODO; rode o **Caso manual** da demo.
5. Só então compare com `solutions/`.

---

# Treino Low-Level Graphics — 2026-09-06 — Portal Verlet Physics

Lab: **Mat4 column-major**, **par de portais A↔B**, **corda Verlet**, **teleporte de esfera**, **demo OpenGL WGL com stencil 1 nível** (`portal_demo.exe`).

## Estrutura

| Pasta / arquivo | Papel |
|-----------------|-------|
| `starter/src/` | TODOs: `math`, `portal`, `verlet`, `sphere_portal`, `render_gl`, `main_opengl` |
| `starter/tests/` | `test_portal_transform`, `test_verlet_rope`, `test_sphere_portal` |
| `solutions/src/` | Gabarito com `PEDAGOGY-SOLUTION` |
| Headers | `math.hpp`, `portal.hpp`, `verlet.hpp`, `sphere_portal.hpp`, `render_gl.hpp` |

## TODOs auditáveis

| ID | Tópico |
|----|--------|
| `GFX-PORTAL-01` | `mat4_inverse_rigid`, `mat4_transform_point/direction` |
| `GFX-PORTAL-02` | `make_frame_matrix`, `make_portal_pair` |
| `GFX-PORTAL-03` | `portal_transport_position/velocity` |
| `GFX-PORTAL-04` | `verlet_step` |
| `GFX-PORTAL-05` | `sphere_crosses_portal_plane`, `try_sphere_teleport` |
| `GFX-PORTAL-06` | WGL + stencil 1 nível + `portal_demo.exe` (**visual obrigatório**) |

## Pré-requisitos

- CMake 3.16+, C++17, MSVC (demo OpenGL: Windows + `opengl32`)

## Build starter (esperado FAIL até preencher TODOs)

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\graphics\portal_verlet_physics\starter
cmake -S . -B build -A x64
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

## Build gabarito CPU (esperado PASS)

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\graphics\portal_verlet_physics\solutions
cmake -S . -B build -A x64
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

Saídas: `OK portal transform`, `OK verlet rope`, `OK sphere portal`.

## Demo visual (manual — Caso 6)

```powershell
cmake -S . -B build-demo -A x64 -DPORTAL_OPENGL=ON
cmake --build build-demo --config Release
.\build-demo\Release\portal_demo.exe
```

Controles: WASD, mouse look, Space/clique arremessa esfera, Esc sai.

## O que os testes cobrem

| Caso | PEDAGOGY-TEST | Comportamento |
|------|---------------|---------------|
| 1–3 | GFX-PORTAL-01..03 | Mat4, frames, transporte z=8 + round-trip |
| 4 | GFX-PORTAL-04 | Corda: comprimento + queda + endpoints |
| 5 | GFX-PORTAL-05 | Esfera teleporta; fora do disco não |
| 6 | GFX-PORTAL-06 | `portal_demo.exe` — stencil (manual) |

## Portar para projects/

| Item | Detalhe |
|------|---------|
| O que levar | `math`/`portal`/`verlet` + stub de render |
| Milestone | graphics — portal physics |
| Commit sugerido | `feat(graphics): port portal Mat4+Verlet from day lab` |
