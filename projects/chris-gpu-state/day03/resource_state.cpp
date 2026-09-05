// SOLVES [GFX-STATE-TRANSITION-01]
// SOLVES [GFX-VK-MAP-02]
// SOLVES [GFX-D3D12-MAP-03]
#include "resource_state.hpp"

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
