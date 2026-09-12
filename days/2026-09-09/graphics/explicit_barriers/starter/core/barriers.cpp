#include "barriers.hpp"

namespace barr {

bool can_transition(ResourceState from, ResourceState to) {
    // TODO [GFX-BAR-VALID]: allow only legal resource state edges
    (void)from;
    (void)to;
    return false;
}

bool apply_barrier(Resource& resource, ResourceState to) {
    // TODO [GFX-BAR-APPLY]: validate then write resource.state
    (void)resource;
    (void)to;
    return false;
}

bool tick_barrier(Resource& resource) {
    // TODO [GFX-BAR-TICK]: advance demo cycle; soft-reset Present→Undefined
    (void)resource;
    return false;
}

}  // namespace barr
