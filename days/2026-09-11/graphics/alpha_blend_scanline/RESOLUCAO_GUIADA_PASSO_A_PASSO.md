# Resolução guiada — alpha_blend_scanline

## Mapa exato starter → resolução

| TODO ID | Arquivo starter | Função / âncora | Substituir |
|---------|-----------------|-----------------|------------|
| `GFX-BLEND-PIXEL` | `starter/core/blend.cpp` | `blend_pixel` | stub `TODO [GFX-BLEND-PIXEL]` |
| `GFX-BLEND-SCAN` | `starter/core/blend.cpp` | `blend_scanline` | stub `TODO [GFX-BLEND-SCAN]` |
| `GFX-BLEND-SPRITE` | `starter/core/blend.cpp` | `update_sprite` | stub `TODO [GFX-BLEND-SPRITE]` |

---

## Baseline

```powershell
cd days/2026-09-11/graphics/alpha_blend_scanline/starter
cmake -S . -B build_ci -DCMAKE_BUILD_TYPE=Release
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado antes dos TODOs:** `test_blend` falha em pixel/scan/sprite.

---

## Relatório de resolução

## GFX-BLEND-PIXEL — `blend_pixel`

### Onde colocar (PIXEL)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/core/blend.cpp` |
| Função | `blend_pixel` |
| Substituir | stub `TODO [GFX-BLEND-PIXEL]` |

### 1. O problema (PIXEL)

Sem src-over, sprites translúcidos não misturam com o checker — a demo visual perde o sentido.

### Escreva o código (PIXEL)

```cpp
void blend_pixel(Pixel& dst, Pixel src) {
    const float sa = src.a / 255.0f;
    const float da = 1.0f - sa;
    dst.r = static_cast<std::uint8_t>(src.r * sa + dst.r * da);
    dst.g = static_cast<std::uint8_t>(src.g * sa + dst.g * da);
    dst.b = static_cast<std::uint8_t>(src.b * sa + dst.b * da);
    dst.a = 255;
}
```

### Por que funciona (PIXEL)

Interpola RGB pelo alpha da fonte (straight src-over). O assert só exige `r > 100` para a=128.

### Verifique (PIXEL)

`ctest` parcial: Caso 1 PASS; scan/sprite ainda falham.

### Debug (PIXEL)

| Sintoma | Causa | Ação |
|---------|-------|------|
| r baixo | usou a invertido | sa = src.a/255 |

---

## GFX-BLEND-SCAN — `blend_scanline`

### Onde colocar (SCAN)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/core/blend.cpp` |
| Função | `blend_scanline` |
| Substituir | stub `TODO [GFX-BLEND-SCAN]` |

### 1. O problema (SCAN)

O blit CPU escreve linhas inteiras; sem scanline o software_win32 não reutiliza o pixel testado.

### Escreva o código (SCAN)

```cpp
void blend_scanline(Pixel* dst, const Pixel* src, int n) {
    for (int i = 0; i < n; ++i) {
        blend_pixel(dst[i], src[i]);
    }
}
```

### Por que funciona (SCAN)

Delega ao pixel já correto; o Caso 2 cobre dois pixels opacos verdes/azuis.

### Verifique (SCAN)

`line_d[0].g == 255` após scanline. Sprite ainda pode falhar.

### Debug (SCAN)

| Sintoma | Causa | Ação |
|---------|-------|------|
| só 1º pixel | loop curto | `i < n` |

---

## GFX-BLEND-SPRITE — `update_sprite`

### Onde colocar (SPRITE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/core/blend.cpp` |
| Função | `update_sprite` |
| Substituir | stub `TODO [GFX-BLEND-SPRITE]` |

### 1. O problema (SPRITE)

Sem integração + bounce, os retângulos não se movem e VISUAL-01 fica estático.

### Escreva o código (SPRITE)

```cpp
void update_sprite(Sprite& s, float dt, float minx, float miny, float maxx, float maxy) {
    s.x += s.vx * dt;
    s.y += s.vy * dt;
    if (s.x < minx || s.x + s.w > maxx) {
        s.vx = -s.vx;
        s.x += s.vx * dt;
    }
    if (s.y < miny || s.y + s.h > maxy) {
        s.vy = -s.vy;
        s.y += s.vy * dt;
    }
}
```

### Por que funciona (SPRITE)

Euler + reflexão elástica; o teste só exige avanço com vx positivo.

### Verifique (SPRITE)

`ctest` PASS completo. Rode `blend_sw` / `blend_gl` para VISUAL-01.

### Debug (SPRITE)

| Sintoma | Causa | Ação |
|---------|-------|------|
| atravessa borda | sem inverter | negue vx/vy |
| some da tela | sem correção pos | some `vx*dt` após flip |
