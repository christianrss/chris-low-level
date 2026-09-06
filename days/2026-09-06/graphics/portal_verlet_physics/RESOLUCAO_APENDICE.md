# Portal Verlet — apêndice da resolução guiada

> Continuação de `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` (`GFX-PORTAL-05` e `GFX-PORTAL-06`).
> Trabalhe em `starter/`. APIs reais: `sphere_portal.hpp`, `render_gl.hpp`, `main_opengl.cpp`.

---

## GFX-PORTAL-05 — Esfera atravessa portal

### 1. O problema

Em `starter/src/sphere_portal.cpp`:

```cpp
bool sphere_crosses_portal_plane(const Sphere& sphere, const PortalFrame& frame, float portal_radius) {
    // TODO [GFX-PORTAL-05]
    return false;
}

bool try_sphere_teleport(Sphere& sphere, const PortalPair& pair, bool at_portal_a, float portal_radius) {
    // TODO [GFX-PORTAL-05]
    return false;
}
```

`sphere_step` já pode existir no gabarito; no starter o foco do TODO é cruzar plano + teleportar. Sem isso, `test_sphere_portal` falha no primeiro `assert(sphere_crosses_portal_plane(...))`.

### 2. O algoritmo

```text
signed_distance(point, frame) =
  dot(point - frame.position, normalize(frame.forward))

inside_disc(point, frame, R):
  local = transform_point(inverse_rigid(make_frame_matrix(frame)), point)
  return sqrt(local.x² + local.y²) ≤ R

crosses:
  dist = signed_distance(center, frame)
  se dist + radius < 0 → false
  se não inside_disc → false
  return dist ≤ radius

teleport(at_portal_a):
  se !crosses(src) → false
  center = portal_transport_position(pair, at_portal_a, center)
  velocity = portal_transport_velocity(pair, at_portal_a, velocity)
  return true
```

### 3. Código

Alinhe com `solutions/src/sphere_portal.cpp`. O teste oficial só exige as duas funções abaixo; `sphere_step` entra no `GFX-PORTAL-06` (demo).

```cpp
#include "sphere_portal.hpp"

static float signed_distance_to_plane(Vec3 point, const PortalFrame& frame) {
    return vec3_dot(vec3_sub(point, frame.position), vec3_normalize(frame.forward));
}

static bool inside_portal_disc(Vec3 point, const PortalFrame& frame, float portal_radius) {
    Vec3 local = mat4_transform_point(mat4_inverse_rigid(make_frame_matrix(frame)), point);
    return std::sqrt(local.x * local.x + local.y * local.y) <= portal_radius;
}

bool sphere_crosses_portal_plane(const Sphere& sphere, const PortalFrame& frame, float portal_radius) {
    float dist = signed_distance_to_plane(sphere.center, frame);
    if (dist + sphere.radius < 0.f) return false;
    if (!inside_portal_disc(sphere.center, frame, portal_radius)) return false;
    return dist <= sphere.radius;
}

bool try_sphere_teleport(Sphere& sphere, const PortalPair& pair, bool at_portal_a, float portal_radius) {
    const PortalFrame& src = at_portal_a ? pair.portal_a : pair.portal_b;
    if (!sphere_crosses_portal_plane(sphere, src, portal_radius)) {
        return false;
    }
    sphere.center = portal_transport_position(pair, at_portal_a, sphere.center);
    sphere.velocity = portal_transport_velocity(pair, at_portal_a, sphere.velocity);
    return true;
}
```

Para a demo (06): declare `void sphere_step(Sphere&, Vec3, float, float floor_y = 0.f);` em `sphere_portal.hpp` e implemente como em `solutions/src/sphere_portal.cpp` (integra velocity + bounce no chão).

### 4. Entenda

- `dist` negativo = centro atrás do portal (lado “de trás” do normal).
- Janela `[-radius, +radius]` aproxima o momento em que a esfera toca o plano.
- Disco em XY local impede teleporte lateral fora do quad.
- Trace: `(0,0,-0.2)` + r=0.3 → z'≈10.2, vz'≈−4.

### 5. Verificação

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\graphics\portal_verlet_physics\starter
cmake --build build --config Release
.\build\Release\test_sphere_portal.exe
```

```text
OK sphere portal
```

---

## GFX-PORTAL-06 — Demo OpenGL + stencil 1 nível (obrigatória)

### 1. O problema

`starter/src/render_gl.cpp` retorna `false` em `portal_gl_init`; `starter/src/main_opengl.cpp` só mostra MessageBox. Sem WGL + stencil, não há Caso manual 6.

Também complete em `starter/src/math.cpp` (usados pela câmera/demo, presentes em `solutions/src/math.cpp`):

- `mat4_perspective`
- `mat4_look_at`

### 2. O algoritmo — um frame

```text
portal_gl_init:
  GetDC → ChoosePixelFormat com cStencilBits=8 → SetPixelFormat
  wglCreateContext → wglMakeCurrent
  glEnable(DEPTH_TEST), BLEND

portal_gl_render_frame:
  stencil_passes = 0
  Clear COLOR|DEPTH|STENCIL
  setup proj/view(camera); draw_scene_content(sem frames)
  render_through_portal(A); render_through_portal(B)
  desenhar quads A/B
  SwapBuffers

render_through_portal(from_a):
  Enable STENCIL; Clear STENCIL
  ColorMask/DepthMask FALSE
  StencilFunc ALWAYS,1; Op REPLACE; draw portal quad
  ColorMask/DepthMask TRUE
  StencilFunc EQUAL,1; Op KEEP
  view = mirror_camera_through_portal(...)
  draw_scene_content(sem frames)
  Disable STENCIL; ++stencil_passes

main loop:
  PeekMessage → input WASD/mouse/Space
  verlet_step; sphere_step; try_sphere_teleport A senão B
  portal_gl_render_frame
```

### 3. Código — núcleos (espelhe `solutions/src/`)

**WGL init (trecho crítico)** em `portal_gl_init`:

```cpp
PIXELFORMATDESCRIPTOR pfd{};
pfd.nSize = sizeof(pfd);
pfd.nVersion = 1;
pfd.dwFlags = PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL | PFD_DOUBLEBUFFER;
pfd.iPixelType = PFD_TYPE_RGBA;
pfd.cColorBits = 32;
pfd.cDepthBits = 24;
pfd.cStencilBits = 8;  // obrigatório — sem isto não há máscara de portal
```

**Stencil pass** (`render_through_portal`):

```cpp
glEnable(GL_STENCIL_TEST);
glStencilMask(0xFF);
glClear(GL_STENCIL_BUFFER_BIT);

glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE);
glDepthMask(GL_FALSE);
glStencilFunc(GL_ALWAYS, 1, 0xFF);
glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE);
setup_projection(aspect);
setup_view(camera);
draw_portal_quad(src, scene.portal_radius, 1.f, 1.f, 1.f);

glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE);
glDepthMask(GL_TRUE);
glStencilFunc(GL_EQUAL, 1, 0xFF);
glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP);

const Camera mirrored = mirror_camera_through_portal(camera, scene.portals, from_a);
setup_projection(aspect);
setup_view(mirrored);
draw_scene_content(scene, false);

glDisable(GL_STENCIL_TEST);
++ctx.stencil_passes;
```

**Câmera espelhada** (`mirror_camera_through_portal`):

```cpp
Camera out = camera;
out.eye = portal_transport_position(pair, from_a, camera.eye);
Vec3 f = camera_forward(camera);
Vec3 target = vec3_add(camera.eye, vec3_scale(f, 3.f));
Vec3 mirrored_target = portal_transport_position(pair, from_a, target);
Vec3 new_f = vec3_normalize(vec3_sub(mirrored_target, out.eye));
out.yaw = std::atan2(new_f.x, new_f.z);
out.pitch = std::asin(std::clamp(new_f.y, -1.f, 1.f));
return out;
```

**Simulação no loop** (`main_opengl.cpp` — estrutura do gabarito):

```cpp
void simulate(float dt) {
    verlet_step(g_scene.rope, {0.f, -9.8f, 0.f}, dt, 6);
    sphere_step(g_scene.sphere, {0.f, -9.8f, 0.f}, dt, 0.f);
    if (!try_sphere_teleport(g_scene.sphere, g_scene.portals, true, g_scene.portal_radius)) {
        try_sphere_teleport(g_scene.sphere, g_scene.portals, false, g_scene.portal_radius);
    }
}
```

Cena default do gabarito: portais em `(0,2,-4)` / `(0,2,4)` face a face; corda em x=2; esfera em `(0,1.5,2)`.

Para o restante (draw_floor, draw_rope, draw_sphere, WinMain completo): copie estruturalmente de `solutions/src/render_gl.cpp` e `solutions/src/main_opengl.cpp` **depois** de entender o stencil — o volume de fixed-function GL não cabe aqui linha a linha sem virar filler.

### 4. Entenda

- Passo A (máscara): escreve `1` só nos pixels do quad; cor/depth off.
- Passo B (conteúdo): redesenha o mundo com câmera no “outro lado”, só onde stencil==1.
- 1 nível: não reabre stencil dentro da vista espelhada — sem portal-recursivo infinito.
- `stencil_passes` deve ir a 2 por frame (A e B).

### 5. Verificação — Caso manual (obrigatório)

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\graphics\portal_verlet_physics\solutions
cmake -S . -B build-demo -A x64 -DPORTAL_OPENGL=ON
cmake --build build-demo --config Release
.\build-demo\Release\portal_demo.exe
```

Checklist visual:

1. Janela 1280×720 abre (não MessageBox de starter).
2. Chão/paredes coloridas; corda amarela; esfera laranja.
3. Quad azul e laranja; **através** deles vê-se a sala (não só a cor do quad).
4. Space/clique: esfera atravessa e reaparece no outro portal.
5. Esc fecha.

Se WGL falhar: MessageBox `"WGL init failed (need stencil buffer)."` → driver/pixel format sem stencil.

Starter equivalente: implemente 06 e construa o `portal_demo` do `starter/CMakeLists.txt` se `PORTAL_OPENGL` estiver ligado (espelhe a opção do solutions).

---

## Mapa de consistência auditada

| ID | starter | solutions |
|----|---------|-----------|
| 01 | `src/math.cpp` | `src/math.cpp` |
| 02–03 | `src/portal.cpp` | `src/portal.cpp` |
| 04 | `src/verlet.cpp` | `src/verlet.cpp` |
| 05 | `src/sphere_portal.cpp` | `src/sphere_portal.cpp` |
| 06 | `src/render_gl.cpp`, `src/main_opengl.cpp` | mesmos |

Testes: `starter/tests/test_{portal_transform,verlet_rope,sphere_portal}.cpp`. Demo: `PEDAGOGY-TEST: GFX-PORTAL-06` em `main_opengl.cpp`.

---

## Relatório de resolução

### O que foi validado

- TODOs `GFX-PORTAL-01..06` no starter (01–04 no arquivo principal; 05–06 aqui).
- CPU: `OK portal transform`, `OK verlet rope`, `OK sphere portal`.
- Visual: `portal_demo.exe` com stencil 1 nível — Caso manual 6.

### Armadilhas encontradas

- `cStencilBits=0` → init “ok” em alguns setups mas máscara inútil / falha WGL.
- Desenhar conteúdo espelhado sem `GL_EQUAL` → cena duplicada na tela toda.
- Teleporte só em A e nunca em B no `simulate`.
- Usar `transform_point` na velocity da esfera.

### Depuração e saída esperada

- **CPU:** três executáveis de teste com linha `OK …`.
- **GPU:** checklist acima; `ctx.stencil_passes == 2` por frame se instrumentar.
- **Gabarito:** `ctest` em `solutions/build` 100%; demo em `build-demo`.

### Próximo passo sugerido

Refazer 03 e 05 sem olhar o código; depois medir FPS stencil ON vs OFF em `BENCHMARK_GUIADO.md`.
