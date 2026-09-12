#include "blend.hpp"
namespace blendlab {
void blend_pixel(Pixel& dst, Pixel src) {
    // PEDAGOGY-SOLUTION: GFX-BLEND-PIXEL
    const float sa = src.a / 255.0f;
    const float da = 1.0f - sa;
    dst.r = static_cast<std::uint8_t>(src.r * sa + dst.r * da);
    dst.g = static_cast<std::uint8_t>(src.g * sa + dst.g * da);
    dst.b = static_cast<std::uint8_t>(src.b * sa + dst.b * da);
    dst.a = 255;
}
void blend_scanline(Pixel* dst, const Pixel* src, int n) {
    // PEDAGOGY-SOLUTION: GFX-BLEND-SCAN
    for (int i = 0; i < n; ++i) blend_pixel(dst[i], src[i]);
}
void update_sprite(Sprite& s, float dt, float minx, float miny, float maxx, float maxy) {
    // PEDAGOGY-SOLUTION: GFX-BLEND-SPRITE
    s.x += s.vx * dt;
    s.y += s.vy * dt;
    if (s.x < minx || s.x + s.w > maxx) { s.vx = -s.vx; s.x += s.vx * dt; }
    if (s.y < miny || s.y + s.h > maxy) { s.vy = -s.vy; s.y += s.vy * dt; }
}
}
