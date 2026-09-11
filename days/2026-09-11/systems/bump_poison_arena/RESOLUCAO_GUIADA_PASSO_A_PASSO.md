# Resolução guiada — bump_poison_arena

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `SYS-BUMP-01` | `starter/bump.cpp` | `arena_reset` |
| `SYS-BUMP-02` | `starter/bump.cpp` | `arena_alloc` |
| `SYS-BUMP-03` | `starter/bump.cpp` | `arena_check_canary` |

## Baseline

```powershell
cd days/2026-09-11/systems/bump_poison_arena/starter
cmake -S . -B build_ci -G Ninja
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado:** FAIL.

## SYS-BUMP-01

### Onde colocar (SYS-BUMP-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/bump.cpp` |
| Função | `arena_reset` |
| Substituir | o corpo sob o comentário `TODO [SYS-BUMP-01]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Sem poison o teste não distingue memória fresca.

### Algoritmo / trace

used=0; memset POISON.

### Escreva o código

```cpp
    a.used = 0;
    std::memset(a.buf, POISON, ARENA_CAP);
    /* done */
```

### Por que funciona?

Pinta 64 bytes e reinicia o bump.

### Verifique

Todos buf[i]==0xA5, used==0.

### Código completo alinhado ao solutions/ (SYS-BUMP-01)

```cpp
PEDAGOGY-SOLUTION: SYS-BUMP-01 */
    a.used = 0; std::memset(a.buf, POISON, ARENA_CAP);
}
void *arena_alloc(BumpArena &a, std::size_t n) {
    /* 
```

## SYS-BUMP-02

### Onde colocar (SYS-BUMP-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/bump.cpp` |
| Função | `arena_alloc` |
| Substituir | o corpo sob o comentário `TODO [SYS-BUMP-02]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Precisa used==9 e canário em buf[8].

### Algoritmo / trace

Se used+n+1>64 nullptr; senão reserva n+1.

### Escreva o código

```cpp
    if (n == 0 || a.used + n + 1 > ARENA_CAP) return nullptr;
    void *p = a.buf + a.used;
    a.used += n + 1;
    a.buf[a.used - 1] = CANARY;
    return p;
```

### Por que funciona?

O +1 reserva o canário.

### Verifique

alloc(56) → nullptr.

### Código completo alinhado ao solutions/ (SYS-BUMP-02)

```cpp
PEDAGOGY-SOLUTION: SYS-BUMP-02 */
    if (n == 0 || a.used + n + 1 > ARENA_CAP) return nullptr;
    void *p = a.buf + a.used; a.used += n + 1; a.buf[a.used - 1] = CANARY; return p;
}
int arena_check_canary(const BumpArena &a, const void *p, std::size_t n) {
    /* 
```

## SYS-BUMP-03

### Onde colocar (SYS-BUMP-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/bump.cpp` |
| Função | `arena_check_canary` |
| Substituir | o corpo sob o comentário `TODO [SYS-BUMP-03]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Detectar corrupção do byte após o payload.

### Algoritmo / trace

return b[n]==CANARY ? 0 : -1 com bounds.

### Escreva o código

```cpp
    if (!p || n == 0) return -1;
    const auto *b = static_cast<const std::uint8_t *>(p);
    if (b < a.buf || b + n >= a.buf + ARENA_CAP) return -1;
    return b[n] == CANARY ? 0 : -1;
```

### Por que funciona?

b[n] é o byte escrito no alloc.

### Verifique

Canário intacto→0; buf[8]=0→-1.

### Código completo alinhado ao solutions/ (SYS-BUMP-03)

```cpp
PEDAGOGY-SOLUTION: SYS-BUMP-03 */
    if (!p || n == 0) return -1;
    const auto *b = static_cast<const std::uint8_t *>(p);
    if (b < a.buf || b + n >= a.buf + ARENA_CAP) return -1;
    return b[n] == CANARY ? 0 : -1;
}
```

## Debug

| Sintoma | Correção |
|---------|----------|
| used=8 | some +1 |
| check b[n-1] | use b[n] |

## Relatório de resolução

- TODOs: [ ]
- Testes:
- Invariantes: CAP 64, A5, C3
