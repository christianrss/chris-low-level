# RESOLUÇÃO GUIADA — OS / Graphics reference (chris-os)

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `D2-GFX-INDEX` | `starter/src/graphics.cpp` | `Surface::index` |
| `D2-GFX-FILL-RECT` | `starter/src/graphics.cpp` | `Surface::fill_rect` |
| `D2-GFX-ALPHA-OVER` | `starter/src/graphics.cpp` | `alpha_over` |
| `D2-GFX-COMPOSE` | `starter/src/graphics.cpp` | `Compositor::compose` |
| `D2-GFX-DIRTY-RECT` | `starter/src/graphics.cpp` | `DirtyTracker` + marks em fill/blit |
| `D2-GFX-FRAME-PACE` | `starter/src/graphics.cpp` | `FramePacer::compose_with_damage` |

Cada ID existe como `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` no gabarito e `PEDAGOGY-TEST: ID` nos testes. Se não bater, pare.

> Trabalhe em `days/2026-09-04/os/graphics_reference/starter/`. `solutions/` só após tentativa.

Layout: pixels row-major; `Pixel {r,g,b,a}`; `Layer {surface*, x, y}`; `Rect` AABB; `DirtyTracker`; `FrameStats`.

Os exercícios 5–6 (dirty + frame pace) continuam em `RESOLUCAO_APENDICE.md` se você preferir fatiar a leitura — o mapa acima cobre os seis IDs.

---

## Baseline

```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

Build passa; testes falham enquanto os TODOs existirem.

---

## Exercício Fácil — `D2-GFX-INDEX`

### 1. O problema

O starter lança `logic_error("TODO index")`. Sem índice, `pixel`/`set_pixel`/`fill_rect` não acessam o buffer.

### 2. O algoritmo

```text
se x >= width_ ou y >= height_: throw out_of_range
return y * width_ + x
```

### 3. Escreva o código

```cpp
if (x >= width_ || y >= height_) {
    throw std::out_of_range("pixel outside surface");
}
return y * width_ + x;
```

### 4. Por que funciona

Row-major: cada linha ocupa `width_` slots. `y * width_ + x` salta `y` linhas e avança `x` colunas. Guard evita escrita fora do `vector`.

Trace — width=4, `(1,2)` → `2*4+1=9`.

### 5. Verifique

Compile; testes de fill/compose ainda falham. Confirme `(0,0)` → 0 e `(width-1,height-1)` → último.

---

## Exercício Médio — `D2-GFX-FILL-RECT`

### 1. O problema

TODO vazio: retângulos (inclusive negativos) não pintam. O teste `fill_rect(-1,-1,3,3)` espera só a interseção visível.

### 2. O algoritmo

```text
se width<=0 ou height<=0: return
x0 = max(0, x);  y0 = max(0, y)
x1 = min(width_, x+width);  y1 = min(height_, y+height)
se x0>=x1 ou y0>=y1: return
para py in [y0,y1), px in [x0,x1): set_pixel(px,py,value)
mark_dirty(x0,y0,x1-x0,y1-y0)   // ver D2-GFX-DIRTY-RECT
```

### 3. Escreva o código

```cpp
if (width <= 0 || height <= 0) {
    return;
}
const int x0 = std::max(0, x);
const int y0 = std::max(0, y);
const int x1 = std::min(static_cast<int>(width_), x + width);
const int y1 = std::min(static_cast<int>(height_), y + height);
if (x0 >= x1 || y0 >= y1) {
    return;
}
for (int py = y0; py < y1; ++py) {
    for (int px = x0; px < x1; ++px) {
        set_pixel(static_cast<std::size_t>(px), static_cast<std::size_t>(py), value);
    }
}
mark_dirty(x0, y0, x1 - x0, y1 - y0);
```

### 4. Por que funciona

`[x0,x1)×[y0,y1)` é a interseção com a surface. Semiaberto evita off-by-one. Dirty só após clip — nunca marque o pedido cru.

### 5. Verifique

Surface 4×4, `(-1,-1,3,3)` → `[0,2)×[0,2)`. Pedido `(10,10,2,2)` → vazio, sem dirty.

---

## Exercício Difícil A — `D2-GFX-ALPHA-OVER`

### 1. O problema

Starter devolve `dst` inalterado. Blend 50% vermelho+azul deve ~`(127,0,128)`.

### 2. O algoritmo

```text
α = src.a;  inv = 255 - α
canal = (src*α + dst*inv + 127) / 255
out.a = 255
```

### 3. Escreva o código

```cpp
const unsigned alpha = src.a;
const unsigned inv = 255u - alpha;
Pixel out;
out.r = static_cast<std::uint8_t>((src.r * alpha + dst.r * inv + 127u) / 255u);
out.g = static_cast<std::uint8_t>((src.g * alpha + dst.g * inv + 127u) / 255u);
out.b = static_cast<std::uint8_t>((src.b * alpha + dst.b * inv + 127u) / 255u);
out.a = 255;
return out;
```

### 4. Por que funciona

Source-over 8-bit. `+127` aproxima arredondamento. Destino tratado como opaco.

### 5. Verifique

`(255,0,0,128)` sobre `(0,0,255,255)` — R e B ~128. α=0 → dst; α=255 → src.

---

## Exercício Difícil B — `D2-GFX-COMPOSE`

### 1. O problema

Starter só devolve surface com `background`. Layers não são desenhadas.

### 2. O algoritmo

```text
output = Surface(width, height, background)
para cada layer (nullptr → skip):
  para sy,sx na layer:
    dx = layer.x + sx; dy = layer.y + sy
    se fora do destino: continue
    output[dx,dy] = alpha_over(layer[sx,sy], output[dx,dy])
  mark_dirty(footprint ∩ bounds)   // D2-GFX-DIRTY-RECT
return output
```

### 3. Escreva o código

```cpp
Surface output(width, height, background);
const Rect bounds{0, 0, static_cast<int>(width), static_cast<int>(height)};
for (const auto& layer : layers) {
    if (layer.surface == nullptr) {
        continue;
    }
    for (std::size_t sy = 0; sy < layer.surface->height(); ++sy) {
        for (std::size_t sx = 0; sx < layer.surface->width(); ++sx) {
            const int dx = layer.x + static_cast<int>(sx);
            const int dy = layer.y + static_cast<int>(sy);
            if (dx < 0 || dy < 0 || dx >= static_cast<int>(width) ||
                dy >= static_cast<int>(height)) {
                continue;
            }
            const auto ux = static_cast<std::size_t>(dx);
            const auto uy = static_cast<std::size_t>(dy);
            output.set_pixel(
                ux, uy,
                alpha_over(layer.surface->pixel(sx, sy), output.pixel(ux, uy)));
        }
    }
    const Rect footprint{
        layer.x,
        layer.y,
        static_cast<int>(layer.surface->width()),
        static_cast<int>(layer.surface->height())};
    const Rect dirty = footprint.intersect(bounds);
    if (!dirty.empty()) {
        output.mark_dirty(dirty);
    }
}
return output;
```

### 4. Por que funciona

Z-order = ordem do vetor. Clip em `(dx,dy)`. Dirty do footprint permite o frame pacer saber o que mudou.

### 5. Verifique

Testes antigos de compose/alpha devem passar. Dirty da layer 2×2 em `(2,1)` → rect `(2,1,2,2)`.

---

## Exercício Difícil C — `D2-GFX-DIRTY-RECT`

### 1. O problema

`DirtyTracker::mark_dirty` / `take_dirty_union` estão vazios. Sem união, não há damage para o frame pacer.

### 2. O algoritmo

```text
mark(x,y,w,h):
  se w<=0 ou h<=0: return
  se tracker vazio: union = rect
  senao: union = union.unite(rect)

take_dirty_union:
  out = dirty_union(); clear(); return out
```

### 3. Escreva o código

```cpp
void DirtyTracker::mark_dirty(int x, int y, int width, int height) {
    if (width <= 0 || height <= 0) {
        return;
    }
    const Rect added{x, y, width, height};
    if (!has_ || union_.empty()) {
        union_ = added;
        has_ = true;
        return;
    }
    union_ = union_.unite(added);
}

Rect DirtyTracker::take_dirty_union() {
    const Rect out = dirty_union();
    clear();
    return out;
}
```

Ligue `fill_rect` (após clip) e o footprint do compose a `mark_dirty` — ver exercícios anteriores.

### 4. Por que funciona

AABB union é O(1) por mark. Trace: marks `(0,0,2,2)` + `(5,5,2,2)` → `(0,0,7,7)` área 49.

### 5. Verifique

`PEDAGOGY-TEST: D2-GFX-DIRTY-RECT` — fill clipado, união de dois fills, footprint do compose.

---

## Exercício Difícil D — `D2-GFX-FRAME-PACE`

### 1. O problema

`compose_with_damage` devolve `FrameStats{}` e não toca o framebuffer. Precisa recompor **só** `damage ∩ bounds`.

### 2. O algoritmo

```text
region = damage.intersect(bounds do target)
stats.dirty_area = region.area()
para cada pixel (px,py) em region:
  cor = background
  para cada layer: se (px,py) cai na layer → alpha_over
  target.set_pixel(px,py,cor)
  pixels_touched++
mark_dirty(region) no target
return stats
```

A overload com `DirtyTracker&` chama `take_dirty_union()` e delega.

### 3. Escreva o código

```cpp
FrameStats FramePacer::compose_with_damage(
    Surface& target,
    Pixel background,
    const std::vector<Layer>& layers,
    Rect damage) {
    FrameStats stats{};
    const Rect bounds{
        0, 0,
        static_cast<int>(target.width()),
        static_cast<int>(target.height())};
    const Rect region = damage.intersect(bounds);
    stats.dirty_area = region.area();
    if (region.empty()) {
        return stats;
    }
    for (int py = region.y; py < region.y + region.height; ++py) {
        for (int px = region.x; px < region.x + region.width; ++px) {
            Pixel out = background;
            for (const auto& layer : layers) {
                if (layer.surface == nullptr) {
                    continue;
                }
                const int sx = px - layer.x;
                const int sy = py - layer.y;
                if (sx < 0 || sy < 0 ||
                    sx >= static_cast<int>(layer.surface->width()) ||
                    sy >= static_cast<int>(layer.surface->height())) {
                    continue;
                }
                out = alpha_over(
                    layer.surface->pixel(
                        static_cast<std::size_t>(sx),
                        static_cast<std::size_t>(sy)),
                    out);
            }
            target.set_pixel(
                static_cast<std::size_t>(px),
                static_cast<std::size_t>(py),
                out);
            ++stats.pixels_touched;
        }
    }
    target.mark_dirty(region);
    return stats;
}
```

### 4. Por que funciona

Pixels fora do damage **permanecem** (frame anterior). Damage full-screen deve bater bit-a-bit com `Compositor::compose`. `pixels_touched == dirty_area` neste lab (uma AABB).

### 5. Verifique

```bash
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

Esperado: `chris-os graphics reference tests passed`.

---

## Checkpoint no papel

1. `fill_rect(-1,-1,3,3)` em 4×4 — pixels e dirty?
2. Dois marks distantes — área da união vs soma das áreas?
3. Damage 2×2 com framebuffer cinza — o que acontece em `(7,7)`?
4. Sprite que se move: por que marcar posição antiga **e** nova?

## Debugging

1. Clip falha → `x0,y0,x1,y1` semiaberto.
2. Dirty “gigante” → marcou antes do clip ou esqueceu `take`.
3. Fantasma do sprite → damage sem posição anterior.
4. Pace ≠ compose full → z-order / sample `sx = px - layer.x`.
5. Mais em `RESOLUCAO_APENDICE.md`.

## Benchmark

```bash
cmake -S starter -B starter/build-bench -DCHRIS_BUILD_BENCHMARKS=ON
cmake --build starter/build-bench
./starter/build-bench/os_graphics_benchmark
```

Compare `mode=full` vs `mode=damage` (`pixels_touched`). Hipótese antes de rodar.

## Relatório

| ID | Aceite |
|----|--------|
| INDEX | `y*width+x`; fora → throw |
| FILL-RECT | negativo parcialmente visível + dirty clipado |
| ALPHA-OVER | vermelho+azul 50% ≈ (127,0,128) |
| COMPOSE | layers posteriores por cima + dirty footprint |
| DIRTY-RECT | união AABB; `take` limpa |
| FRAME-PACE | só damage; `pixels_touched` / `dirty_area` |

**Saída:** `chris-os graphics reference tests passed`.

## Relatório de resolução

- TODOs concluídos: ___
- Testes starter: FAIL esperado antes / PASS depois? ___
- Paper-trace dirty+pace feito? Sim/Não
- Portei para projects/? Sim/Não — evidência: ___
