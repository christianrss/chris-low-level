# RESOLUÇÃO GUIADA — Graphics / Vulkan–D3D12 resource states

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `GFX-STATE-TRANSITION-01` | `starter/resource_state.cpp` | `ResourceTracker::transition` |
| `GFX-VK-MAP-02` | `starter/resource_state.cpp` | `to_vulkan` |
| `GFX-D3D12-MAP-03` | `starter/resource_state.cpp` | `to_d3d12` |

Cada ID existe como `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` no gabarito e `PEDAGOGY-TEST: ID` em `starter/test_states.cpp`.

> Trabalhe em `days/2026-09-05/graphics/vulkan_d3d12_resource_states/starter/`. `solutions/` é gabarito — consulte só depois da tentativa.

> Não comece copiando `solutions/`. Compile e rode `ctest` após cada TODO.

---

## GFX-STATE-TRANSITION-01 — tabela de transições

### 1. O problema (starter stub)

```cpp
bool ResourceTracker::transition(State next) {
    // TODO [GFX-STATE-TRANSITION-01]
    (void)next;
    return false;
}
```

Sempre `false` → o primeiro `assert(tracker.transition(ShaderRead))` falha. Baseline esperado.

### 2. O algoritmo

```text
se next == state_ → return false          # no-op rejeitado
allowed ← (CopyDst→ShaderRead) ∨
          (ShaderRead→RenderTarget) ∨
          (RenderTarget→Present) ∨
          (Present→RenderTarget)
se allowed: state_ ← next
return allowed                            # falha não muta state_
```

### 3. Código completo

Em `starter/resource_state.cpp`:

```cpp
bool ResourceTracker::transition(State next) {
    if (next == state_) {
        return false;
    }

    const bool allowed =
        (state_ == State::CopyDst && next == State::ShaderRead) ||
        (state_ == State::ShaderRead && next == State::RenderTarget) ||
        (state_ == State::RenderTarget && next == State::Present) ||
        (state_ == State::Present && next == State::RenderTarget);

    if (allowed) {
        state_ = next;
    }
    return allowed;
}
```

### 4. Por que funciona?

- A tabela espelha o pipeline do teste: upload → sample → draw → present, com loop `Present→RenderTarget` para o próximo frame.
- No-op e saltos inválidos (`Present→CopyDst`) retornam `false` sem tocar `state_`.
- Mutação só dentro de `if (allowed)`: rejeição deixa o tracker no último estado aceito.

### 5. Verificação parcial

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-05\graphics\vulkan_d3d12_resource_states\starter
cmake -S . -B build
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

Ainda FAIL nos maps. Trace no papel:

```text
CopyDst → ShaderRead → RenderTarget → Present → CopyDst?
  true      true           true          true      false (fica Present)
```

---

## GFX-VK-MAP-02 — layouts Vulkan

### 1. O problema (starter stub)

```cpp
std::string to_vulkan(State state) {
    // TODO [GFX-VK-MAP-02]
    (void)state;
    return {};
}
```

String vazia → assert de `Present` falha.

### 2. O algoritmo

```text
switch(state):
  CopyDst      → VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL
  ShaderRead   → VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL
  RenderTarget → VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL
  Present      → VK_IMAGE_LAYOUT_PRESENT_SRC_KHR
default → ""
```

### 3. Código completo

```cpp
std::string to_vulkan(State state) {
    switch (state) {
    case State::CopyDst:
        return "VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL";
    case State::ShaderRead:
        return "VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL";
    case State::RenderTarget:
        return "VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL";
    case State::Present:
        return "VK_IMAGE_LAYOUT_PRESENT_SRC_KHR";
    }
    return {};
}
```

### 4. Por que funciona?

Cada estado abstrato é o layout que a validation layer espera naquela fase. O teste fixa `Present` → `VK_IMAGE_LAYOUT_PRESENT_SRC_KHR` (sufixo `_KHR` obrigatório).

### 5. Verificação parcial

Recompile; o assert Vulkan passa. D3D12 ainda vazio → FAIL restante.

---

## GFX-D3D12-MAP-03 — estados D3D12

### 1. O problema (starter stub)

```cpp
std::string to_d3d12(State state) {
    // TODO [GFX-D3D12-MAP-03]
    (void)state;
    return {};
}
```

### 2. O algoritmo

```text
switch(state):
  CopyDst      → D3D12_RESOURCE_STATE_COPY_DEST
  ShaderRead   → D3D12_RESOURCE_STATE_PIXEL_SHADER_RESOURCE
  RenderTarget → D3D12_RESOURCE_STATE_RENDER_TARGET
  Present      → D3D12_RESOURCE_STATE_PRESENT
```

### 3. Código completo

```cpp
std::string to_d3d12(State state) {
    switch (state) {
    case State::CopyDst:
        return "D3D12_RESOURCE_STATE_COPY_DEST";
    case State::ShaderRead:
        return "D3D12_RESOURCE_STATE_PIXEL_SHADER_RESOURCE";
    case State::RenderTarget:
        return "D3D12_RESOURCE_STATE_RENDER_TARGET";
    case State::Present:
        return "D3D12_RESOURCE_STATE_PRESENT";
    }
    return {};
}
```

### 4. Por que funciona?

D3D12 nomeia o mesmo pipeline com constantes paralelas; `RENDER_TARGET` é o par de `COLOR_ATTACHMENT_OPTIMAL`. O teste fixa `RenderTarget` → `D3D12_RESOURCE_STATE_RENDER_TARGET`.

### 5. Verificação

```powershell
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

Esperado: `OK gpu states` e 100% passed.

---

## Como depurar se falhar

- Primeiro `transition` false: faltou `CopyDst→ShaderRead` ou retorna sempre false.
- `Present→CopyDst` true: mutou `state_` em transição inválida.
- Vulkan vazio/errado: typo `PRESENT_SRC` sem `_KHR`.
- D3D12 errado: confundiu `RENDER_TARGET` com depth write.

## Relatório de resolução

| ID | Arquivo | Resultado esperado |
|----|---------|-------------------|
| GFX-STATE-TRANSITION-01 | `resource_state.cpp` | pipeline CopyDst→Present; rejeita Present→CopyDst |
| GFX-VK-MAP-02 | `resource_state.cpp` | `Present` → `VK_IMAGE_LAYOUT_PRESENT_SRC_KHR` |
| GFX-D3D12-MAP-03 | `resource_state.cpp` | `RenderTarget` → `D3D12_RESOURCE_STATE_RENDER_TARGET` |

Critério de aceite: `ctest` reporta `OK gpu states` e 100% dos testes.
