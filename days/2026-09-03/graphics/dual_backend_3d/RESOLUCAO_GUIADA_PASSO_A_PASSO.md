# RESOLUÇÃO GUIADA - 3D + Physics + Animation / Software vs OpenGL

## Antes de começar no Visual Studio

Use um build limpo:

```bat
rmdir /s /q build-solution 2>nul
cmake -S solutions -B build-solution -A x64
cmake --build build-solution --config Debug
```

O projeto define `NOMINMAX` antes de `windows.h` para evitar a colisão das macros `min/max` do Win32 com `std::min/std::max`.

Comece executando:

```bat
build-solution\Debug\core_tests.exe
```

Só depois abra os renderers.

---

## Exercício Fácil - rastrear um vértice pelo pipeline

Escolha um vértice local `p = (x,y,z,1)`.

O pipeline é:

```text
local --Model--> world --View--> camera --Projection--> clip
     --divide by w--> NDC --viewport--> screen pixel
```

### Como resolver

1. abra `common/engine.cpp`;
2. encontre a matriz model de um DrawItem;
3. encontre `view` e `projection`;
4. no software renderer, localize `project_vertex`;
5. coloque breakpoint após cada multiplicação;
6. anote os quatro componentes.

O ponto importante é entender que `clip.w` participa da perspectiva. Depois:

```cpp
const float inverse_w = 1.0f / clip.w;
const float ndc_x = clip.x * inverse_w;
```

Se você simplesmente ignorasse `w`, objetos distantes não pareceriam menores da forma correta.

---

## Exercício Médio A - implementar o rasterizador software

Abra:

```text
starter/software_win32/main.cpp
```

Localize `rasterize_triangle`.

### Passo 1 - área orientada

```cpp
const float area = edge(a.x, a.y, b.x, b.y, c.x, c.y);
if (std::fabs(area) < 1.0e-6f) {
    return;
}
```

Triângulo de área quase zero é degenerado.

### Passo 2 - bounding box

Não teste todos os pixels da tela. Calcule a caixa que contém o triângulo:

```cpp
const float min_x_f = std::min({a.x, b.x, c.x});
const float max_x_f = std::max({a.x, b.x, c.x});
const float min_y_f = std::min({a.y, b.y, c.y});
const float max_y_f = std::max({a.y, b.y, c.y});
```

Prenda aos limites da tela:

```cpp
const int min_x = std::max(0, static_cast<int>(std::floor(min_x_f)));
const int max_x = std::min(
    framebuffer.width - 1,
    static_cast<int>(std::ceil(max_x_f))
);
```

Faça o mesmo para Y.

### Passo 3 - iluminação Lambert por face

Calcule a normal do triângulo no mundo:

```cpp
const Vec3 normal = normalize(
    cross(b.world - a.world, c.world - a.world)
);
```

Direção da luz:

```cpp
const Vec3 light_direction = normalize(Vec3{-0.4f, 0.8f, 0.6f});
```

Lambert:

```cpp
const float diffuse = std::max(0.0f, dot(normal, light_direction));
const float light = 0.20f + 0.80f * diffuse;
```

O `0.20` é uma luz ambiente simples para a face não ficar totalmente preta.

### Passo 4 - percorra pixels da bounding box

Amostre no centro do pixel:

```cpp
const float sample_x = static_cast<float>(x) + 0.5f;
const float sample_y = static_cast<float>(y) + 0.5f;
```

### Passo 5 - barycentrics

```cpp
const float w0 = edge(b.x, b.y, c.x, c.y, sample_x, sample_y) / area;
const float w1 = edge(c.x, c.y, a.x, a.y, sample_x, sample_y) / area;
const float w2 = 1.0f - w0 - w1;
```

Se algum peso é negativo, o ponto está fora para a convenção de orientação usada:

```cpp
if (w0 < 0.0f || w1 < 0.0f || w2 < 0.0f) {
    continue;
}
```

### Passo 6 - interpole profundidade

```cpp
const float depth = w0 * a.z + w1 * b.z + w2 * c.z;
```

Rejeite fora de `[0,1]`.

### Passo 7 - depth test

```cpp
const std::size_t index =
    static_cast<std::size_t>(y) * framebuffer.width + x;

if (depth < framebuffer.depth[index]) {
    framebuffer.depth[index] = depth;
    framebuffer.pixels[index] = packed_color;
}
```

Essa condição é o equivalente didático do depth test feito pela GPU.

---

## Exercício Médio B - Lambert no fragment shader OpenGL

Abra:

```text
starter/opengl_win32/main.cpp
```

No fragment shader, substitua o TODO por:

```glsl
vec3 normal = normalize(v_normal);
vec3 light_direction = normalize(vec3(-0.4, 0.8, 0.6));
float diffuse = max(dot(normal, light_direction), 0.0);
float lighting = 0.2 + 0.8 * diffuse;
gl_FragColor = vec4(u_color * lighting, 1.0);
```

### Compare com o software renderer

CPU:

```cpp
dot(normal, light_direction)
```

GPU/GLSL:

```glsl
dot(normal, light_direction)
```

A matemática é a mesma. O que muda é **onde e em quantos elementos em paralelo ela é executada**.

---

## Exercício de Physics - entender e alterar a simulação

No core compartilhado, procure a atualização do corpo físico.

A integração semi-implícita segue:

```text
velocity += gravity * dt
position += velocity * dt
```

### Experimento guiado

1. rode com gravidade original;
2. altere temporariamente a magnitude para metade;
3. observe que a queda demora mais;
4. restaure;
5. altere restitution;
6. observe a altura dos quiques.

### Como verificar a colisão

Quando a esfera cruza o plano, a posição deve ser corrigida para não continuar penetrando e a velocidade vertical deve mudar de sinal multiplicada por restitution.

Essa é uma resposta de colisão simplificada; depois construiremos impulses e friction.

---

## Exercício de Animation - hierarquia pai-filho

A animação do braço não move cada parte em coordenadas globais independentemente. A mão herda o cotovelo, que herda o ombro.

Pense em:

```text
WorldShoulder = Root * LocalShoulder
WorldElbow    = WorldShoulder * LocalElbow
WorldHand     = WorldElbow * LocalHand
```

### Como estudar no debugger

1. pause em `build_draw_list`/função equivalente;
2. anote matriz do ombro;
3. avance até cotovelo;
4. observe que a matriz anterior entra na multiplicação;
5. mude o ângulo do ombro e veja mão/cotovelo se moverem juntos.

Esse princípio será reutilizado em skeleton/bones.

---

## Exercício Difícil - back-face culling nos dois backends

### Software renderer

Antes de rasterizar, você pode usar o sinal da área em screen space.

Com a convenção atual, faça um teste e determine qual sinal representa a face frontal. Por exemplo:

```cpp
const float area = edge(a.x, a.y, b.x, b.y, c.x, c.y);
if (area <= 0.0f) {
    return;
}
```

**Atenção:** o sinal correto depende da ordem dos vértices e da inversão de Y no viewport. Se todas as faces sumirem, inverta a comparação. A parte didática é justamente relacionar winding com screen space.

### OpenGL

Depois de criar o contexto e antes de desenhar:

```cpp
glEnable(GL_CULL_FACE);
glCullFace(GL_BACK);
glFrontFace(GL_CCW);
```

Como o projeto usa OpenGL legado + funções carregadas manualmente, `glEnable` está em `opengl32`, mas confirme se as outras funções necessárias estão disponíveis no header/loader usado.

### O que comparar

- software: você decide matematicamente se o triângulo continua;
- OpenGL: você configura uma etapa fixa do pipeline;
- em ambos, a noção de orientação dos vértices continua existindo.

---

## Desafio principal - câmera WASD + mouse mantendo física fixa

### Parte 1 - estado da câmera

Adicione ao core ou frontend:

```cpp
Vec3 camera_position{0.0f, 1.5f, 6.0f};
float camera_yaw = 0.0f;
float camera_pitch = 0.0f;
```

### Parte 2 - input

Mantenha teclas pressionadas usando estado por frame ou `GetAsyncKeyState` em uma primeira versão educacional.

Exemplo conceitual:

```cpp
if (GetAsyncKeyState('W') & 0x8000) {
    camera_position += forward * camera_speed * frame_dt;
}
```

Faça o mesmo com S/A/D.

### Parte 3 - direção pelo yaw/pitch

```text
forward.x = cos(pitch) * sin(yaw)
forward.y = sin(pitch)
forward.z = -cos(pitch) * cos(yaw)
```

Normalize `forward`; calcule `right = normalize(cross(forward, world_up))`.

### Parte 4 - view matrix

Construa `look_at(camera_position, camera_position + forward, up)`.

### Parte 5 - não misture frame_dt com physics_dt

A câmera pode usar `frame_dt` para responsividade. A física continua em um acumulador de timestep fixo, por exemplo 1/120 s:

```text
accumulator += frame_dt
while accumulator >= physics_dt:
    simulate(physics_dt)
    accumulator -= physics_dt
```

Essa separação é essencial em engines reais.

### Critério de conclusão

Você consegue mover a câmera com taxa de frames variável sem alterar a velocidade de queda/quique do corpo físico.
