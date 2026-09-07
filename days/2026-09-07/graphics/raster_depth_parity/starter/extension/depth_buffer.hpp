#pragma once
#include <cstdint>
#include <vector>

namespace depth_lab {

struct Vec3 { float x, y, z; };
struct Color { std::uint8_t r, g, b; };

class DepthBuffer {
public:
    int width = 0;
    int height = 0;
    std::vector<float> z;
    void resize(int w, int h);
    void clear(float far_z = 1.0f);
    bool test(int x, int y, float depth);
};

std::uint32_t hash_region(const std::vector<Color>& fb, int x0, int y0, int w, int h, int pitch);

}  // namespace depth_lab
