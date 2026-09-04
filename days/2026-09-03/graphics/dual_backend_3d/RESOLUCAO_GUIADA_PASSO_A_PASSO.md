# Resolução guiada auditada — dual_backend_3d

> **Regra deste módulo:** cada etapa abaixo corresponde a um TODO que existe no `starter/` ou a um experimento explicitamente identificado como observação. A `solutions/` contém a implementação final de todos os TODOs. Não é necessário inventar APIs ou procurar uma “função equivalente”.

## 0. Estrutura que você realmente vai editar

```text
starter/
├── CMakeLists.txt
├── common/
│   ├── engine.hpp
│   └── engine.cpp
├── software_win32/
│   └── main.cpp
├── opengl_win32/
│   └── main.cpp
└── tests/
    └── core_tests.cpp
```

Os TODOs auditados são:

```text
GFX-RASTER-01   starter/software_win32/main.cpp::rasterize_triangle
GFX-LAMBERT-01  starter/opengl_win32/main.cpp::fragment_shader_source
GFX-CULL-01     starter/common/engine.cpp::screen_triangle_front_facing
GFX-CULL-02     starter/software_win32/main.cpp::draw_cube
GFX-CULL-03     starter/opengl_win32/main.cpp::render_scene
GFX-CAMERA-01   starter/common/engine.cpp::camera_forward
GFX-CAMERA-02   starter/common/engine.cpp::camera_right
GFX-CAMERA-03   starter/common/engine.cpp::look_at
GFX-CAMERA-04   software/opengl `update_camera_keyboard`
GFX-CAMERA-05   software/opengl `WM_MOUSEMOVE`
```

## 1. Faça o baseline do starter

No Windows, a partir da pasta `dual_backend_3d`:

```bat
rmdir /s /q build-starter 2>nul
cmake -S starter -B build-starter -A x64
cmake --build build-starter --config Debug
ctest --test-dir build-starter -C Debug --output-on-failure
```

O **build deve passar**, mas o teste portátil deve falhar inicialmente em `test_camera_yaw_changes_forward_direction`. Isso é intencional: o starter compila, mas os TODOs avançados ainda não foram implementados.

Para estudar primeiro apenas rasterização/Lambert no Windows, você pode abrir os dois executáveis mesmo com esse teste pendente. Depois do exercício de câmera, o CTest deve ficar 100% verde.

---

# Parte A — entender o pipeline sem editar código

## 2. Rastreie um vértice de verdade

Abra:

```text
starter/software_win32/main.cpp
```

Localize exatamente:

```cpp
bool project_vertex(...)
```

Coloque breakpoints nestas duas linhas:

```cpp
const Vec4 world = model * Vec4{position.x, position.y, position.z, 1.0f};
const Vec4 clip = view_projection * world;
```

Depois avance até:

```cpp
const float inverse_w = 1.0f / clip.w;
const float ndc_x = clip.x * inverse_w;
const float ndc_y = clip.y * inverse_w;
const float ndc_z = clip.z * inverse_w;
```

Registre no caderno:

```text
local = (...)
world = (...)
clip  = (...)
NDC   = (...)
screen= (...)
```

Essa etapa é apenas observação; não existe TODO correspondente porque `project_vertex` já está implementado para servir de referência ao restante do laboratório.

---

# Parte B — rasterizador software

## 3. TODO `GFX-RASTER-01`: implemente `rasterize_triangle`

Abra:

```text
starter/software_win32/main.cpp
```

Localize:

```cpp
void rasterize_triangle(
```

Apague apenas o corpo temporário com `(void)...`. Não altere assinatura, `ScreenVertex`, `Framebuffer` ou `edge()`.

### 3.1 Área orientada e degeneração

Primeiro escreva:

```cpp
const float area = edge(a.x, a.y, b.x, b.y, c.x, c.y);
if (std::fabs(area) < 1.0e-6f) {
    return;
}
```

Por que: barycentrics dividem por `area`. Um triângulo degenerado teria divisão por valor quase zero.

### 3.2 Bounding box

Logo abaixo adicione:

```cpp
const float min_x_f = std::min({a.x, b.x, c.x});
const float max_x_f = std::max({a.x, b.x, c.x});
const float min_y_f = std::min({a.y, b.y, c.y});
const float max_y_f = std::max({a.y, b.y, c.y});

const int min_x = std::max(0, static_cast<int>(std::floor(min_x_f)));
const int max_x = std::min(
    framebuffer.width - 1,
    static_cast<int>(std::ceil(max_x_f)));
const int min_y = std::max(0, static_cast<int>(std::floor(min_y_f)));
const int max_y = std::min(
    framebuffer.height - 1,
    static_cast<int>(std::ceil(max_y_f)));
```

Não percorra a tela inteira: apenas pixels que podem estar dentro do triângulo.

### 3.3 Normal e Lambert por face

Adicione:

```cpp
const Vec3 normal = normalize(cross(b.world - a.world, c.world - a.world));
const Vec3 light_direction = normalize(Vec3{-0.4f, 0.8f, 0.6f});
const float diffuse = std::max(0.0f, dot(normal, light_direction));
const float light = 0.20f + 0.80f * diffuse;
const std::uint32_t packed_color = rgb(base_color, light);
```

A parte `0.20` é ambiente didática; `0.80*diffuse` é Lambert.

### 3.4 Varredura de pixels

Agora crie os loops:

```cpp
for (int y = min_y; y <= max_y; ++y) {
    for (int x = min_x; x <= max_x; ++x) {
        const float sample_x = static_cast<float>(x) + 0.5f;
        const float sample_y = static_cast<float>(y) + 0.5f;
```

O `+0.5` amostra o centro do pixel.

### 3.5 Barycentrics

Dentro do loop:

```cpp
const float w0 = edge(b.x, b.y, c.x, c.y, sample_x, sample_y) / area;
const float w1 = edge(c.x, c.y, a.x, a.y, sample_x, sample_y) / area;
const float w2 = 1.0f - w0 - w1;

if (w0 < 0.0f || w1 < 0.0f || w2 < 0.0f) {
    continue;
}
```

Se quiser depurar um pixel, observe `w0+w1+w2`: deve ser aproximadamente `1.0`.

### 3.6 Profundidade e depth test

Ainda dentro do loop:

```cpp
const float depth = w0 * a.z + w1 * b.z + w2 * c.z;
if (depth < 0.0f || depth > 1.0f) {
    continue;
}

const std::size_t index =
    static_cast<std::size_t>(y) * framebuffer.width + x;

if (depth < framebuffer.depth[index]) {
    framebuffer.depth[index] = depth;
    framebuffer.pixels[index] = packed_color;
}
```

Feche os dois loops e a função.

### 3.7 Build intermediário

```bat
cmake --build build-starter --config Debug
build-starter\Debug\software_renderer.exe
```

Resultado esperado: você deve ver a cena 3D preenchida, com oclusão por depth buffer e iluminação por face. Se só aparecer fundo, coloque breakpoint em `rasterize_triangle` e confirme `area`, bounding box e `visible[]`.

---

# Parte C — Lambert no OpenGL

## 4. TODO `GFX-LAMBERT-01`

Abra:

```text
starter/opengl_win32/main.cpp
```

Localize a string:

```cpp
const char* fragment_shader_source = R"GLSL(
```

Dentro de `void main()` substitua apenas o TODO por:

```glsl
vec3 normal = normalize(v_normal);
vec3 light_direction = normalize(vec3(-0.4, 0.8, 0.6));
float diffuse = max(dot(normal, light_direction), 0.0);
float lighting = 0.2 + 0.8 * diffuse;
gl_FragColor = vec4(u_color * lighting, 1.0);
```

Compile:

```bat
cmake --build build-starter --config Debug
build-starter\Debug\opengl_renderer.exe
```

Se aparecer `Shader compile error`, leia a mensagem da `MessageBox`; não tente corrigir “no escuro”.

Compare a operação central:

```text
CPU:  dot(normal, light_direction)
GLSL: dot(normal, light_direction)
```

---

# Parte D — física e animação: observação guiada com símbolos exatos

## 5. Física: `physics_step`

Abra:

```text
starter/common/engine.cpp
```

Localize exatamente:

```cpp
void physics_step(SceneState& scene, float delta_time)
```

As linhas que implementam Euler semi-implícito são:

```cpp
scene.body.velocity.y += kGravity * delta_time;
scene.body.position =
    scene.body.position + scene.body.velocity * delta_time;
```

Coloque breakpoint na primeira linha. Observe:

```text
scene.body.position.y
scene.body.velocity.y
delta_time
```

Para o experimento, altere temporariamente:

```cpp
constexpr float kGravity = -9.81f;
```

para:

```cpp
constexpr float kGravity = -4.905f;
```

Compile, observe a queda e **restaure -9.81f**. Depois faça o mesmo com:

```cpp
constexpr float kRestitution = 0.72f;
```

Essa etapa não altera a solution final: é um experimento controlado sobre código já implementado.

## 6. Animação: `build_draw_list`

No mesmo arquivo localize:

```cpp
std::vector<DrawItem> build_draw_list(const SceneState& scene)
```

Os símbolos exatos são:

```cpp
const Mat4 shoulder = ...;
const Mat4 upper_arm = shoulder * ...;
const Mat4 elbow = shoulder * ...;
const Mat4 forearm = elbow * ...;
const Mat4 hand = elbow * ...;
```

Coloque breakpoint na construção de `elbow` e depois `hand`. A pergunta a responder é: **qual matriz pai aparece do lado esquerdo da multiplicação?**

---

# Parte E — back-face culling nos dois backends

## 7. TODO `GFX-CULL-01`: regra portátil de winding

Abra:

```text
starter/common/engine.cpp
```

Localize:

```cpp
bool screen_triangle_front_facing(float signed_area)
```

Substitua o placeholder por:

```cpp
return signed_area > 0.0f;
```

Por que `> 0` aqui? `project_vertex` inverte Y ao passar de NDC para pixels de tela, e a função `edge()` deste laboratório usa uma convenção de sinal específica. O teste `test_screen_winding_helper` torna essa convenção explícita.

## 8. TODO `GFX-CULL-02`: software renderer

Abra:

```text
starter/software_win32/main.cpp
```

Dentro de `draw_cube`, localize o comentário `GFX-CULL-02` imediatamente antes de `rasterize_triangle`.

Insira:

```cpp
const float signed_area = edge(
    vertices[i0].x, vertices[i0].y,
    vertices[i1].x, vertices[i1].y,
    vertices[i2].x, vertices[i2].y);

if (!screen_triangle_front_facing(signed_area)) {
    continue;
}
```

## 9. TODO `GFX-CULL-03`: OpenGL

Abra:

```text
starter/opengl_win32/main.cpp
```

Em `render_scene()`, logo depois de:

```cpp
glEnable(GL_DEPTH_TEST);
```

adicione:

```cpp
glEnable(GL_CULL_FACE);
glCullFace(GL_BACK);
glFrontFace(GL_CCW);
```

Aqui não é necessário carregar essas três funções com `wglGetProcAddress`: elas pertencem à API OpenGL 1.1 exportada por `opengl32.dll` no Windows e já são declaradas pelo header usado pelo projeto.

---

# Parte F — câmera WASD + mouse sem quebrar o timestep fixo

## 10. TODO `GFX-CAMERA-01`: `camera_forward`

Abra:

```text
starter/common/engine.cpp
```

Localize:

```cpp
Vec3 camera_forward(const CameraState& camera)
```

Substitua por:

```cpp
const float cos_pitch = std::cos(camera.pitch);
return normalize({
    cos_pitch * std::sin(camera.yaw),
    std::sin(camera.pitch),
    -cos_pitch * std::cos(camera.yaw),
});
```

Com `yaw=0` e `pitch=0`, o resultado deve ser aproximadamente `(0,0,-1)`.

## 11. TODO `GFX-CAMERA-02`: `camera_right`

Na função seguinte use:

```cpp
constexpr Vec3 kWorldUp{0.0f, 1.0f, 0.0f};
return normalize(cross(camera_forward(camera), kWorldUp));
```

Para a câmera padrão, o resultado deve apontar aproximadamente para `+X`.

## 12. TODO `GFX-CAMERA-03`: `look_at`

Substitua o placeholder de `look_at` por:

```cpp
const Vec3 forward = normalize(target - eye);
const Vec3 right = normalize(cross(forward, world_up));
const Vec3 up = cross(right, forward);

Mat4 result = Mat4::identity();
result.m[0] = right.x;
result.m[4] = right.y;
result.m[8] = right.z;
result.m[12] = -dot(right, eye);

result.m[1] = up.x;
result.m[5] = up.y;
result.m[9] = up.z;
result.m[13] = -dot(up, eye);

result.m[2] = -forward.x;
result.m[6] = -forward.y;
result.m[10] = -forward.z;
result.m[14] = dot(forward, eye);
return result;
```

Agora rode o teste portátil:

```bat
cmake --build build-starter --config Debug
ctest --test-dir build-starter -C Debug --output-on-failure
```

Nesse ponto `test_camera_yaw_changes_forward_direction` e `test_default_camera_matches_original_view` devem passar.

## 13. TODO `GFX-CAMERA-04`: teclado nos dois frontends

Nos dois arquivos:

```text
starter/software_win32/main.cpp
starter/opengl_win32/main.cpp
```

localize:

```cpp
void update_camera_keyboard(float frame_dt)
```

Substitua o corpo por:

```cpp
constexpr float kCameraSpeed = 3.0f;
const Vec3 forward = camera_forward(g_camera);
const Vec3 right = camera_right(g_camera);

if ((GetAsyncKeyState('W') & 0x8000) != 0) {
    g_camera.position = g_camera.position + forward * (kCameraSpeed * frame_dt);
}
if ((GetAsyncKeyState('S') & 0x8000) != 0) {
    g_camera.position = g_camera.position - forward * (kCameraSpeed * frame_dt);
}
if ((GetAsyncKeyState('D') & 0x8000) != 0) {
    g_camera.position = g_camera.position + right * (kCameraSpeed * frame_dt);
}
if ((GetAsyncKeyState('A') & 0x8000) != 0) {
    g_camera.position = g_camera.position - right * (kCameraSpeed * frame_dt);
}
```

Observe no loop principal que essa função recebe `delta_time` do frame, enquanto `physics_step` continua recebendo `kFixedTimeStep` dentro do acumulador. Não troque um pelo outro.

## 14. TODO `GFX-CAMERA-05`: mouse nos dois frontends

Dentro de `window_proc`, localize `case WM_MOUSEMOVE` e substitua o placeholder por:

```cpp
case WM_MOUSEMOVE: {
    const POINT current{
        static_cast<short>(LOWORD(lparam)),
        static_cast<short>(HIWORD(lparam)),
    };

    if (g_have_last_mouse) {
        constexpr float kMouseSensitivity = 0.004f;
        const float dx = static_cast<float>(current.x - g_last_mouse.x);
        const float dy = static_cast<float>(current.y - g_last_mouse.y);

        g_camera.yaw += dx * kMouseSensitivity;
        g_camera.pitch = std::clamp(
            g_camera.pitch - dy * kMouseSensitivity,
            -1.45f,
            1.45f);
    }

    g_last_mouse = current;
    g_have_last_mouse = true;
    return 0;
}
```

O clamp evita chegar exatamente a ±90°, onde `forward` e `world_up` podem ficar quase paralelos e tornar o cálculo de `right` numericamente ruim.

---

# 15. Validação final

## Testes portáteis

```bat
cmake --build build-starter --config Debug
ctest --test-dir build-starter -C Debug --output-on-failure
```

Esperado:

```text
100% tests passed, 0 tests failed out of 1
```

## Software backend

```bat
build-starter\Debug\software_renderer.exe
```

Verifique:

- triângulos preenchidos;
- depth test;
- Lambert;
- faces traseiras não desenhadas;
- W/S/A/D movem a câmera;
- mouse altera yaw/pitch;
- P pausa a física;
- R restaura cena e câmera.

## OpenGL backend

```bat
build-starter\Debug\opengl_renderer.exe
```

Faça as mesmas verificações. A cena compartilhada deve continuar equivalente conceitualmente nos dois backends.

## Debugging quando algo falhar

**Tela vazia no software:** breakpoint em `draw_cube`; verifique `visible[]`, `signed_area`, `min_x/max_x`, `w0/w1/w2`.

**Tudo some após culling:** verifique o sinal de `signed_area` e confirme que você copiou `return signed_area > 0.0f` em `screen_triangle_front_facing`.

**Câmera anda invertida:** inspecione `camera_forward(g_camera)` com yaw/pitch zero; deve dar aproximadamente `(0,0,-1)`.

**Mouse vira de ponta-cabeça:** confirme `pitch - dy * sensitivity`, não `+ dy`.

**Física muda ao mover câmera:** confirme que `physics_step` ainda está exclusivamente no `while (accumulator >= kFixedTimeStep)`.

**OpenGL shader falha:** use o log já exibido por `compile_shader`; não altere o loader antes de ler o erro.

---

# 16. Compare com a solution somente agora

Depois que seus testes passarem, compare:

```text
starter/common/engine.cpp               ↔ solutions/common/engine.cpp
starter/software_win32/main.cpp         ↔ solutions/software_win32/main.cpp
starter/opengl_win32/main.cpp           ↔ solutions/opengl_win32/main.cpp
```

Todos os TODOs listados no início deste documento têm implementação correspondente na `solutions/`.

## Mapa de consistência auditada

Cada TODO obrigatório do starter está mapeado abaixo. O identificador deve existir no starter, nesta resolução, na solução correspondente e na cobertura de testes/validação do módulo.

- `GFX-CAMERA-03` — `starter/common/engine.cpp` → `solutions/common/engine.cpp`.
- `GFX-CAMERA-01` — `starter/common/engine.cpp` → `solutions/common/engine.cpp`.
- `GFX-CAMERA-02` — `starter/common/engine.cpp` → `solutions/common/engine.cpp`.
- `GFX-CULL-01` — `starter/common/engine.cpp` → `solutions/common/engine.cpp`.
- `GFX-LAMBERT-01` — `starter/opengl_win32/main.cpp` → `solutions/opengl_win32/main.cpp`.
- `GFX-CAMERA-04` — `starter/opengl_win32/main.cpp` → `solutions/opengl_win32/main.cpp`.
- `GFX-CULL-03` — `starter/opengl_win32/main.cpp` → `solutions/opengl_win32/main.cpp`.
- `GFX-CAMERA-05` — `starter/opengl_win32/main.cpp` → `solutions/opengl_win32/main.cpp`.
- `GFX-RASTER-01` — `starter/software_win32/main.cpp` → `solutions/software_win32/main.cpp`.
- `GFX-CULL-02` — `starter/software_win32/main.cpp` → `solutions/software_win32/main.cpp`.
- `GFX-CAMERA-04` — `starter/software_win32/main.cpp` → `solutions/software_win32/main.cpp`.
- `GFX-CAMERA-05` — `starter/software_win32/main.cpp` → `solutions/software_win32/main.cpp`.
