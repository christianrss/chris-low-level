// PEDAGOGY-TEST [GFX-STATE-TRANSITION-01]: pipeline CopyDst→Present
// PEDAGOGY-TEST [GFX-VK-MAP-02]: mapeamento Vulkan
// PEDAGOGY-TEST [GFX-D3D12-MAP-03]: mapeamento D3D12
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
