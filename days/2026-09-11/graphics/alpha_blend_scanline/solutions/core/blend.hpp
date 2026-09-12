#pragma once
#include <cstdint>
namespace blendlab {
struct Pixel { std::uint8_t r,g,b,a; };
struct Sprite { float x,y,vx,vy; int w,h; Pixel color; };
void blend_pixel(Pixel& dst, Pixel src);
void blend_scanline(Pixel* dst, const Pixel* src, int n);
void update_sprite(Sprite& s, float dt, float minx, float miny, float maxx, float maxy);
}
