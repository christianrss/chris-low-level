# Resolução guiada — pipeline_state_object

## Mapa exato starter → resolução

| TODO ID | Arquivo starter | Função / âncora | Substituir |
|---------|-----------------|-----------------|------------|
| `GFX-PSO-CREATE` | `starter/core/pso.cpp` | `create_default_pso` | stub `TODO [GFX-PSO-CREATE]` |
| `GFX-PSO-BIND` | `starter/core/pso.cpp` | `bind` | stub `TODO [GFX-PSO-BIND]` |
| `GFX-PSO-CYCLE` | `starter/core/pso.cpp` | `cycle_pso` | stub `TODO [GFX-PSO-CYCLE]` |

---

## Baseline

```powershell
cd days/2026-09-10/graphics/pipeline_state_object/starter
cmake -S . -B build_ci -DCMAKE_BUILD_TYPE=Release
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado antes dos TODOs:** compila; `test_pso` falha em asserts de create/bind/cycle.

---

## Relatório de resolução

## GFX-PSO-CREATE — `create_default_pso`

### Onde colocar (CREATE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/core/pso.cpp` |
| Função | `create_default_pso` |
| Substituir | corpo com `TODO [GFX-PSO-CREATE]` |

### 1. O problema (CREATE)

Sem default, o ativo começa a zeros e o triângulo fica preto/invisível. O lab exige o preset 0 (sólido vermelho).

### Escreva o código (CREATE)

```cpp
PipelineState create_default_pso() {
    return preset_at(0);
}
```

### Por que funciona (CREATE)

`preset_at(0)` já define fill sólido e `r > 0.5`, batendo o Caso 1 sem duplicar literais.

### Verifique (CREATE)

`ctest`: assert `fill_mode == kFillSolid` e `r > 0.5`. Ainda falha em bind/cycle.

### Debug (CREATE)

| Sintoma | Causa | Ação |
|---------|-------|------|
| r baixo | retornou `{}` | use `preset_at(0)` |

---

## GFX-PSO-BIND — `bind`

### Onde colocar (BIND)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/core/pso.cpp` |
| Função | `bind` |
| Substituir | stub `TODO [GFX-PSO-BIND]` |

### 1. O problema (BIND)

Sem cópia, `active` permanece zerado mesmo após escolher um preset — o draw nunca vê a cor/wire.

### Escreva o código (BIND)

```cpp
void bind(PipelineState& active, const PipelineState& src) {
    active = src;
}
```

### Por que funciona (BIND)

Atribuição de struct copia todos os campos; é o análogo pedagógico de `BindPipeline`.

### Verifique (BIND)

Após `bind(active, preset_at(1))`, `fill_mode == kFillWire` e `g` coincide com o preset.

### Debug (BIND)

| Sintoma | Causa | Ação |
|---------|-------|------|
| só cor muda | copiou campos à mão e esqueceu fill | use `active = src` |

---

## GFX-PSO-CYCLE — `cycle_pso`

### Onde colocar (CYCLE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/core/pso.cpp` |
| Função | `cycle_pso` |
| Substituir | stub `TODO [GFX-PSO-CYCLE]` |

### 1. O problema (CYCLE)

Sem avanço modular, a demo visual não troca fill/wire/cor a cada 2s e o Caso 3 falha.

### Escreva o código (CYCLE)

```cpp
void cycle_pso(PipelineState& active, int& preset_index) {
    preset_index = (preset_index + 1) % kPresetCount;
    bind(active, preset_at(preset_index));
}
```

### Por que funciona (CYCLE)

O módulo 3 garante 0→1→2→0; `bind` aplica o snapshot imediatamente para o próximo frame.

### Verifique (CYCLE)

Três cycles: índices 1,2,0 com wire → azul → solid. `ctest` deve passar.

### Debug (CYCLE)

| Sintoma | Causa | Ação |
|---------|-------|------|
| idx nunca muda | esqueceu incrementar | `(idx+1)%3` |
| estado antigo | cycle sem bind | chame `bind` |
