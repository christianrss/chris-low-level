#include "descriptor.hpp"

namespace desc {

DescriptorLayout make_layout(int slot_count) {
    // PEDAGOGY-SOLUTION: GFX-DESC-LAYOUT
    DescriptorLayout layout{};
    if (slot_count < 0) {
        slot_count = 0;
    }
    if (slot_count > kMaxSlots) {
        slot_count = kMaxSlots;
    }
    layout.slot_count = slot_count;
    return layout;
}

void bind(DescriptorSet& set, int slot, Vec3 tint) {
    // PEDAGOGY-SOLUTION: GFX-DESC-BIND
    if (slot < 0 || slot >= set.slot_count || slot >= kMaxSlots) {
        return;
    }
    set.tints[slot] = tint;
    set.bound[slot] = true;
}

Vec3 sample(const DescriptorSet& set, int slot) {
    // PEDAGOGY-SOLUTION: GFX-DESC-SAMPLE
    if (slot < 0 || slot >= set.slot_count || slot >= kMaxSlots || !set.bound[slot]) {
        return Vec3{0.0f, 0.0f, 0.0f};
    }
    return set.tints[slot];
}

}  // namespace desc
