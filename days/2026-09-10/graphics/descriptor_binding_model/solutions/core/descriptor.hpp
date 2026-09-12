#pragma once

namespace desc {

struct Vec3 {
    float x = 0.0f;
    float y = 0.0f;
    float z = 0.0f;
};

constexpr int kMaxSlots = 8;

struct DescriptorLayout {
    int slot_count = 0;
};

struct DescriptorSet {
    Vec3 tints[kMaxSlots]{};
    bool bound[kMaxSlots]{};
    int slot_count = 0;
};

DescriptorLayout make_layout(int slot_count);
void bind(DescriptorSet& set, int slot, Vec3 tint);
Vec3 sample(const DescriptorSet& set, int slot);

}  // namespace desc
