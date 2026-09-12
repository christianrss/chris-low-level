#pragma once

namespace barr {

enum class ResourceState {
    Undefined = 0,
    CopyDst = 1,
    ShaderRead = 2,
    RenderTarget = 3,
    Present = 4,
};

struct Resource {
    ResourceState state = ResourceState::Undefined;
};

bool can_transition(ResourceState from, ResourceState to);
bool apply_barrier(Resource& resource, ResourceState to);
bool tick_barrier(Resource& resource);

}  // namespace barr
