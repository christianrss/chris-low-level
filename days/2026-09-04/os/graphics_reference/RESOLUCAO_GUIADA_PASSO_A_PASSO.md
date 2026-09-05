# Resolução guiada passo a passo — Graphics reference do chris-os

## Mapa exato starter → resolução

- `D2-GFX-INDEX` → `starter/src/graphics.cpp`
- `D2-GFX-FILL-RECT` → `starter/src/graphics.cpp`
- `D2-GFX-ALPHA-OVER` → `starter/src/graphics.cpp`
- `D2-GFX-COMPOSE` → `starter/src/graphics.cpp`

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

## Baseline

```bash
cmake -S days/2026-09-04/os/graphics_reference/starter -B days/2026-09-04/os/graphics_reference/starter/build
cmake --build days/2026-09-04/os/graphics_reference/starter/build
ctest --test-dir days/2026-09-04/os/graphics_reference/starter/build --output-on-failure
```

## Fácil — índice de pixel
Abra `starter/src/graphics.cpp`, função `Surface::index`.

```cpp
if (x >= width_ || y >= height_) {
    throw std::out_of_range("pixel outside surface");
}
return y * width_ + x;
```

Para width=4 e `(x=1,y=2)`, offset=9. Desenhe a grade 4x4 e confirme.

### Por que funciona?
Pixels são armazenados row-major: cada linha ocupa `width_` slots consecutivos. `y * width_ + x` salta `y` linhas completas e avança `x` colunas. Guard `out_of_range` evita escrita fora do buffer.

## Médio — `fill_rect` com clipping
Comece ignorando dimensões vazias:

```cpp
if (width <= 0 || height <= 0) {
    return;
}
```

Calcule limites recortados:

```cpp
const int x0 = std::max(0, x);
const int y0 = std::max(0, y);
const int x1 = std::min(static_cast<int>(width_), x + width);
const int y1 = std::min(static_cast<int>(height_), y + height);
```

Preencha:

```cpp
for (int py = y0; py < y1; ++py) {
    for (int px = x0; px < x1; ++px) {
        set_pixel(static_cast<std::size_t>(px), static_cast<std::size_t>(py), value);
    }
}
```

No teste `fill_rect(-1,-1,3,3)`, apenas a região [0,2)x[0,2) deve receber vermelho.

### Por que funciona?
`x0,y0` e `x1,y1` recortam o retângulo pedido à interseção com a surface — retângulos parcialmente fora da tela não corrompem memória nem lançam exceção. Loops semiabertos `[x0,x1)` evitam off-by-one.

## Difícil A — alpha-over
Implemente `alpha_over`:

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

`+127` serve como arredondamento inteiro aproximado antes da divisão.

### Por que funciona?
Fórmula `src*α + dst*(255-α)` com divisão por 255 implementa “over” em inteiro. `+127` antes de `/255` aproxima arredondamento para o vizinho mais próximo — vermelho+azul 50% → ~(127,0,128).

## Difícil B — compositor
Crie saída:

```cpp
Surface output(width, height, background);
```

Para cada layer, ignore `nullptr`, percorra a surface e converta coordenada local `(sx,sy)` em destino `(dx,dy)`. Digite o bloco completo no TODO `D2-GFX-COMPOSE` de `starter/src/graphics.cpp`:

```cpp
Surface output(width, height, background);
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
                ux,
                uy,
                alpha_over(layer.surface->pixel(sx, sy), output.pixel(ux, uy)));
        }
    }
}
return output;
```

### Por que funciona?
Cada layer desenha por cima da composição acumulada (`alpha_over` com pixel já composto). Clipping em `(dx,dy)` ignora pixels fora da surface destino. Ordem do vetor `layers` é z-order — último layer vence.

## Teste esperado

```text
chris-os graphics reference tests passed
100% tests passed
```

O pixel misturado vermelho + azul 50% deve ficar aproximadamente `(127,0,128)`.

## Debug estilo sistemas
Se clipping falhar, inspecione `x0,y0,x1,y1`. Se composição falhar, inspecione `sx,sy,dx,dy`, pixel source, pixel destination e alpha. Faça primeiro um caso 2x2 no papel.

## Benchmark
O benchmark compõe 40 frames 640x360 com duas surfaces. Compile com `CHRIS_BUILD_BENCHMARKS=ON`, rode e registre FPS. Depois use isso como baseline antes de adicionar damage tracking/SIMD.


## Solução final comentada
Depois de deixar o starter verde, compare somente os blocos `PEDAGOGY-SOLUTION` em `solutions/` correspondentes aos IDs do mapa. Se houver uma linha necessária no gabarito que não foi ensinada acima, trate como defeito do material e não como algo que você deveria adivinhar.

## Relatório de resolução

| ID | Função | Aceite visual/numérico |
|----|--------|------------------------|
| D2-GFX-INDEX | `Surface::index` | `y*width+x`; fora dos limites lança |
| D2-GFX-FILL-RECT | clipping | retângulo negativo parcialmente visível |
| D2-GFX-ALPHA-OVER | blend | vermelho+azul 50% ≈ (127,0,128) |
| D2-GFX-COMPOSE | z-order | layers posteriores por cima |

Aceite: `chris-os graphics reference tests passed`. Depure clipping com `x0,y0,x1,y1` antes de alpha. Benchmark 640×360 estabelece baseline FPS CPU antes de otimizações futuras do chris-os.
