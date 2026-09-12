// PEDAGOGY-TEST: GFX-DESC-LAYOUT
// PEDAGOGY-TEST: GFX-DESC-BIND
// PEDAGOGY-TEST: GFX-DESC-SAMPLE
// Test cases (TESTES_GUIADOS.md):
// Caso 1: make_layout clamps slot count (GFX-DESC-LAYOUT).
// Caso 2: bind stores tint per slot (GFX-DESC-BIND).
// Caso 3: sample returns tint or zero (GFX-DESC-SAMPLE).
#include <cassert>
#include <cmath>
#include "descriptor.hpp"

using namespace desc;

static bool near3(Vec3 a, Vec3 b) {
    return std::fabs(a.x - b.x) < 1e-5f && std::fabs(a.y - b.y) < 1e-5f &&
           std::fabs(a.z - b.z) < 1e-5f;
}

int main() {
    DescriptorLayout layout = make_layout(3);
    assert(layout.slot_count == 3);
    assert(make_layout(99).slot_count == kMaxSlots);

    DescriptorSet set{};
    set.slot_count = layout.slot_count;
    bind(set, 0, {1.0f, 0.0f, 0.0f});
    bind(set, 1, {0.0f, 1.0f, 0.0f});
    bind(set, 2, {0.0f, 0.0f, 1.0f});
    assert(set.bound[0] && set.bound[1] && set.bound[2]);
    assert(near3(sample(set, 0), {1.0f, 0.0f, 0.0f}));
    assert(near3(sample(set, 1), {0.0f, 1.0f, 0.0f}));
    assert(near3(sample(set, 2), {0.0f, 0.0f, 1.0f}));
    assert(near3(sample(set, 7), {0.0f, 0.0f, 0.0f}));
    return 0;
}
