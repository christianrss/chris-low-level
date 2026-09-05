# Resolução guiada auditada — dual_backend_3d

## Mapa exato starter → resolução

| TODO ID | Starter | Função/área |
|---------|---------|-------------|
| `GFX-CAMERA-01` | `starter/common/engine.cpp` | `camera_forward()` |
| `GFX-CAMERA-02` | `starter/common/engine.cpp` | `camera_right()` |
| `GFX-CAMERA-03` | `starter/common/engine.cpp` | `look_at()` |
| `GFX-CULL-01` | `starter/common/engine.cpp` | `screen_triangle_front_facing()` |
| `GFX-CULL-02` | `starter/software_win32/main.cpp` | rasterização — área com sinal / back-face |
| `GFX-CAMERA-04` | `starter/software_win32/main.cpp`, `starter/opengl_win32/main.cpp` | `update_camera_keyboard()` |
| `GFX-CAMERA-05` | `starter/software_win32/main.cpp`, `starter/opengl_win32/main.cpp` | `WM_MOUSEMOVE` — yaw/pitch |
| `GFX-CULL-03` | `starter/opengl_win32/main.cpp` | `render_scene()` — `GL_CULL_FACE` |
| `GFX-LAMBERT-01` | `starter/opengl_win32/main.cpp` | fragment shader — difuso + ambiente |

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-03/graphics/dual_backend_3d/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

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

> Continua em `RESOLUCAO_APENDICE.md`.

## Relatório de resolução

Resumo executivo deste módulo (detalhes e checklist completo no apêndice):

### O que foi validado

- Câmera FPS (`GFX-CAMERA-01`…`05`) com paridade software/OpenGL.
- Culling por winding (`GFX-CULL-01`…`03`) e Lambert (`GFX-LAMBERT-01`).
- `core_tests` e backends compilam; starter falha nos TODOs até implementação.

### Armadilhas encontradas

- Inversão de Y no raster software vs coordenadas OpenGL.
- `view_matrix` exige base ortonormal consistente (right × up = -forward).
- Benchmark visual não substitui testes numéricos de `core_tests`.

### Próximo passo

Complete o apêndice, registre FPS/frame time em `BENCHMARK_GUIADO.md` → **Resultados observados**, e compare um frame software vs GL.
