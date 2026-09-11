#pragma once
#include <cstdint>
struct Pixel { uint8_t r,g,b,a; };
void blend_pixel(Pixel &dst, Pixel src);
void blend_scanline(Pixel *dst, const Pixel *src, int n);
int blend_coverage(const Pixel *dst, int n, uint8_t min_a);
