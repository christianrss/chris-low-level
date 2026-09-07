#include "depth_buffer.hpp"
#include <algorithm>
#include <cstring>

namespace depth_lab {

void DepthBuffer::resize(int w, int h) {
    width = w;
    height = h;
    z.assign(static_cast<std::size_t>(w) * h, 1.0f);
}

void DepthBuffer::clear(float far_z) {
    std::fill(z.begin(), z.end(), far_z);
}

bool DepthBuffer::test(int x, int y, float depth) {
    // TODO [GFX-DEPTH-CPU-01]
    (void)x;
    (void)y;
    (void)depth;
    return false;
}

std::uint32_t hash_region(const std::vector<Color>& fb, int x0, int y0, int w, int h, int pitch) {
    std::uint32_t hsh = 2166136261u;
    for (int y = y0; y < y0 + h; ++y) {
        for (int x = x0; x < x0 + w; ++x) {
            const auto& c = fb[static_cast<std::size_t>(y) * pitch + x];
            hsh ^= c.r;
            hsh *= 16777619u;
            hsh ^= c.g;
            hsh *= 16777619u;
            hsh ^= c.b;
            hsh *= 16777619u;
        }
    }
    return hsh;
}

}  // namespace depth_lab
