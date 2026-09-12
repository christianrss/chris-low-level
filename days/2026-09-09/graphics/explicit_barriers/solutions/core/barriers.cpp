#include "barriers.hpp"

namespace barr {

bool can_transition(ResourceState from, ResourceState to) {
    // PEDAGOGY-SOLUTION: GFX-BAR-VALID
    if (from == ResourceState::Undefined && to == ResourceState::CopyDst) {
        return true;
    }
    if (from == ResourceState::CopyDst && to == ResourceState::ShaderRead) {
        return true;
    }
    if (from == ResourceState::ShaderRead && to == ResourceState::RenderTarget) {
        return true;
    }
    if (from == ResourceState::RenderTarget && to == ResourceState::Present) {
        return true;
    }
    if (from == ResourceState::Present && to == ResourceState::RenderTarget) {
        return true;
    }
    return false;
}

bool apply_barrier(Resource& resource, ResourceState to) {
    // PEDAGOGY-SOLUTION: GFX-BAR-APPLY
    if (!can_transition(resource.state, to)) {
        return false;
    }
    resource.state = to;
    return true;
}

bool tick_barrier(Resource& resource) {
    // PEDAGOGY-SOLUTION: GFX-BAR-TICK
    // Demo loop: Undefined→CopyDst→ShaderRead→RenderTarget→Present→(soft reset)Undefined
    if (resource.state == ResourceState::Present) {
        resource.state = ResourceState::Undefined;
        return true;
    }
    ResourceState next = ResourceState::CopyDst;
    switch (resource.state) {
    case ResourceState::Undefined:
        next = ResourceState::CopyDst;
        break;
    case ResourceState::CopyDst:
        next = ResourceState::ShaderRead;
        break;
    case ResourceState::ShaderRead:
        next = ResourceState::RenderTarget;
        break;
    case ResourceState::RenderTarget:
        next = ResourceState::Present;
        break;
    case ResourceState::Present:
        next = ResourceState::Undefined;
        break;
    }
    return apply_barrier(resource, next);
}

}  // namespace barr
