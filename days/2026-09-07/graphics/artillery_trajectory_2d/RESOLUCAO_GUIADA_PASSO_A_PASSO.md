# Resolução guiada — artillery_trajectory_2d

## Mapa exato starter → resolução

| TODO ID | Arquivo starter | Função / âncora | Substituir |
|---------|-----------------|-----------------|------------|
| `GFX-ART-PHYS-01` | `starter/core/artillery.cpp` | `integrate` | stub `TODO [GFX-ART-PHYS-01]` |
| `GFX-ART-TERRAIN-02` | `starter/core/artillery.cpp` | `terrain_hit` | stub `TODO [GFX-ART-TERRAIN-02]` |
| `GFX-ART-TRAIL-03` | `starter/core/artillery.cpp` | `trail_push` | stub `TODO [GFX-ART-TRAIL-03]` |
| `GFX-ART-SW-04` | `starter/software_win32/main.cpp` | loop de frame | stub `TODO [GFX-ART-SW-04]` |
| `GFX-ART-GL-05` | `starter/opengl_win32/main.cpp` | desenho ortho | stub `TODO [GFX-ART-GL-05]` |
| `GFX-ART-D3D-06` | `starter/d3d11_win32/main.cpp` | swapchain | stub `TODO [GFX-ART-D3D-06]` |

---

## Baseline

```powershell
cd days/2026-09-07/graphics/artillery_trajectory_2d/starter
cmake -S . -B build_ci -DCMAKE_BUILD_TYPE=Release
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado antes dos TODOs:** compila; `test_artillery` falha em `integrate` / `terrain_hit` / `trail_push`.

---

## Relatório de resolução

## GFX-ART-PHYS-01 — `integrate`

### Onde colocar (PHYS-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/core/artillery.cpp` |
| Função | `integrate` |
| Substituir | corpo com `TODO [GFX-ART-PHYS-01]` |

### 1. O problema (PHYS-01)

Sem integração Euler, o projétil não se move: `fire()` define velocidade inicial mas `pos` permanece zero. A parábola exige `v += g*dt` e `p += v*dt`.

### Escreva o código (PHYS-01)

```cpp
void integrate(Projectile& p, float dt, float gravity) {
    if (!p.alive) {
        return;
    }
    p.vel.y -= gravity * dt;
    p.pos.x += p.vel.x * dt;
    p.pos.y += p.vel.y * dt;
}
```

### Por que funciona (PHYS-01)

Euler explícito é suficiente para o lab: gravidade só afeta `vy`; `vx` permanece constante sem arrasto.

### Verifique (PHYS-01)

Caso 1: após `integrate(p, 0.5f, 9.8f)`, `pos.x > 0` e `pos.y > 0`. `ctest` ainda falha em terreno/trilha.

---

## GFX-ART-TERRAIN-02 — `terrain_hit`

### Onde colocar (TERRAIN-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/core/artillery.cpp` |
| Função | `terrain_hit` |
| Substituir | stub `TODO [GFX-ART-TERRAIN-02]` |

### 1. O problema (TERRAIN-02)

Colisão 1D compara altura do projétil com `terrain.sample(x)`. Sem isso, o tiro atravessa o chão infinitamente.

### Escreva o código (TERRAIN-02)

```cpp
bool terrain_hit(const Projectile& p, const Terrain& t) {
    if (!p.alive) {
        return false;
    }
    return p.pos.y <= t.sample(p.pos.x);
}
```

### Por que funciona (TERRAIN-02)

`sample` interpola a altura do terreno no `x` atual; quando `y` cai abaixo, o impacto ocorre.

### Verifique (TERRAIN-02)

Caso 2: com `heights[32]=50` e `p.pos={320,40}`, assert `terrain_hit` verdadeiro.

### Debug (TERRAIN-02)

| Sintoma | Causa | Ação |
|---------|-------|------|
| nunca colide | `sample` retorna 0 | confira índice `x*0.1f` |
| colide no ar | comparou `>` em vez de `<=` | inverta operador |

---

## GFX-ART-TRAIL-03 — `trail_push`

### Onde colocar (TRAIL-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/core/artillery.cpp` |
| Função | `trail_push` |
| Substituir | stub `TODO [GFX-ART-TRAIL-03]` |

### 1. O problema (TRAIL-03)

A trilha visual precisa de histórico de posições. Buffer circular evita realocação a cada frame.

### Escreva o código (TRAIL-03)

```cpp
void trail_push(Trail& trail, Vec2 pos) {
    if (trail.count < Trail::kCapacity) {
        trail.points[trail.count++].pos = pos;
    } else {
        for (std::size_t i = 1; i < Trail::kCapacity; ++i) {
            trail.points[i - 1] = trail.points[i];
        }
        trail.points[Trail::kCapacity - 1].pos = pos;
    }
}
```

### Por que funciona (TRAIL-03)

Até encher, append simples; depois desloca janela deslizante — mesma ideia de ring buffer sem ponteiros.

### Verifique (TRAIL-03)

Caso 3: dois `trail_push` → `count == 2`. `ctest` passa para o core.

---

## GFX-ART-SW-04 — raster CPU

### Onde colocar (SW-04)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/software_win32/main.cpp` |
| Função | `wWinMain` + helpers DIB |
| Substituir | comentário `TODO [GFX-ART-SW-04]` |

### 1. O problema (SW-04)

O core calcula física; o backend CPU desenha terreno (linha + fill), projétil (círculo) e trilha (polyline) em framebuffer `uint32_t`, depois `StretchDIBits`.

### Escreva o código (SW-04)

```cpp
// PEDAGOGY-SOLUTION: GFX-ART-SW-04
void draw_scene(Framebuffer& fb, const Terrain& t, const Projectile& p, const Trail& trail) {
    fb.clear(0x00204080);
    for (int x = 0; x < fb.width; ++x) {
        const int y = static_cast<int>(t.sample(static_cast<float>(x)));
        fb.plot(x, fb.height - 1 - y, 0x0030A030);
    }
    if (p.alive) {
        fb.fill_circle(static_cast<int>(p.pos.x), fb.height - 1 - static_cast<int>(p.pos.y), 4, 0x00FFAA00);
    }
}
```

### Por que funciona (SW-04)

Mesmo contrato do Dia 01 software: você controla cada pixel antes de confiar na GPU.

### Verifique (SW-04)

Caso 4 / VISUAL-01: janela mostra parábola e terreno verde; trilha visível após disparo.

---

## GFX-ART-GL-05 — OpenGL ortho

### Onde colocar (GL-05)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/opengl_win32/main.cpp` |
| Função | init GL + draw |
| Substituir | `TODO [GFX-ART-GL-05]` |

### 1. O problema (GL-05)

Reproduzir a mesma cena com ortho e primitivas 2D.

### Escreva o código (GL-05)

```cpp
// PEDAGOGY-SOLUTION: GFX-ART-GL-05
glMatrixMode(GL_PROJECTION);
glLoadIdentity();
glOrtho(0, width, height, 0, -1, 1);
glBegin(GL_LINE_STRIP);
for (int x = 0; x < width; ++x) {
    const float y = terrain.sample(static_cast<float>(x));
    glVertex2f(static_cast<float>(x), y);
}
glEnd();
```

### Por que funciona (GL-05)

Orthographic 2D mapeia coordenadas de mundo 1:1 com a janela; física permanece em `artillery_core`.

### Verifique (GL-05)

Caso 5: `artillery_gl` — mesma silhueta que `artillery_sw` (VISUAL-01).

---

## GFX-ART-D3D-06 — D3D11

### Onde colocar (D3D-06)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/d3d11_win32/main.cpp` |
| Função | device/swapchain |
| Substituir | `TODO [GFX-ART-D3D-06]` |

### 1. O problema (D3D-06)

Terceiro backend com swapchain DXGI.

### Escreva o código (D3D-06)

```cpp
// PEDAGOGY-SOLUTION: GFX-ART-D3D-06
DXGI_SWAP_CHAIN_DESC sd{};
sd.BufferCount = 1;
sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
sd.OutputWindow = hwnd;
sd.SampleDesc.Count = 1;
sd.Windowed = TRUE;
// D3D11CreateDeviceAndSwapChain → CreateRenderTargetView → ClearRenderTargetView → Present
```

### Por que funciona (D3D-06)

Mesma separação core/backends do `dual_backend_3d`; D3D11 substitui apenas apresentação.

### Verifique (D3D-06)

Caso 6 / VISUAL-01: três janelas, mesma trajetória.

### Resultado esperado

`ctest` verde; três executáveis mostram parábola idêntica (tolerância visual).
