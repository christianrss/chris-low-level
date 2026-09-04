# Resolução guiada passo a passo — Graphics reference do chris-os

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

## Difícil B — compositor
Crie saída:

```cpp
Surface output(width, height, background);
```

Para cada layer, ignore null e percorra sua surface. Converta coordenada local `(sx,sy)` para destino `(dx,dy)`, faça clipping e então:

```cpp
output.set_pixel(
    ux,
    uy,
    alpha_over(layer.surface->pixel(sx, sy), output.pixel(ux, uy)));
```

O bloco completo de loops está no gabarito `solutions/src/graphics.cpp`; tente reconstruí-lo seguindo essa transformação de coordenadas antes de comparar.

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
