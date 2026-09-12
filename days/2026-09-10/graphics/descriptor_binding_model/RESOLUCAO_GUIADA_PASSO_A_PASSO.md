# Resolução guiada — descriptor_binding_model

## Mapa exato starter → resolução

| TODO ID | Arquivo starter | Função / âncora | Substituir |
|---------|-----------------|-----------------|------------|
| `GFX-DESC-LAYOUT` | `starter/core/descriptor.cpp` | `make_layout` | stub `TODO [GFX-DESC-LAYOUT]` |
| `GFX-DESC-BIND` | `starter/core/descriptor.cpp` | `bind` | stub `TODO [GFX-DESC-BIND]` |
| `GFX-DESC-SAMPLE` | `starter/core/descriptor.cpp` | `sample` | stub `TODO [GFX-DESC-SAMPLE]` |

---

## Baseline

```powershell
cd days/2026-09-10/graphics/descriptor_binding_model/starter
cmake -S . -B build_ci -DCMAKE_BUILD_TYPE=Release
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado antes dos TODOs:** `test_descriptor` falha nos asserts de layout/bind/sample.

---

## Relatório de resolução

## GFX-DESC-LAYOUT — `make_layout`

### Onde colocar (LAYOUT)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/core/descriptor.cpp` |
| Função | `make_layout` |
| Substituir | stub `TODO [GFX-DESC-LAYOUT]` |

### 1. O problema (LAYOUT)

Sem clamp, `slot_count` inválido quebra o array fixo e o Caso 1 falha.

### Escreva o código (LAYOUT)

```cpp
DescriptorLayout make_layout(int slot_count) {
    DescriptorLayout layout{};
    if (slot_count < 0) slot_count = 0;
    if (slot_count > kMaxSlots) slot_count = kMaxSlots;
    layout.slot_count = slot_count;
    return layout;
}
```

### Por que funciona (LAYOUT)

Normaliza a capacidade antes de qualquer bind — contrato estável para o set.

### Verifique (LAYOUT)

`make_layout(3)==3`, `make_layout(99)==kMaxSlots`. `ctest` ainda falha em bind.

### Debug (LAYOUT)

| Sintoma | Causa | Ação |
|---------|-------|------|
| 99 não clampa | faltou max | compare com `kMaxSlots` |

---

## GFX-DESC-BIND — `bind`

### Onde colocar (BIND)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/core/descriptor.cpp` |
| Função | `bind` |
| Substituir | stub `TODO [GFX-DESC-BIND]` |

### 1. O problema (BIND)

Sem gravar tint + flag, `sample` não tem o que devolver e os painéis ficam pretos.

### Escreva o código (BIND)

```cpp
void bind(DescriptorSet& set, int slot, Vec3 tint) {
    if (slot < 0 || slot >= set.slot_count || slot >= kMaxSlots) return;
    set.tints[slot] = tint;
    set.bound[slot] = true;
}
```

### Por que funciona (BIND)

Guarda o recurso e marca o slot válido — espelho de update de descriptor.

### Verifique (BIND)

Após três binds RGB, `bound[0..2]` true. Sample ainda pode falhar se não implementado.

### Debug (BIND)

| Sintoma | Causa | Ação |
|---------|-------|------|
| escrita ignorada | `slot_count` 0 | setar do layout |

---

## GFX-DESC-SAMPLE — `sample`

### Onde colocar (SAMPLE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/core/descriptor.cpp` |
| Função | `sample` |
| Substituir | stub `TODO [GFX-DESC-SAMPLE]` |

### 1. O problema (SAMPLE)

O draw precisa de um tint por painel; sem sample seguro, ou crash ou lixo.

### Escreva o código (SAMPLE)

```cpp
Vec3 sample(const DescriptorSet& set, int slot) {
    if (slot < 0 || slot >= set.slot_count || slot >= kMaxSlots || !set.bound[slot]) {
        return Vec3{0.0f, 0.0f, 0.0f};
    }
    return set.tints[slot];
}
```

### Por que funciona (SAMPLE)

Valida range + bound; devolve zero definido quando inválido — Caso 3 cobre o slot 7.

### Verifique (SAMPLE)

`ctest` passa: R/G/B nos slots 0..2 e zero no 7.

### Debug (SAMPLE)

| Sintoma | Causa | Ação |
|---------|-------|------|
| sempre zero | não checou `bound` ao contrário | retorne tint se bound |
