#include "resource_state.hpp"

bool ResourceTracker::transition(State next) {
    // TODO [GFX-STATE-TRANSITION-01]
    (void)next;
    return false;
}

std::string to_vulkan(State state) {
    // TODO [GFX-VK-MAP-02]
    (void)state;
    return {};
}

std::string to_d3d12(State state) {
    // TODO [GFX-D3D12-MAP-03]
    (void)state;
    return {};
}
