# Resolução guiada — alpha_blend_scanline

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `GFX-BLEND-01` | `starter/blend.cpp` | `blend_pixel` |
| `GFX-BLEND-02` | `starter/blend.cpp` | `blend_scanline` |
| `GFX-BLEND-03` | `starter/blend.cpp` | `blend_coverage` |

## Baseline

```powershell
cd days/2026-09-11/graphics/alpha_blend_scanline/starter
cmake -S . -B build_ci -G Ninja
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado:** FAIL.

## GFX-BLEND-01

### Onde colocar (GFX-BLEND-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/blend.cpp` |
| Função | `blend_pixel` |
| Substituir | o corpo sob o comentário `TODO [GFX-BLEND-01]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

dst vermelho deve ~128 com src a=128.

### Algoritmo / trace

lerp por canal com +127/255.

### Escreva o código

```cpp
    uint8_t a = src.a;
    dst.r = (uint8_t)((src.r * a + dst.r * (255 - a) + 127) / 255);
    dst.g = (uint8_t)((src.g * a + dst.g * (255 - a) + 127) / 255);
    dst.b = (uint8_t)((src.b * a + dst.b * (255 - a) + 127) / 255);
    dst.a = (uint8_t)(a + (dst.a * (255 - a) + 127) / 255);
```

### Por que funciona?

Src-over clássico em 8-bit.

### Verifique

120<=r<=135.

### Código completo alinhado ao solutions/ (GFX-BLEND-01)

```cpp
PEDAGOGY-SOLUTION: GFX-BLEND-01 */
    uint8_t a = src.a;
    dst.r = lerp8(dst.r, src.r, a);
    dst.g = lerp8(dst.g, src.g, a);
    dst.b = lerp8(dst.b, src.b, a);
    dst.a = (uint8_t)(a + (dst.a * (255 - a) + 127) / 255);
}
void blend_scanline(Pixel *dst, const Pixel *src, int n) {
    /* 
```

## GFX-BLEND-02

### Onde colocar (GFX-BLEND-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/blend.cpp` |
| Função | `blend_scanline` |
| Substituir | o corpo sob o comentário `TODO [GFX-BLEND-02]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Dois pixels opacos devem copiar r e g.

### Algoritmo / trace

loop blend_pixel.

### Escreva o código

```cpp
    for (int i = 0; i < n; ++i)
        blend_pixel(dst[i], src[i]);
    /* scanline done */
```

### Por que funciona?

Scanline = N blends.

### Verifique

dst[0].r==255, dst[1].g==255.

### Código completo alinhado ao solutions/ (GFX-BLEND-02)

```cpp
PEDAGOGY-SOLUTION: GFX-BLEND-02 */
    for (int i = 0; i < n; ++i) blend_pixel(dst[i], src[i]);
}
int blend_coverage(const Pixel *dst, int n, uint8_t min_a) {
    /* 
```

## GFX-BLEND-03

### Onde colocar (GFX-BLEND-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/blend.cpp` |
| Função | `blend_coverage` |
| Substituir | o corpo sob o comentário `TODO [GFX-BLEND-03]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Contar a>=200.

### Algoritmo / trace

loop contador.

### Escreva o código

```cpp
    int c = 0;
    if (!dst || n < 0) return -1;
    for (int i = 0; i < n; ++i) if (dst[i].a >= min_a) ++c;
    return c;
```

### Por que funciona?

Métrica simples de cobertura.

### Verifique

return 2.

### Código completo alinhado ao solutions/ (GFX-BLEND-03)

```cpp
PEDAGOGY-SOLUTION: GFX-BLEND-03 */
    int c = 0;
    if (!dst || n < 0) return -1;
    for (int i = 0; i < n; ++i) if (dst[i].a >= min_a) ++c;
    return c;
}
```

## Debug

| Sintoma | Correção |
|---------|----------|
| r baixo | +127 |

## Relatório de resolução

- TODOs: [ ]
