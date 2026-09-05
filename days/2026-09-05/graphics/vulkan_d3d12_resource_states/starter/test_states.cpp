// PEDAGOGY-TEST: GFX-STATE-TRANSITION-01: pipeline CopyDst→Present
// PEDAGOGY-TEST: GFX-VK-MAP-02: mapeamento Vulkan
// PEDAGOGY-TEST: GFX-D3D12-MAP-03: mapeamento D3D12
// PEDAGOGY-TEST: GFX-STATE-TRANSITION-01: pipeline CopyDst→Present e rejeição inválida
// PEDAGOGY-TEST: GFX-VK-MAP-02: layout Vulkan de Present
// PEDAGOGY-TEST: GFX-D3D12-MAP-03: state D3D12 de RenderTarget
// Test cases (TESTES_GUIADOS.md):
// Caso 1: `test_states` valida pipeline CopyDst → ShaderRead → RenderTarget → Present.
// Caso 2: **Transição inválida:** CopyDst → Present retorna false.
// Caso 3: **Vulkan:** Present → `VK_IMAGE_LAYOUT_PRESENT_SRC_KHR`.
// Caso 4: **D3D12:** RenderTarget → `D3D12_RESOURCE_STATE_RENDER_TARGET`.
// Caso 5: Consulte diagrama de máquina de estados em TEORIA_PASSO_A_PASSO.md.
#include "resource_state.hpp"
#include <cassert>
#include <iostream>

int main() {
    ResourceTracker tracker(State::CopyDst);
    assert(tracker.transition(State::ShaderRead));
    assert(tracker.transition(State::RenderTarget));
    assert(tracker.transition(State::Present));
    assert(!tracker.transition(State::CopyDst));
    assert(to_vulkan(State::Present) == "VK_IMAGE_LAYOUT_PRESENT_SRC_KHR");
    assert(to_d3d12(State::RenderTarget) == "D3D12_RESOURCE_STATE_RENDER_TARGET");
    std::cout << "OK gpu states\n";
    return 0;
}