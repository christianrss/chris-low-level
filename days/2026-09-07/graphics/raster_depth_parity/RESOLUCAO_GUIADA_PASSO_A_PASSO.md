# Resolução guiada — raster_depth_parity

## Mapa exato starter → resolução

| TODO ID | Arquivo starter | Função / âncora | Substituir |
|---------|-----------------|-----------------|------------|
| `GFX-DEPTH-CPU-01` | `starter/extension/depth_buffer.cpp` | `DepthBuffer::test` | stub `TODO [GFX-DEPTH-CPU-01]` |
| `GFX-DEPTH-GL-02` | `starter/extension/opengl_depth.cpp` | init GL depth | stub `TODO [GFX-DEPTH-GL-02]` |
| `GFX-DEPTH-PARITY-03` | `starter/extension/parity.cpp` | `parity_scene_cpu` | stub `TODO [GFX-DEPTH-PARITY-03]` |
| `GFX-PERSP-04` | `starter/extension/perspective.cpp` | `perspective_z_at` | stub `TODO [GFX-PERSP-04]` |

---

## Baseline

```powershell
cd days/2026-09-07/graphics/raster_depth_parity/starter
cmake -S . -B build_ci -DCMAKE_BUILD_TYPE=Release
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado antes dos TODOs:** `test_depth` falha em `DepthBuffer::test`.

---

## Relatório de resolução

## GFX-DEPTH-CPU-01 — depth test CPU

### Onde colocar (CPU-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/extension/depth_buffer.cpp` |
| Função | `DepthBuffer::test` |
| Substituir | `TODO [GFX-DEPTH-CPU-01]` |

### 1. O problema (CPU-01)

Sem Z-buffer, o último triângulo rasterizado vence mesmo estando atrás. `test` deve aceitar apenas profundidades menores que o valor armazenado.

### Escreva o código (CPU-01)

```cpp
bool DepthBuffer::test(int x, int y, float depth) {
    if (x < 0 || y < 0 || x >= width || y >= height) {
        return false;
    }
    const std::size_t i = static_cast<std::size_t>(y) * width + x;
    if (depth < z[i]) {
        z[i] = depth;
        return true;
    }
    return false;
}
```

### Por que funciona (CPU-01)

Comparação `depth < z[i]` com convenção near=menor; pixel só pinta se mais perto que o anterior.

### Verifique (CPU-01)

Caso 1: `test(1,1,0.5)` ok; `test(1,1,0.9)` rejeita; `test(1,1,0.3)` atualiza.

---

## GFX-DEPTH-GL-02 — OpenGL depth

### Onde colocar (GL-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/extension/opengl_depth.cpp` |
| Função | `wWinMain` |
| Substituir | `TODO [GFX-DEPTH-GL-02]` |

### 1. O problema (GL-02)

Espelhar o CPU: `glEnable(GL_DEPTH_TEST)`, `glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)`, depth function `GL_LESS`.

### Por que funciona (GL-02)

GPU aplica o mesmo teste por pixel que você implementou na CPU.

### Verifique (GL-02)

Caso 2: `depth_gl` abre sem erro; triângulo da frente oculta o de trás.

---

## GFX-DEPTH-PARITY-03 — paridade vermelho/azul

### Onde colocar (PARITY-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/extension/parity.cpp` |
| Função | `parity_scene_cpu` |
| Substituir | `TODO [GFX-DEPTH-PARITY-03]` |

### 1. O problema (PARITY-03)

Dois triângulos sobrepostos: vermelho `z=0.8`, azul `z=0.2`. Sem depth, vermelho poderia vencer; com depth, região central deve ser azul.

### Escreva o código (PARITY-03)

Rasterize full-screen quads com `db.test`; pinte vermelho primeiro, azul depois — azul deve prevalecer no overlap.

### Por que funciona (PARITY-03)

Ordem de desenho deixa de importar quando o teste de profundidade está correto.

### Verifique (PARITY-03)

Caso 3: `hash_region` da região central bate com valor documentado em TEORIA.

### Debug (PARITY-03)

| Sintoma | Causa | Ação |
|---------|-------|------|
| vermelho na frente | depth invertido | use menor = mais perto |
| tudo azul | clear depth errado | `clear(1.0f)` |

---

## GFX-PERSP-04 — interpolação z/w

### Onde colocar (PERSP-04)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/extension/perspective.cpp` |
| Função | `perspective_z_at` |
| Substituir | `TODO [GFX-PERSP-04]` |

### 1. O problema (PERSP-04)

Após projeção perspectiva, interpolar `z` linearmente em screen space está errado; o lab documenta interpolação de `z/w` (ou `1/z` em pipelines avançados).

### Escreva o código (PERSP-04)

```cpp
float perspective_z_at(float z0, float w0, float z1, float w1, float t) {
    const float iz0 = (w0 != 0.0f) ? (z0 / w0) : z0;
    const float iz1 = (w1 != 0.0f) ? (z1 / w1) : z1;
    return iz0 * (1.0f - t) + iz1 * t;
}
```

### Por que funciona (PERSP-04)

Interpolação em espaço já dividido por `w` aproxima o comportamento correto para este exercício.

### Verifique (PERSP-04)

Caso 4: `t=0.5` entre vértices simétricos retorna média de `z/w`.

### Resultado esperado

`ctest` verde; VISUAL-01: CPU e GL mostram azul na frente.
