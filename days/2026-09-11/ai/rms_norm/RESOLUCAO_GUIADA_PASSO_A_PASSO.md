# Resolução guiada — rms_norm

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `AI-RMS-01` | `starter/rms.c` | `rms_of` |
| `AI-RMS-02` | `starter/rms.c` | `rms_norm` |
| `AI-RMS-03` | `starter/rms.c` | `rms_norm_g` |

## Baseline

```powershell
cd days/2026-09-11/ai/rms_norm/starter
cmake -S . -B build_ci -G Ninja
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado:** FAIL.

## AI-RMS-01

### Onde colocar (AI-RMS-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/rms.c` |
| Função | `rms_of` |
| Substituir | o corpo sob o comentário `TODO [AI-RMS-01]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

rms de [3,4] = sqrt(12.5).

### Algoritmo / trace

soma x^2 / n + eps; sqrt.

### Escreva o código

```c
    float s = 0.f; int i;
    if (!x || n <= 0) return -1.f;
    for (i = 0; i < n; i++) s += x[i] * x[i];
    return sqrtf(s / (float)n + eps);
```

### Por que funciona?

Mean dos quadrados, não da soma.

### Verifique

fabs(r-sqrt(12.5))<1e-5.

### Código completo alinhado ao solutions/ (AI-RMS-01)

```c
PEDAGOGY-SOLUTION: AI-RMS-01 */
    float s = 0.f; int i;
    if (!x || n <= 0) return -1.f;
    for (i = 0; i < n; i++) s += x[i] * x[i];
    return sqrtf(s / (float)n + eps);
}
int rms_norm(const float *x, int n, float eps, float *out) {
    /* 
```

## AI-RMS-02

### Onde colocar (AI-RMS-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/rms.c` |
| Função | `rms_norm` |
| Substituir | o corpo sob o comentário `TODO [AI-RMS-02]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

out = x/rms.

### Algoritmo / trace

chame rms_of; divida.

### Escreva o código

```c
    float r; int i;
    if (!x || !out || n <= 0) return -1;
    r = rms_of(x, n, eps);
    if (r <= 0.f) return -1;
    for (i = 0; i < n; i++) out[i] = x[i] / r;
    return 0;
```

### Por que funciona?

Normaliza magnitude RMS.

### Verifique

out[0]==3/rms.

### Código completo alinhado ao solutions/ (AI-RMS-02)

```c
PEDAGOGY-SOLUTION: AI-RMS-02 */
    float r; int i;
    if (!x || !out || n <= 0) return -1;
    r = rms_of(x, n, eps);
    if (r <= 0.f) return -1;
    for (i = 0; i < n; i++) out[i] = x[i] / r;
    return 0;
}
int rms_norm_g(const float *x, const float *g, int n, float eps, float *out) {
    /* 
```

## AI-RMS-03

### Onde colocar (AI-RMS-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/rms.c` |
| Função | `rms_norm_g` |
| Substituir | o corpo sob o comentário `TODO [AI-RMS-03]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Gain elementwise após norm.

### Algoritmo / trace

rms_norm depois *= g[i].

### Escreva o código

```c
    int i;
    if (!g || rms_norm(x, n, eps, out) != 0) return -1;
    for (i = 0; i < n; i++) out[i] *= g[i];
    return 0;
```

### Por que funciona?

g escala canais.

### Verifique

2*3/rms.

### Código completo alinhado ao solutions/ (AI-RMS-03)

```c
PEDAGOGY-SOLUTION: AI-RMS-03 */
    int i;
    if (!g || rms_norm(x, n, eps, out) != 0) return -1;
    for (i = 0; i < n; i++) out[i] *= g[i];
    return 0;
}
```

## Debug

| Sintoma | Correção |
|---------|----------|
| rms grande | divida por n |

## Relatório de resolução

- TODOs: [ ]
