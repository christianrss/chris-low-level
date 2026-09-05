# Resolução guiada passo a passo — Graphics — Vulkan / D3D12 Resource States

## Mapa exato starter → resolução

- `GFX-STATE-TRANSITION-01` → `starter/resource_state.cpp` (`ResourceTracker::transition`)
- `GFX-VK-MAP-02` → `starter/resource_state.cpp` (`to_vulkan`)
- `GFX-D3D12-MAP-03` → `starter/resource_state.cpp` (`to_d3d12`)

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-05/graphics/vulkan_d3d12_resource_states/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

## 0. Preparar o projeto

Na raiz do repositório:

```bash
cmake -S days/2026-09-05/graphics/vulkan_d3d12_resource_states/starter -B days/2026-09-05/graphics/vulkan_d3d12_resource_states/starter/build
cmake --build days/2026-09-05/graphics/vulkan_d3d12_resource_states/starter/build
ctest --test-dir days/2026-09-05/graphics/vulkan_d3d12_resource_states/starter/build --output-on-failure
```

O build deve funcionar. Os testes **devem falhar**: `transition` retorna `false` na primeira chamada e os mapeamentos devolvem string vazia. Esse é o baseline.

## `GFX-STATE-TRANSITION-01` — pipeline de transições

### Arquivo

Abra:

```text
starter/resource_state.cpp
```

Localize:

```cpp
bool ResourceTracker::transition(State next) {
```

Substitua o corpo por:

```cpp
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
```

### Por que funciona?

A tabela codifica exatamente o pipeline do teste: upload → leitura → render → apresentar, com loop `Present → RenderTarget` para frames subsequentes. No-op e saltos inválidos retornam `false` sem mutar `state_`.

### Verificação manual

```text
CopyDst → ShaderRead → RenderTarget → Present → CopyDst?
  true      true           true          true      false (fica Present)
```

### Checkpoint

Os quatro primeiros `assert(tracker.transition(...))` do teste passam; o quinto `assert(!tracker.transition(CopyDst))` ainda depende dos mapeamentos apenas se você rodar o binário inteiro — mas a transição já deve estar correta.

---

## `GFX-VK-MAP-02` — layout Vulkan

### Arquivo

Localize:

```cpp
std::string to_vulkan(State state) {
```

Substitua o corpo por:

```cpp
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
```

### Por que funciona?

Cada estado abstrato corresponde ao layout que a validation layer espera para aquela fase de uso da imagem. O teste verifica explicitamente `Present`.

### Verificação manual

```text
to_vulkan(State::Present) == "VK_IMAGE_LAYOUT_PRESENT_SRC_KHR"
```

### Checkpoint

O assert de Vulkan no teste passa após recompilar.

---

## `GFX-D3D12-MAP-03` — estado D3D12

### Arquivo

Localize:

```cpp
std::string to_d3d12(State state) {
```

Substitua o corpo por:

```cpp
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
```

### Por que funciona?

D3D12 nomeia estados de forma paralela a Vulkan; `RENDER_TARGET` é o equivalente direto de `COLOR_ATTACHMENT_OPTIMAL` para escrita de cor.

### Verificação manual

```text
to_d3d12(State::RenderTarget) == "D3D12_RESOURCE_STATE_RENDER_TARGET"
```

### Checkpoint

Todos os asserts de `test_states.cpp` passam.

---

## Rode os testes novamente

```bash
cmake --build days/2026-09-05/graphics/vulkan_d3d12_resource_states/starter/build
ctest --test-dir days/2026-09-05/graphics/vulkan_d3d12_resource_states/starter/build --output-on-failure
```

Saída esperada contém:

```text
OK gpu states
100% tests passed
```

## Como depurar se falhar

- Primeiro `transition` falha: você retorna `false` sempre ou esqueceu `CopyDst → ShaderRead`.
- `Present → CopyDst` retorna `true`: estado foi alterado indevidamente em transição inválida.
- String Vulkan vazia: typo no nome (`PRESENT_SRC` vs `PRESENT_SRC_KHR`).
- D3D12 errado: confundiu `RENDER_TARGET` com `DEPTH_WRITE`.

## Solução final comentada

Compare `starter/resource_state.cpp` com `solutions/resource_state.cpp`. Justifique cada aresta permitida e cada string de API.

## Relatório de resolução

| ID | Arquivo | Resultado esperado |
|----|---------|-------------------|
| GFX-STATE-TRANSITION-01 | `resource_state.cpp` | pipeline CopyDst→Present; rejeita Present→CopyDst |
| GFX-VK-MAP-02 | `resource_state.cpp` | `Present` → `VK_IMAGE_LAYOUT_PRESENT_SRC_KHR` |
| GFX-D3D12-MAP-03 | `resource_state.cpp` | `RenderTarget` → `D3D12_RESOURCE_STATE_RENDER_TARGET` |

Critério de aceite: `ctest` reporta `OK gpu states` e 100% dos testes.

### Template do relatório

```
Aluno:
Módulo: Graphics — Vulkan / D3D12 Resource States
Data:

1. TODOs: GFX-STATE-TRANSITION-01, GFX-VK-MAP-02, GFX-D3D12-MAP-03
2. Primeira falha: [ex.: transition(CopyDst→ShaderRead) retornou false]
3. Correção aplicada: [ex.: tabela de transições + switches de mapeamento]
4. Evidência: [colar saída OK gpu states]
```
