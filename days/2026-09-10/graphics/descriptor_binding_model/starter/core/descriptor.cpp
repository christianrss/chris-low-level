#include "descriptor.hpp"

namespace desc {

DescriptorLayout make_layout(int slot_count) {
    // TODO [GFX-DESC-LAYOUT]: clamp slot_count to [0, kMaxSlots] and store it
    (void)slot_count;
    return DescriptorLayout{};
}

void bind(DescriptorSet& set, int slot, Vec3 tint) {
    // TODO [GFX-DESC-BIND]: write tint into set.tints[slot] and mark bound
    (void)set;
    (void)slot;
    (void)tint;
}

Vec3 sample(const DescriptorSet& set, int slot) {
    // TODO [GFX-DESC-SAMPLE]: return bound tint or zero if unbound/OOB
    (void)set;
    (void)slot;
    return Vec3{};
}

}  // namespace desc
